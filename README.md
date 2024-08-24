# Coin Data Analyser

There are 3 scripts currently with the following functionality:

### last24hours.py
Analyzes hourly trading data for a specific cryptocurrency over the last 24 hours. Plots open, close, high, low prices, and percentage difference. Includes an interactive slider for percentage difference and toggles for plot visibility.

### last6MonthsData.py
Fetches daily trading data for a single cryptocurrency over the last 6 months. Plots prices and percentage difference with markers, formats volume in USDT, calculates volatility, and provides toggles for plot visibility.

### allCoinHistory2.py
Analyzes top 50 cryptocurrencies on Binance over the last 6 months. Calculates average percentage difference, volume in USDT, and volatility. Exports results to Excel and includes plot visibility toggles.

## **allCoinDataHistory.py**
This script fetches and analyzes cryptocurrency data from Binance, focusing on metrics like percentage difference, trading volume, and volatility over different 6 months (180 days). The results are printed in the console and exported to an Excel file.

### Features
1. Fetches data for top coins on Binance with High % difference (High - low)
2. Calculates average percentage difference for both the last 6 months and 30 days.
3. Calculates average trading volume in USDT over the last 180 days.
4. Calculates the volatility of the coin over the last 6 months.
5. Exports the results to an Excel file with proper formatting.

### Installation
1. Clone the repository:
```
git clone https://github.com/akshithP/coin-data.git
```
```
cd crypto-coin-analysis
```
2. Set Up a Virtual Environment:
```
python -m venv venv
```
2. Install the required dependencies: 
```
pip install -r requirements.txt
```

## Fields Explained
### 1. Average % Difference (High-Low) - 6 months
This field represents the average percentage difference between the highest and lowest prices for the coin over the last 6 months.

### 2. Average Volume (180 days)
This field shows the average trading volume of the coin in USDT over the last 180 days. High trading volume indicates strong interest and liquidity, making it easier to buy or sell the coin without affecting the price significantly.
### 3. Current Volume (24H)
This field represents the total trading volume of the coin in USDT over the last 24 hours. It provides a snapshot of recent trading activity, which can indicate current market interest and momentum.

