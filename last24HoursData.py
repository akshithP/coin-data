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

# Calculate the timestamp for 24 hours ago from now in AEDT
now_aedt = datetime.now(aedt)
twenty_four_hours_ago_aedt = now_aedt - timedelta(hours=24)
start_timestamp = int(twenty_four_hours_ago_aedt.timestamp() * 1000)

# Parameters for the request to get hourly data
params = {
    "symbol": "BTCUSDT",  # Change this to the coin of your choice
    "interval": "1h",  # 1 hour interval for hourly data
    "startTime": start_timestamp,
    "limit": 24  # 24 data points for 24 hours
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
        
        # Calculate percentage difference between high and low prices
        percentage_difference = ((float(candle[2]) - float(candle[3])) / float(candle[3])) * 100
        percentage_differences.append(percentage_difference)
    
    # Create a pandas DataFrame
    df = pd.DataFrame({
        "Time (AEDT)": open_times,
        "Open Price": open_prices,
        "High Price": high_prices,
        "Low Price": low_prices,
        "Close Price": close_prices,
        "% Difference (High-Low)": percentage_differences
    })
    
    # Display the DataFrame in a table format
    print(df)
    
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.22)
    
    # Plot the price lines
    l_open, = ax1.plot(df["Time (AEDT)"], df["Open Price"], label="Open Price", marker="o", color='blue', linestyle='-')
    l_high, = ax1.plot(df["Time (AEDT)"], df["High Price"], label="High Price", marker="^", color='green', linestyle='-')
    l_low, = ax1.plot(df["Time (AEDT)"], df["Low Price"], label="Low Price", marker="v", color='red', linestyle='-')
    l_close, = ax1.plot(df["Time (AEDT)"], df["Close Price"], label="Close Price", marker="x", color='black', linestyle='-')
    
    # Second y-axis for % Difference
    ax2 = ax1.twinx()
    l_diff, = ax2.plot(df["Time (AEDT)"], df["% Difference (High-Low)"], label="% Difference (High-Low)", color="purple", linestyle="--")

    # Add a horizontal line at 5% on the percentage difference axis
    ax2.axhline(y=5, color='gray', linestyle='--', label='5% Threshold')
    
    # Rotate x-axis labels for better readability
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    
    # Add labels and title
    ax1.set_xlabel("Time (AEDT)")
    ax1.set_ylabel("Price (USDT)")
    ax2.set_ylabel("% Difference (High-Low)")
    plt.title("BTC/USDT Hourly Data over the Last 24 Hours")
    
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
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.05)
    
    # Show plot
    plt.tight_layout()
    plt.show()

else:
    print(f"Failed to retrieve data: {response.status_code}")
