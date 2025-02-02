import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load historical stock data from a CSV file
file_path = "../../data/portfolio/historical_prices.csv"
data = pd.read_csv(file_path, index_col='Date', parse_dates=True)

# Define the portfolio weights (e.g., 30% AAPL, 40% MSFT, 10% GOOGL, 10% AMZN, 10% FB)
assets = ['AD.AS', 'HEIA.AS', 'LOW', 'TGT', 'PM', 'ALV.DE', 'BRK-B', 'SPGI', 'KKR', 'CME', 'LSEG.L', 'EQIX', 'AED.BR', 'AMT', 'MDT', 'BAYN.DE', 'UNH', 'LH', 'REGN', 'IDXX', 'NOVO-B.CO', 'HCA', 'DHL.DE', 'CMI', 'EOAN.DE', 'AMAT', 'CRG.IR', 'APD', 'LPX', 'DTE', 'ASML', 'NFLX', 'ETN', 'SAPA', 'TCEHY', '992', 'SONY', 'META', 'DELL']
portfolio_weights = [0.0254, 0.0223, 0.0132, 0.017, 0.0493, 0.0202, 0.0075, 0.0394, 0.0218, 0.0209, 0.0359, 0.0459, 0.0216, 0.0144, 0.0167, 0.0233, 0.0097, 0.0332, 0.0169, 0.0093, 0.0113, 0.0309, 0.0076, 0.0143, 0.0254, 0.0139, 0.0107, 0.0303, 0.0152]
num_assets = len(portfolio_weights)
# Define parameters for the Monte Carlo simulation
num_simulations = 1000
time_horizon = 252  # Trading days in a year
initial_portfolio_value = 1000000  # $1,000,000 initial investment
risk_free_rate = 0.03  # Assumed annual risk-free rate
dividend_yield = 0.02  # Assumed average annual dividend yield
volatility = 0.2  # Assumed annual portfolio volatility (20%)

# Calculate daily returns from historical data
daily_returns = data.pct_change().dropna()

# Calculate the mean and standard deviation of daily returns for each stock
mean_returns = daily_returns.mean()
std_returns = daily_returns.std()

# Perform Monte Carlo simulations
# Create an empty DataFrame to store simulation results
simulation_results = pd.DataFrame()

portfolio_returns = []
portfolio_risks = []
for i in range(num_simulations):
    sim_returns = []
    for j in range(num_assets):
        sim_return = np.random.normal(data[assets[j]].mean(),
                                       data[assets[j]].std())
        sim_returns.append(sim_return)
    portfolio_return = np.dot(portfolio_weights, sim_returns)
    portfolio_returns.append(portfolio_return)
    portfolio_risk = np.sqrt(np.dot(portfolio_weights.T, np.dot(data.cov(), portfolio_weights)))
    portfolio_risks.append(portfolio_risk)

# Plot results
plt.scatter(portfolio_risks, portfolio_returns)
plt.xlabel('Risk')
plt.ylabel('Expected Return')
plt.title('Efficient Frontier')

# Append the simulation results to a temporary DataFrame
temp_df = pd.DataFrame({f'Simulation_{i + 1}': portfolio_weights})

# Concatenate the temporary DataFrame with the main simulation_results
simulation_results = pd.concat([simulation_results, temp_df], axis=1)


# Plot the Monte Carlo simulation results
plt.figure(figsize=(12, 6))
plt.plot(simulation_results, lw=0.5, alpha=0.5)
plt.xlabel('Trading Days')
plt.ylabel('Portfolio Value')
plt.title('Monte Carlo Simulation of Portfolio Value')
plt.grid(True)
plt.show()

# Calculate summary statistics of the simulation results
portfolio_returns = simulation_results.pct_change().dropna()
mean_portfolio_return = portfolio_returns.mean().mean()
std_portfolio_return = portfolio_returns.std().mean()
max_portfolio_value = simulation_results.max().max()
min_portfolio_value = simulation_results.min().min()

print(f"Mean Portfolio Return: {mean_portfolio_return:.4f}")
print(f"Std Portfolio Return: {std_portfolio_return:.4f}")
print(f"Maximum Portfolio Value: ${max_portfolio_value:.2f}")
print(f"Minimum Portfolio Value: ${min_portfolio_value:.2f}")

# Calculate additional risk metrics
percentile_5th = simulation_results.iloc[-1].quantile(0.05)
percentile_95th = simulation_results.iloc[-1].quantile(0.95)

print(f"5th Percentile Portfolio Value: ${percentile_5th:.2f}")
print(f"95th Percentile Portfolio Value: ${percentile_95th:.2f}")
