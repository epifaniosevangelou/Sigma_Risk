import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
import os

# Inputs
tickers = ['ROP', '^GSPC','FIDU']  # List of stock tickers to compare
benchmark = '^GSPC'
start_date = '2023-11-08'
end_date = '2024-11-08'
risk_free_rate_annual = 0.04  # Annual risk-free rate
output_dir = "outputs/Reporting/Stock Comparison"
historical_prices_path = "data/portfolio/all_historical_prices.csv"

# Convert the annual risk-free rate to a daily risk-free rate
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# Fetch historical data using yfinance for each ticker
all_tickers = tickers + [benchmark]
stock_data = {}
for ticker in all_tickers:
    stock_data[ticker] = yf.download(ticker, start=start_date, end=end_date)['Adj Close'].ffill()

# Calculate daily returns for each stock
daily_returns = pd.DataFrame()
for ticker in all_tickers:
    daily_returns[ticker] = stock_data[ticker].pct_change().dropna()



import seaborn as sns

# Assuming the CSV has a 'Date' column that we can use to merge on
portfolio_prices_df = pd.read_csv(historical_prices_path, index_col="Date", parse_dates=True, sep=";")

# Ensure that the CSV file has matching dates to the stock data we've downloaded
# Align the dates by taking only the overlapping date range
portfolio_prices_df = portfolio_prices_df.loc[portfolio_prices_df.index.intersection(daily_returns.index)]

# Recalculate daily returns for the portfolio stocks (from the CSV)
portfolio_returns_df = portfolio_prices_df.pct_change(fill_method=None).dropna()

# Merge the test stock returns with the portfolio returns from the CSV
combined_returns_df = pd.concat([daily_returns[tickers], portfolio_returns_df], axis=1).dropna()

# Compute the correlation matrix for the combined returns (test stocks vs portfolio)
correlation_matrix = combined_returns_df.corr()

# Get correlations of test stocks with other portfolio stocks (exclude the test stocks themselves)
test_stock_correlation = correlation_matrix.loc[tickers, portfolio_returns_df.columns]

# Calculate the average correlation of test stocks with the portfolio
average_correlation_with_portfolio = test_stock_correlation.mean(axis=1)

# Plot and save the average correlation heatmap
plt.figure(figsize=(7, 4))
sns.heatmap(
    pd.DataFrame(average_correlation_with_portfolio, columns=["Mean"]),
    annot=True,
    cmap="rocket",
    fmt=".4f",
    square=True,
    linewidths=0.5,
    cbar=False,
    annot_kws={"size": 11},
    yticklabels=tickers,
    xticklabels=["Mean Correlation"],
)
plt.title("Average Correlation with Portfolio Stocks")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the average correlation heatmap
plt.savefig(os.path.join(output_dir, "Correlation_Average.png"), bbox_inches="tight", dpi=400)
plt.close()

# Plot and save the detailed correlation heatmap
plt.figure(figsize=(10, 5))
sns.heatmap(
    test_stock_correlation,
    annot=False,
    cmap="coolwarm",
    fmt=".4f",
    linewidths=0.5,
    annot_kws={"size": 14},
    xticklabels=True,
    yticklabels=True,
)
plt.title("Correlation Heatmap with Portfolio Stocks")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "Correlation Detailed.png"), bbox_inches="tight", dpi=400)
plt.close()