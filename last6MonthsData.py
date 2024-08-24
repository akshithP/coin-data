import requests
from datetime import datetime, timezone, timedelta
import pytz
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Slider
import matplotlib.dates as mdates

# Binance API endpoint for candlestick data
url = "https://api.binance.com/api/v3/klines"

# Set up the timezone for Australia/Sydney
aedt = pytz.timezone('Australia/Sydney')

# Calculate the timestamp for 6 months ago from now in AEDT
now_aedt = datetime.now(aedt)
six_months_ago_aedt = now_aedt - timedelta(days=180)
start_timestamp = int(six_months_ago_aedt.timestamp() * 1000)

# Parameters for the request to get daily data
params = {
    "symbol": "PEOPLEUSDT",  # Change this to the coin of your choice
    "interval": "1d",  # 1 day interval for daily data
    "startTime": start_timestamp,
    "limit": 180  # 180 data points for 180 days (approx. 6 months)
}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Prepare lists to hold the extracted data
    open_times = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    percentage_differences = []
    volumes = []

    # Process each candlestick entry
    for candle in data:
        # Convert the Open time to AEDT
        open_time_utc = datetime.fromtimestamp(candle[0] / 1000, timezone.utc)
        open_time_aedt = open_time_utc.astimezone(aedt)
        
        # Append data to lists
        open_times.append(open_time_aedt)
        open_prices.append(float(candle[1]))
        high_prices.append(float(candle[2]))
        low_prices.append(float(candle[3]))
        close_prices.append(float(candle[4]))

        # Calculate the volume in USDT (close price * volume)
        volume_usdt = float(candle[5]) * float(candle[4])
        volumes.append(volume_usdt)
        
        # Calculate percentage difference between high and low prices
        percentage_difference = ((float(candle[2]) - float(candle[3])) / float(candle[3])) * 100
        percentage_differences.append(percentage_difference)
    
    # Calculate volatility as the standard deviation of the daily returns
    returns = [(close_prices[i + 1] - close_prices[i]) / close_prices[i] for i in range(len(close_prices) - 1)]
    # volatility = pd.Series(returns).std() * 100  # Convert to percentage

    # Format volumes to millions with commas and dollar signs
    formatted_volumes = [f"${volume / 1_000_000:.2f}M" for volume in volumes]
    
    # Create a pandas DataFrame
    df = pd.DataFrame({
        "Time (AEDT)": open_times,
        "Open Price": open_prices,
        "High Price": high_prices,
        "Low Price": low_prices,
        "Close Price": close_prices,
        "% Difference (High-Low)": percentage_differences,
        "Volume (USDT)": formatted_volumes
    })
    
    # Display the DataFrame in a table format
    print(df)
    # print(f"\nVolatility: {volatility:.2f}%")
    
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.22)
    
    # Reduced marker size
    marker_size = 5
    
    # Plot the price lines with reduced markers
    l_open, = ax1.plot(df["Time (AEDT)"], df["Open Price"], label="Open Price", marker="o", color='blue', linestyle='-', markersize=marker_size)
    l_high, = ax1.plot(df["Time (AEDT)"], df["High Price"], label="High Price", marker="^", color='green', linestyle='-', markersize=marker_size)
    l_low, = ax1.plot(df["Time (AEDT)"], df["Low Price"], label="Low Price", marker="v", color='red', linestyle='-', markersize=marker_size)
    l_close, = ax1.plot(df["Time (AEDT)"], df["Close Price"], label="Close Price", marker="x", color='black', linestyle='-', markersize=marker_size)
    
    # Second y-axis for % Difference
    ax2 = ax1.twinx()
    l_diff, = ax2.plot(df["Time (AEDT)"], df["% Difference (High-Low)"], label="% Difference (High-Low)", color="purple", linestyle="--", marker="d", markersize=marker_size)

    # Add a horizontal line at 5% on the percentage difference axis
    ax2.axhline(y=5, color='gray', linestyle='--', label='5% Threshold')
    
    # Rotate x-axis labels for better readability
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
    plt.xticks(rotation=45)
    
    # Add labels and title
    ax1.set_xlabel("Time (AEDT)")
    ax1.set_ylabel("Price (USDT)")
    ax2.set_ylabel("% Difference (High-Low)")
    plt.title(f"{params['symbol']} Daily Data over the Last 6 Months")
    
    # Add CheckButtons for toggling visibility of plots
    rax = plt.axes([0.85, 0.4, 0.1, 0.2])  # Position of the CheckButtons
    labels = ['Open Price', 'High Price', 'Low Price', 'Close Price', '% Difference (High-Low)']
    visibility = [l_open.get_visible(), l_high.get_visible(), l_low.get_visible(), l_close.get_visible(), l_diff.get_visible()]
    check = CheckButtons(rax, labels, visibility)
    
    def toggle_visibility(label):
        if label == 'Open Price':
            l_open.set_visible(not l_open.get_visible())
        elif label == 'High Price':
            l_high.set_visible(not l_high.get_visible())
        elif label == 'Low Price':
            l_low.set_visible(not l_low.get_visible())
        elif label == 'Close Price':
            l_close.set_visible(not l_close.get_visible())
        elif label == '% Difference (High-Low)':
            l_diff.set_visible(not l_diff.get_visible())
        plt.draw()
    
    check.on_clicked(toggle_visibility)
    
    # Adding slider for adjusting percentage difference range
    axcolor = 'lightgoldenrodyellow'
    axdiff = plt.axes([0.1, 0.01, 0.25, 0.03], facecolor=axcolor)  # Position and size of the % Difference slider

    # Extend the slider range slightly beyond the actual min and max values
    min_diff = min(percentage_differences) * 0.9
    max_diff = max(percentage_differences) * 1.1

    sdiff = Slider(axdiff, '% Diff', min_diff, max_diff, valinit=max(percentage_differences))

    def update(val):
        ax2.set_ylim(0, sdiff.val)
        fig.canvas.draw_idle()

    sdiff.on_changed(update)

    # Enable draggable axis
    plt.gca().set_xmargin(0)
    plt.gca().set_ymargin(0)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.22)
    
    # Show plot
    plt.tight_layout()
    plt.show()

else:
    print(f"Failed to retrieve data: {response.status_code}")
