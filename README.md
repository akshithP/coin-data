# Coin Data Analyser

There are 2 scripts currently with the following functionality:


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
git clone https://github.com/yourusername/crypto-coin-analysis.git
cd crypto-coin-analysis
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
### 4. Volatility (6 months)
1. Description: Volatility measures how much the coin's price fluctuates daily over the last 6 months. It's calculated as the standard deviation of daily returns.
2. Usefulness: Volatility is a key indicator of risk. Higher volatility means more price swings, which can lead to higher profits or losses. Lower volatility indicates more stable price movement.
3. Example:
- Low Volatility (< 5%): The coin's price is relatively stable, with smaller price swings. Suitable for long-term investors.
- Moderate Volatility (5% - 15%): The coin's price has moderate fluctuations, offering a balance between risk and reward.
- High Volatility (> 15%): The coin's price fluctuates significantly, offering high-profit potential but also higher risk. Suitable for experienced traders.
- If the volatility is 10%, it means that the coin's price typically moves by 10% from the average return each day. If you bought a coin at $100, a 10% volatility suggests that the price might swing between $90 and $110 in the short term.
