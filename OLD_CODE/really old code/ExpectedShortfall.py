# Import necessary libraries
import numpy as np
import pandas as pd
from scipy.stats import norm

# Set the time horizon, confidence level, and number of iterations for the ES calculation
time_horizon = 1
confidence_level = 0.95
iterations = 100

# Define the returns for each asset in the portfolio
asset_returns = [0.1, 0.2, 0.15, 0.05]

# Define the covariance matrix for the assets in the portfolio
covariance_matrix = [[0.05, 0.02, 0.03, 0.01],
                     [0.02, 0.09, 0.01, 0.04],
                     [0.03, 0.01, 0.08, 0.02],
                     [0.01, 0.04, 0.02, 0.07]]

# Generate random samples of returns for each asset
asset_samples = np.random.multivariate_normal(mean=asset_returns, cov=covariance_matrix, size=iterations)

# Calculate the portfolio return for each sample
portfolio_returns = asset_samples.mean(axis=1)

# Calculate the value at risk (VaR) for the portfolio
var = norm.ppf(1 - confidence_level, loc=portfolio_returns.mean(), scale=portfolio_returns.std())

# Calculate the expected shortfall (ES) for the portfolio
es = np.mean(portfolio_returns[portfolio_returns < var])

# Print the results
print(f'Value at risk (VaR) for the portfolio: {var:.2%}')
print(f'Expected shortfall (ES) for the portfolio: {es:.2%}')