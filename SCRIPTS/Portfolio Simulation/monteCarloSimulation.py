import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the historical prices CSV file into a DataFrame
historical_prices_path = 'data/portfolio/all_historical_prices.csv'
historical_prices_df = pd.read_csv(historical_prices_path, sep=',')

# Calculate daily returns for each stock
# Since we're interested in the returns, we will drop the 'Date' column
historical_returns = historical_prices_df.drop(columns='Date').pct_change()

# Calculate mean returns and volatilities for each stock
mean_daily_returns = historical_returns.mean()
volatilities = historical_returns.std()

# Load the portfolio weights into a DataFrame
portfolio_path = 'data/portfolio/All_Sectors.csv'
portfolio_df = pd.read_csv(portfolio_path, sep=';', decimal=',')
weights_df = portfolio_df[['Ticker', 'Weight in Portofolio ']].copy()
weights_df.columns = ['Ticker', 'Weight']  # Renaming for clarity
weights_df['Weight'] /= weights_df['Weight'].sum()  # Normalizing the weights so they sum to 1

# Define the parameters for the Monte Carlo simulation
num_simulations = 1000
time_horizon = 252  # Trading days in a year
initial_portfolio_value = 1000000  # $1,000,000 initial investment
risk_free_rate = 0.03  # Assumed annual risk-free rate
dividend_yield = 0.02  # Assumed average annual dividend yield

# Assuming historical average daily returns and volatilities for the stocks
weights = weights_df['Weight'].values
mean_daily_returns = mean_daily_returns.values
volatilities = volatilities.values

# Initialize an array to hold the simulation results
portfolio_values = np.zeros((num_simulations, time_horizon))

# Run the Monte Carlo simulation
for i in range(num_simulations):
    # Generate the random daily returns for each stock
    daily_returns = np.random.normal(mean_daily_returns, volatilities, (time_horizon, len(mean_daily_returns)))
    # Adjust for risk free rate and dividend yield
    daily_returns = daily_returns - risk_free_rate / 252 + dividend_yield / 252
    # Calculate the daily returns of the portfolio
    daily_portfolio_returns = np.sum(daily_returns * weights, axis=1)
    # Calculate the cumulative returns
    cumulative_portfolio_returns = np.cumprod(1 + daily_portfolio_returns) * initial_portfolio_value
    # Store the results
    portfolio_values[i] = cumulative_portfolio_returns

# Plot the results
plt.figure(figsize=(14, 7))
for i in range(num_simulations):
    plt.plot(portfolio_values[i], lw=1, alpha=0.2)
plt.title('Monte Carlo Simulations of Portfolio Value')
plt.xlabel('Days')
plt.ylabel('Portfolio Value')
plt.axhline(y=initial_portfolio_value, color='r', linestyle='-', lw=2)
save_path = (
    "scripts/3_Outputs/monte_carlo_simulations.png"  # Update the path accordingly
)
plt.savefig(save_path)
plt.show()

# Additional Analysis
# Calculating the final portfolio statistics
final_values = portfolio_values[:, -1]
mean_final_value = final_values.mean()
median_final_value = np.median(final_values)
min_final_value = final_values.min()
max_final_value = final_values.max()

# Printing the summary statistics
print(f"Mean final portfolio value: ${mean_final_value:,.2f}")
print(f"Median final portfolio value: ${median_final_value:,.2f}")
print(f"Minimum final portfolio value: ${min_final_value:,.2f}")
print(f"Maximum final portfolio value: ${max_final_value:,.2f}")

# Standard deviation (risk) and the Sharpe ratio
std_dev = final_values.std()
sharpe_ratio = (mean_final_value - initial_portfolio_value) / std_dev

print(f"Standard deviation (Risk): ${std_dev:,.2f}")
print(f"Sharpe ratio: {sharpe_ratio:.2f}")

# Plotting a histogram of the final portfolio values to visualize the distribution
plt.figure(figsize=(14, 7))
plt.hist(final_values, bins=50, alpha=0.75)
plt.title('Distribution of Final Portfolio Values')
plt.axvline(mean_final_value, color='r', linestyle='dashed', linewidth=2)
plt.axvline(median_final_value, color='g', linestyle='dashed', linewidth=2)
plt.xlabel('Final Portfolio Value')
plt.ylabel('Frequency')
save_path = "scripts/3_Outputs/final_portfolio_distribution.png"  # Update the path accordingly
plt.savefig(save_path)
plt.show()

# Generating a cumulative returns graph for the median simulation
median_simulation = portfolio_values[np.argsort(final_values)[num_simulations // 2]]

plt.figure(figsize=(14, 7))
plt.plot(median_simulation, lw=2, alpha=0.75, label='Median Simulation')
plt.title('Cumulative Returns of Median Simulation')
plt.xlabel('Days')
plt.ylabel('Portfolio Value')
plt.axhline(y=initial_portfolio_value, color='r', linestyle='-', lw=2)
plt.legend()
save_path = "scripts/3_Outputs/median_simulation_cumulative_returns.png"  # Update the path accordingly
plt.savefig(save_path)
plt.show()
