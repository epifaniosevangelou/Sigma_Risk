import os
import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# Input parameters
historical_prices_path = "data/portfolio/all_historical_prices.csv"
test_stocks = ["AAPL", "TSLA", "AMZN"]
start_date = "2022-01-01"
end_date = "2023-01-01"

# Download stock data for a given ticker
def download_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data["Adj Close"]

# Read historical price data from CSV
all_prices_df = pd.read_csv(historical_prices_path, index_col="Date", parse_dates=True)

# Download and add stock data for each test stock
for stock in test_stocks:
    prices = download_stock_data(stock, start_date=start_date, end_date=end_date)
    all_prices_df[stock] = prices

# Calculate daily returns
returns_df = all_prices_df.pct_change(fill_method=None).dropna()

# Compute the correlation matrix
correlation_matrix = returns_df.corr()

# Get correlations of test stocks with other portfolio stocks
test_stock_correlation = correlation_matrix.loc[
    test_stocks, ~correlation_matrix.columns.isin(test_stocks)
]

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
    yticklabels=test_stocks,
    xticklabels=["Mean Correlation"],
)
plt.title("Average Correlation with Portfolio Stocks")
plt.savefig("outputs/Stock Reporting/correlation_average", bbox_inches="tight", dpi=400)
plt.close()

# Plot and save the detailed correlation heatmap
plt.figure(figsize=(12, 4))
sns.heatmap(
    test_stock_correlation,
    annot=False,
    cmap="coolwarm",
    fmt=".4f",
    linewidths=0.5,
    annot_kws={"size": 10},
    xticklabels=True,
    yticklabels=True,
)
plt.title("Correlation Heatmap of Potential Stocks with Portfolio Stocks")
plt.tight_layout()
plt.savefig("outputs/Stock Reporting/correlation_detailed", bbox_inches="tight", dpi=400)
plt.close()
