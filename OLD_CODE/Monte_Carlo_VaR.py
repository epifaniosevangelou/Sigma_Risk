import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "data/portfolio/historical_prices.csv"
stock_prices = pd.read_csv(file_path, index_col="Date", parse_dates=True)

#Fill Non-leading NA values and calculate daily returns
stock_prices_filled = stock_prices.fillna(method='ffill').fillna(method='bfill')
daily_returns = stock_prices_filled.pct_change().dropna()

# Load portfolio weights
weights_file_path = "data/portfolio/historical_prices.csv"
weight_column_name = "Weight in a Portfolio"
weights_data = pd.read_csv(file_path, index_col="Date", parse_dates=True)

data = pd.read_csv(file_path, sep = ";")
if weight_column_name in data.columns:
        # Replace commas with dots and convert to float
        weights = weights_data[weight_column_name].str.replace(',', '.').astype(float).values
else:
        raise ValueError(f"Column '{weight_column_name}' not found in the file.")

# if weight_column_name in weights_data.columns:
#         # Replace commas with dots and convert to float
#         weights = weights_data[weight_column_name].str.replace(',', '.').astype(float).values
# else:
#          raise ValueError(f"Column '{weight_column_name}' not found in the file.")

#Perform Monte Carlo Simulations
n_simulations = 10000
time_horizon=365*2, # Daily time horizon as we use daily returns
samples = daily_returns.sample(n=n_simulations*time_horizon, replace=True).values
samples = samples.reshape(n_simulations, time_horizon, -1)
simulated_daily_returns = np.sum(samples * weights, axis=2)
portfolio_simulations = np.prod(1 + simulated_daily_returns, axis=1) - 1

#Calculate Value at Risk (VaR)
alpha = 0.05
VaR= np.percentile(portfolio_simulations, alpha * 100)
print(f"Value at Risk (VaR) at {(1 - alpha) * 100}% confidence level: {VaR*100:.2f}%")

#Plotting
plt.figure(figsize=(10, 6))
plt.hist(portfolio_simulations, bins=100, alpha=0.75, color='blue', label='Simulated Returns')

# Highlight the 5% lowest outcomes
critical_value = np.percentile(portfolio_simulations, 5)
# Filter values that are less than the critical value
worst_cases = portfolio_simulations[portfolio_simulations <= critical_value]
plt.hist(worst_cases, bins=100, alpha=0.75, color='red', label='Worst 5% Outcomes')

plt.axvline(VaR, color="red", linestyle="dashed", linewidth=2, label='VaR at 95% Confidence Level')
plt.xlabel("Portfolio Return")
plt.ylabel("Frequency")
plt.title("Distribution of Simulated Portfolio Returns with VaR Highlight")
plt.legend()

output_path = "scripts/Step_3_Outputs/portfolio_simulation_plot.png"
plt.savefig(output_path, bbox_inches="tight", pad_inches=0.2)
plt.close()

print(weights_data.columns)

# def load_stock_prices(file_path):
#     """
#     Load historical stock prices from a CSV file.
#     """
#     return pd.read_csv(file_path, index_col="Date", parse_dates=True)


# def calculate_daily_returns(stock_prices):
#     """
#     Calculate daily returns from stock prices, handling NaN values appropriately.
#     """
#     # Fill non-leading NA values to avoid issues with pct_change()
#     stock_prices_filled = stock_prices.fillna(method='ffill').fillna(method='bfill')
#     return stock_prices_filled.pct_change().dropna()

# def load_weights(file_path, weight_column_name='Weight in Portofolio '):
#     """
#     Load portfolio weights from a specific column in a CSV file.
    
#     Args:
#     file_path (str): Path to the CSV file containing portfolio weights.
#     weight_column_name (str): The column name where weights are stored.
    
#     Returns:
#     numpy.ndarray: Array of weights.
#     """
#     # Load the entire CSV into a DataFrame
#     data = pd.read_csv(file_path, sep = ";")
#     if weight_column_name in data.columns:
#         # Replace commas with dots and convert to float
#         weights = data[weight_column_name].str.replace(',', '.').astype(float).values
#     else:
#         raise ValueError(f"Column '{weight_column_name}' not found in the file.")
    
#     return weights
# def perform_monte_carlo_simulation(
#     daily_returns, weights, n_simulations=10000, time_horizon=3
# ):
#     """
#     Perform Monte Carlo simulations using vectorized operations.
#     """
#     samples = daily_returns.sample(n=n_simulations*time_horizon, replace=True).values
#     samples = samples.reshape(n_simulations, time_horizon, -1)
#     simulated_daily_returns = np.sum(samples * weights, axis=2)
#     portfolio_simulations = np.prod(1 + simulated_daily_returns, axis=1) - 1
#     return portfolio_simulations
    

# def calculate_var(portfolio_simulations, alpha =0.05):
#     """
#     Calculate the Value at Risk (VaR) from portfolio simulations.
#     """
#     return np.percentile(portfolio_simulations, alpha * 100)


# def plot_simulation_results(portfolio_simulations, VaR, output_path):
#     """
#     Plot the distribution of simulated portfolio returns and save the figure.
#     Highlights the 5% lowest outcomes to illustrate the Value at Risk (VaR).
#     """
#     plt.figure(figsize=(10, 6))
#     # Histogram of all simulations
#     plt.hist(portfolio_simulations, bins=100, alpha=0.75, color='blue', label='Simulated Returns')

#     # Highlight the 5% lowest outcomes
#     critical_value = np.percentile(portfolio_simulations, 5)
#     # Filter values that are less than the critical value
#     worst_cases = portfolio_simulations[portfolio_simulations <= critical_value]
#     plt.hist(worst_cases, bins=100, alpha=0.75, color='red', label='Worst 5% Outcomes')

#     plt.axvline(VaR, color="red", linestyle="dashed", linewidth=2, label='VaR at 95% Confidence Level')
#     plt.xlabel("Portfolio Return")
#     plt.ylabel("Frequency")
#     plt.title("Distribution of Simulated Portfolio Returns with VaR Highlight")
#     plt.legend()
#     plt.savefig(output_path, bbox_inches="tight", pad_inches=0.2)
#     plt.close()
# def run_monte_carlo_analysis(
#     file_path,
#     weights_file_path,
#     weight_column_name,  # Added this parameter to specify the column name
#     n_simulations=10000,
#     time_horizon=365*2, # Daily time horizon as we use daily returns
#     alpha=0.05,
#     output_path="scripts/Step_3_Outputs/portfolio_simulation_plot.png",
# ):
#     stock_prices = load_stock_prices(file_path)
#     weights = load_weights(weights_file_path, weight_column_name)
#     daily_returns = calculate_daily_returns(stock_prices)
#     portfolio_simulations = perform_monte_carlo_simulation(
#         daily_returns, weights, n_simulations, time_horizon
#     )
#     VaR = calculate_var(portfolio_simulations, alpha)
#     print(
#         f"Value at Risk (VaR) at {(1 - alpha) * 100}% confidence level: {VaR*100:.2f}%"
#     )
#     plot_simulation_results(portfolio_simulations, VaR, output_path)
    
# if __name__ == "__main__":
#     file_path = "data/portfolio/historical_prices.csv"
#     weights_file_path = "data/portfolio/All_Sectors.csv"
#     weights_column = "Weight in Portofolio "  # Replace with your actual column name for weights
#     run_monte_carlo_analysis(file_path, weights_file_path, weights_column)

# ""