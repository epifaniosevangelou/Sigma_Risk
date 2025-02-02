import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
import os

# Inputs
tickers = ['MCK', 'ISRG', 'CAH']  # List of stock tickers to compare
benchmark = '^GSPC'
start_date = '2023-09-25'
end_date = '2024-09-25'
risk_free_rate_annual = 0.02  # Annual risk-free rate
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

# Calculate annualized Sharpe Ratio for each stock
sharpe_ratios = []
for ticker in tickers:  # Exclude the benchmark
    mean_daily_return = daily_returns[ticker].mean()
    std_daily_return = daily_returns[ticker].std()
    sharpe_ratio = (mean_daily_return - risk_free_rate_daily) / std_daily_return * np.sqrt(252)  # Annualize Sharpe ratio
    sharpe_ratios.append(sharpe_ratio)

# Plotting the Sharpe Ratios as a bar chart
bar_colors = ['#0D3580', '#AF0C15', '#0D7036']  # Colors for the bar chart
plt.rc('font', size=18)
plt.figure(figsize=(8, 6))
plt.bar(tickers, sharpe_ratios, color=bar_colors)
plt.xlabel('Ticker')
plt.ylabel('Sharpe Ratio')
plt.title('Sharpe Ratio')
plt.grid(axis='y')

# Save the bar chart to an output file
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "Sharpe Ratios"), bbox_inches='tight', dpi=400)



from sklearn.linear_model import LinearRegression

# Initialize lists to store Betas and Alphas
betas = []
alphas = []

# Calculate Beta and Alpha using linear regression for each stock
for ticker in tickers:
   # Fetch the benchmark (X) and stock (y) returns as 1D arrays
    X = daily_returns[benchmark].values  # Keep X as 1D for now
    y = daily_returns[ticker].values

    # Create a mask to filter out rows with NaN values in either X or y
    valid_mask = ~np.isnan(X) & ~np.isnan(y)

    # Apply the mask to filter out the NaN values in X and y
    X_valid = X[valid_mask]  # X is still 1D here
    y_valid = y[valid_mask]

    # Reshape X_valid for the linear regression (sklearn expects 2D input)
    X_valid = X_valid.reshape(-1, 1)  # Now reshape to 2D after filtering NaNs

    # Perform linear regression on the filtered data
    model = LinearRegression().fit(X_valid, y_valid)
    
    # The slope of the regression line is the Beta
    beta = model.coef_[0]
    betas.append(beta)
    
    # The intercept is the Alpha
    alpha = model.intercept_
    alphas.append(alpha)

# Plotting the Betas as a bar chart
plt.figure(figsize=(8, 6))
plt.bar(tickers, betas, color=bar_colors)
plt.xlabel('Ticker')
plt.ylabel('Beta')
plt.title('Beta Comparison')
plt.grid(axis='y')

# Save the Beta bar chart to an output file
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "Betas.png"), bbox_inches='tight', dpi=400)

# Plotting the Alphas as a bar chart
plt.figure(figsize=(8, 6))
plt.bar(tickers, alphas, color=bar_colors)
plt.xlabel('Ticker')
plt.ylabel('Alpha')
plt.title('Alpha Comparison')
plt.grid(axis='y')

# Save the Alpha bar chart to an output file
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "Alphas.png"), bbox_inches='tight', dpi=400)



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
plt.figure(figsize=(16, 8))
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
plt.savefig(os.path.join(output_dir, "Correlation Detailed.png"), bbox_inches="tight", dpi=400)
plt.close()