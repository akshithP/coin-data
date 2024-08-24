import requests
from datetime import datetime, timezone, timedelta
import pandas as pd

# Binance API endpoints
symbol_url = "https://api.binance.com/api/v3/exchangeInfo"
kline_url = "https://api.binance.com/api/v3/klines"
ticker_24h_url = "https://api.binance.com/api/v3/ticker/24hr"
price_stats_url = "https://api.binance.com/api/v3/ticker/24hr"

# Fetch all symbols/coins from Binance with USDT 
response = requests.get(symbol_url)
symbols_info = response.json()  # Directly get the JSON response (which is a dictionary)
symbols = [symbol['symbol'] for symbol in symbols_info['symbols'] if symbol['symbol'].endswith('USDT')]

# Calculate the timestamp for 6 months ago and 30 days ago from now
now = datetime.now(timezone.utc)
six_months_ago = now - timedelta(days=180)
thirty_days_ago = now - timedelta(days=30)
start_timestamp_6m = int(six_months_ago.timestamp() * 1000)
start_timestamp_30d = int(thirty_days_ago.timestamp() * 1000)

# List to hold the results
results = []

# Loop through each symbol/coin and fetch the kline (open, close, high, low) data
for symbol in symbols:
    # Parameters for the kline request for 6 months
    params_6m = {
        "symbol": symbol,
        "interval": "1d",  # 1 day interval for daily data
        "startTime": start_timestamp_6m,
        "limit": 1000  # Binance API limit, 1000 data points max
    }

    # Parameters for the kline request for 30 days
    params_30d = {
        "symbol": symbol,
        "interval": "1d",  # 1 day interval for daily data
        "startTime": start_timestamp_30d,
        "limit": 1000  # Binance API limit, 1000 data points max
    }

    # Send the GET request to fetch kline data for 6 months
    response_6m = requests.get(kline_url, params=params_6m)
    
    if response_6m.status_code == 200:
        data_6m = response_6m.json()
        
        # Check if the coin has at least 180 days of data
        if len(data_6m) >= 180:
            # Initialize variables for calculations
            percentage_differences_6m = []
            usdt_volumes_6m = []
            prices = []
            for candle in data_6m:
                high_price = float(candle[2])
                low_price = float(candle[3])
                close_price = float(candle[4])
                volume = float(candle[5])
                quote_volume = close_price * volume  # Calculate USDT volume

                # Calculate percentage difference
                percentage_difference = ((high_price - low_price) / low_price) * 100
                percentage_differences_6m.append(percentage_difference)
                
                # Collect USDT volumes and closing prices
                usdt_volumes_6m.append(quote_volume)
                prices.append(close_price)
            
            # Calculate the average percentage difference (not rounded) for 6 months
            average_difference_6m = sum(percentage_differences_6m) / len(percentage_differences_6m)
            
            # Calculate average USDT volume over the last 180 days
            average_usdt_volume_6m = sum(usdt_volumes_6m) / len(usdt_volumes_6m)
            
            # Calculate volatility as the standard deviation of the daily returns
            returns = [(prices[i + 1] - prices[i]) / prices[i] for i in range(len(prices) - 1)]
            volatility = round(pd.Series(returns).std() * 100, 2)  # Convert to percentage and round to 2 decimal places
            
            # Send the GET request to fetch kline data for 30 days
            response_30d = requests.get(kline_url, params=params_30d)
            data_30d = response_30d.json()
            
            if len(data_30d) > 0:
                # Calculate the average percentage difference for the last 30 days
                percentage_differences_30d = []
                for candle in data_30d:
                    high_price = float(candle[2])
                    low_price = float(candle[3])
                    percentage_difference = ((high_price - low_price) / low_price) * 100
                    percentage_differences_30d.append(percentage_difference)
                
                average_difference_30d = sum(percentage_differences_30d) / len(percentage_differences_30d)
            else:
                average_difference_30d = None  # If no data for 30 days, set as None
            
            # Fetch 24h ticker info for current volume in USDT
            ticker_response = requests.get(ticker_24h_url, params={"symbol": symbol})
            ticker_data = ticker_response.json()
            current_usdt_volume = float(ticker_data['quoteVolume'])  # Using quoteVolume for USDT volume
            current_price = float(ticker_data['lastPrice'])
            
            # Append to results
            results.append((
                symbol, 
                average_difference_6m,  # Average % Difference (6 months)
                average_difference_30d,  # Average % Difference (30 days)
                average_usdt_volume_6m,  # Average Volume in USDT (180 days)
                current_usdt_volume,  # Current 24H Volume in USDT
                volatility,  # Volatility
                current_price  # Current Price
            ))

# Convert to DataFrame for sorting and further processing
df_results = pd.DataFrame(results, columns=[
    "Coin Symbol", 
    "Average % Difference (High-Low) - 6 months", 
    "Average % Difference (High-Low) - 30 days", 
    "Average Volume (180 days)", 
    "Current Volume (24H)", 
    "Volatility (6 months)", 
    "Current Price"
])

# Ensure correct sorting in descending order by average percentage difference over 6 months
df_results = df_results.sort_values(by="Average % Difference (High-Low) - 6 months", ascending=False)

# Select the top 50 coins
top_50_results = df_results.head(100)

# Function to format large numbers into a human-readable format
def format_large_number(value):
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f} Trillion"
    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f} Billion"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f} Million"
    else:
        return f"${value:,.2f}"

# Apply formatting to the DataFrame
top_50_results["Average % Difference (High-Low) - 6 months"] = top_50_results["Average % Difference (High-Low) - 6 months"].apply(lambda x: f"{x:.8f}%")
top_50_results["Average % Difference (High-Low) - 30 days"] = top_50_results["Average % Difference (High-Low) - 30 days"].apply(lambda x: f"{x:.8f}%" if x is not None else "N/A")
top_50_results["Average Volume (180 days)"] = top_50_results["Average Volume (180 days)"].apply(format_large_number)
top_50_results["Current Volume (24H)"] = top_50_results["Current Volume (24H)"].apply(format_large_number)
top_50_results["Volatility (6 months)"] = top_50_results["Volatility (6 months)"].apply(lambda x: f"{x:.2f}%")
top_50_results["Current Price"] = top_50_results["Current Price"].apply(lambda x: f"${x:,.8f}")

# Print the formatted data to the console
print(top_50_results.to_string(index=False))

# Export the results to an Excel file with better formatting
excel_filename = "top_50_coins_data.xlsx"
top_50_results.to_excel(excel_filename, index=False)

# Display a confirmation message
print(f"\nData exported to {excel_filename} with formatted columns.")
