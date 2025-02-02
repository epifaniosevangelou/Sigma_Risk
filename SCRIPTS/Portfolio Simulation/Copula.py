import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns
from sklearn.preprocessing import QuantileTransformer
from scipy.stats import norm
import matplotlib.pyplot as plt
from copulae import GaussianCopula

import warnings;

warnings.filterwarnings('ignore')

# Load the CSV file to read the tickers
historical_prices_path = '../../data/portfolio/historical_prices.csv'  # Update the path to your file location
historical_prices_df = pd.read_csv(historical_prices_path, nrows=1)
# We use .columns to get the column headers and then convert to a list
historical_tickers = historical_prices_df.columns.tolist()

# Since the first column is 'Date', we remove it to get only the tickers
historical_tickers.remove('Date')  # This modifies historical_tickers in-place
portfolio_tickers = historical_tickers  # Now portfolio_tickers is assigned the correct list

stock = "NOW"

# 1. Fetch real data
end_date = "2024-01-01"
start_date = "2020-01-01"
symbols = [stock] + portfolio_tickers
data = yf.download(symbols, start=start_date, end=end_date)["Adj Close"]

# Filter out the tickers that were not downloaded successfully
data = data.dropna(axis=1, how='all')  # This removes columns with all NaN values
portfolio_tickers = data.columns.drop(stock).tolist()  # Update the portfolio tickers to only include successful downloads


market_drop_percentage = -0.05

# 2. Compute daily returns
returns = data.pct_change().dropna()

# 3. Transform returns to [0,1] range using quantile transformation
quantile_transformers = {}
data_uniform = pd.DataFrame()

for symbol in returns.columns:
    qt = QuantileTransformer(output_distribution='uniform')
    data_uniform[symbol] = qt.fit_transform(returns[[symbol]]).flatten()
    quantile_transformers[symbol] = qt


# Define the function for conditional sampling
def conditional_sample(u1, rho, n_samples=1000):
    u2 = np.linspace(0.001, 0.999, n_samples)
    return u2, norm.cdf((norm.ppf(u1) - rho * norm.ppf(u2)) / np.sqrt(1 - rho ** 2))


# Simulation for each stock in the portfolio
results = {}
for ticker in portfolio_tickers:
    index_drop = quantile_transformers[stock].transform(np.array([[market_drop_percentage]]))[0][0]

    # Bivariate assumption with ticker and each stock
    bi_data = data_uniform[[stock, ticker]]
    bi_copula = GaussianCopula(dim=2)
    bi_copula.fit(bi_data.values)
    rho = bi_copula.params[0]

    conditional_u2, conditional_cdf = conditional_sample(index_drop, rho)
    conditional_returns = quantile_transformers[ticker].inverse_transform(conditional_cdf.reshape(-1, 1)).flatten()
    results[ticker] = conditional_returns

print("Downloaded tickers:", symbols)
print("Downloaded data:")
print(data)

'''
# Visualization for each stock in the portfolio
# Comment it out to see the impact to each stock in portfolio
for ticker, conditional_returns in results.items():
    fig, ax = plt.subplots(2, 2, figsize=(25, 10))
    last_known_price = data[ticker].iloc[-1]
    min_return = np.min(conditional_returns)
    max_return = np.max(conditional_returns)
    mean_return = np.mean(conditional_returns)

    final_min_price = last_known_price * (1 + min_return)
    final_max_price = last_known_price * (1 + max_return)
    final_mean_price = last_known_price * (1 + mean_return)

    simulated_dates = pd.date_range(start=data.index[-1], periods=31, freq='D')[1:]

    min_price_trajectory = [last_known_price] + [final_min_price] * (len(simulated_dates) - 1)
    max_price_trajectory = [last_known_price] + [final_max_price] * (len(simulated_dates) - 1)
    mean_price_trajectory = [last_known_price] + [final_mean_price] * (len(simulated_dates) - 1)

    # Plot 1: Histogram of Simulated Returns
    ax[0, 0].hist(conditional_returns, bins=50, edgecolor='k', alpha=0.7)
    ax[0, 0].set_title(f"Simulated {ticker} Returns given 10% drop in S&P 500")
    ax[0, 0].set_xlabel("Returns")
    ax[0, 0].set_ylabel("Frequency")

    # Plot 2: CDF of Simulated Returns
    ax[0, 1].hist(conditional_returns, bins=100, density=True, cumulative=True, alpha=0.7)
    ax[0, 1].set_title('CDF of Simulated Returns')

    # Plot 3: KDE of Simulated Returns
    sns.kdeplot(conditional_returns, shade=True, ax=ax[1, 0])
    ax[1, 0].set_title('KDE of Simulated Returns')

    # Plot 4: Ticker Original vs. Worst, Best, and Mean Case Scenarios
    data[ticker].plot(ax=ax[1, 1], label="Original Prices")
    pd.Series(min_price_trajectory, index=simulated_dates).plot(ax=ax[1, 1], label="Worst-Case Scenario", linestyle='--', color="red")
    pd.Series(max_price_trajectory, index=simulated_dates).plot(ax=ax[1, 1], label="Best-Case Scenario", linestyle='--', color="green")
    pd.Series(mean_price_trajectory, index=simulated_dates).plot(ax=ax[1, 1], label="Mean Scenario", linestyle='--', color="blue")

    label_x_position = simulated_dates[-10]
    ax[1, 1].annotate(f"{min_return*100:.2f}% (Worst Scenario)", (label_x_position, final_min_price * 0.98), fontsize=12, ha="left", color="red")
    ax[1, 1].annotate(f"{max_return*100:.2f}% (Best Scenario)", (label_x_position, final_max_price * 1.02), fontsize=12, ha="left", color="green")
    ax[1, 1].annotate(f"{mean_return*100:.2f}% (Mean Scenario)", (label_x_position, final_mean_price), fontsize=12, ha="left", color="blue")

    ax[1, 1].set_title(f"{ticker} Original vs. Worst, Best and Mean Case Scenarios")
    ax[1, 1].legend()

    plt.tight_layout()
    plt.show()
'''
# Compute portfolio returns from individual stock returns
portfolio_returns = np.mean(np.array([results[ticker] for ticker in portfolio_tickers]), axis=0)

# Visualization for the Portfolio
fig, ax = plt.subplots(2, 2, figsize=(25, 10))
fig.subplots_adjust(wspace=50.0, hspace=20.0)
last_known_prices = data[portfolio_tickers].iloc[-1]
portfolio_last_known_price = np.mean(last_known_prices)  # Equally weighted

min_return = np.min(portfolio_returns)
max_return = np.max(portfolio_returns)
mean_return = np.mean(portfolio_returns)

final_min_price = portfolio_last_known_price * (1 + min_return)
final_max_price = portfolio_last_known_price * (1 + max_return)
final_mean_price = portfolio_last_known_price * (1 + mean_return)

simulated_dates = pd.date_range(start=data.index[-1], periods=31, freq='D')[1:]

min_price_trajectory = [portfolio_last_known_price] + [final_min_price] * (len(simulated_dates) - 1)
max_price_trajectory = [portfolio_last_known_price] + [final_max_price] * (len(simulated_dates) - 1)
mean_price_trajectory = [portfolio_last_known_price] + [final_mean_price] * (len(simulated_dates) - 1)

# Plot 1: Histogram of Simulated Returns
ax[0, 0].hist(portfolio_returns, bins=50, edgecolor='k', alpha=0.7)
ax[0, 0].set_title(f"Simulated Portfolio Returns given {market_drop_percentage * 100:.2f}% drop in " + stock,
                   fontsize=15)
ax[0, 0].set_xlabel("Returns")
ax[0, 0].set_ylabel("Frequency")

# Plot 2: CDF of Simulated Returns
ax[0, 1].hist(portfolio_returns, bins=100, density=True, cumulative=True, alpha=0.7)
ax[0, 1].set_title('CDF of Simulated Portfolio Returns', fontsize=15)

# Plot 3: KDE of Simulated Returns
sns.kdeplot(portfolio_returns, shade=True, ax=ax[1, 0])
ax[1, 0].set_title('KDE of Simulated Portfolio Returns', fontsize=15)

# Plot 4: Portfolio Original vs. Worst, Best, and Mean Case Scenarios
portfolio_prices = data[portfolio_tickers].mean(axis=1)
portfolio_prices.plot(ax=ax[1, 1], label="Original Prices")
pd.Series(min_price_trajectory, index=simulated_dates).plot(ax=ax[1, 1], label="Worst-Case Scenario", linestyle='--',
                                                            color="red")
pd.Series(max_price_trajectory, index=simulated_dates).plot(ax=ax[1, 1], label="Best-Case Scenario", linestyle='--',
                                                            color="green")
pd.Series(mean_price_trajectory, index=simulated_dates).plot(ax=ax[1, 1], label="Mean Scenario", linestyle='--',
                                                             color="blue")

label_x_position = simulated_dates[-10]
ax[1, 1].annotate(f"{min_return * 100:.2f}%", (label_x_position, final_min_price * 0.9), fontsize=10,
                  ha="left", color="red")
ax[1, 1].annotate(f"{max_return * 100:.2f}%", (label_x_position, final_max_price * 1.05), fontsize=10,
                  ha="left", color="green")
ax[1, 1].annotate(f"{mean_return * 100:.2f}%", (label_x_position, final_mean_price), fontsize=10,
                  ha="left", color="blue")

ax[1, 1].set_title(f"Portfolio Original vs. Worst, Best, and Mean Case Scenarios", fontsize=15)
ax[1, 1].legend()

# General configurations for the plot aesthetics
sns.set_style("whitegrid")
plt.tight_layout()
plt.show()

print(f'The average scenario given a {market_drop_percentage * 100:.2f}% change in ' + stock + ' is a', f"{mean_return * 100:.2f}% change in portfolio returns.")
print(f'The worst-case scenario given a {market_drop_percentage * 100:.2f}% change in ' + stock + ' is a', f"{min_return * 100:.2f}% change in portfolio returns.")
print(f'The best-case scenario given a {market_drop_percentage * 100:.2f}% change in ' + stock + ' is a', f"{max_return * 100:.2f}% change in portfolio returns.")
