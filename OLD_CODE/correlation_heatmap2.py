import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy

# Load the historical price data from your CSV
portfolio_data = pd.read_csv('data/portfolio/all_historical_prices.csv')

# Convert the Date column to datetime format (tz-naive)
portfolio_data['Date'] = pd.to_datetime(portfolio_data['Date'])
portfolio_data.set_index('Date', inplace=True)

# Define the test stocks and date range
test_stocks = ["AAPL", "TSLA", "AMZN"]
start_date = "2022-01-01"
end_date = "2023-01-01"

# Fetch data for the test stocks from yfinance
test_stocks_data = yf.download(test_stocks, start=start_date, end=end_date)['Adj Close']

# Convert the yfinance data index to tz-naive to match the portfolio data
test_stocks_data.index = test_stocks_data.index.tz_localize(None)

# Filter the portfolio data for the specified date range
portfolio_filtered = portfolio_data[(portfolio_data.index >= start_date) & (portfolio_data.index <= end_date)]

# Merge the test stock data with the portfolio data by aligning on the date index
combined_data = pd.concat([portfolio_filtered, test_stocks_data], axis=1)

# Calculate the correlation matrix for all stocks
correlation_matrix = combined_data.corr()

# Extract the correlation of the test stocks with all other stocks (but not the correlation between test stocks)
selected_stocks = test_stocks + portfolio_filtered.columns.tolist()  # All stocks in portfolio + selected stocks
correlation_matrix_filtered = correlation_matrix.loc[test_stocks, portfolio_filtered.columns]
cor_matrix=correlation_matrix_filtered.T

# Plot the heatmap using seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(cor_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation of Test Stocks with Portfolio')
plt.show()
