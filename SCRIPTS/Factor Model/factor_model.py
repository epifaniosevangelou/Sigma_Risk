import numpy as np
import pandas as pd
import statsmodels.api as sm

# Load portfolio data from a CSV file
file_path1 = "../../data/portfolio/portfolio_returns.csv"
portfolio_data = pd.read_csv(file_path1, index_col='Date', parse_dates=True)

# Load factor data from a CSV file
factor_returns = pd.read_csv('factor_returns.csv', index_col='Date', parse_dates=True)

# Ensure the portfolio data and factor data have the same date index
common_dates = portfolio_data.index.intersection(factor_returns.index)
portfolio_data = portfolio_data.loc[common_dates]
factor_returns = factor_returns.loc[common_dates]

# Perform factor model regression
X = sm.add_constant(factor_returns)
factor_model = sm.OLS(portfolio_data.values, X).fit()

# Get factor exposures (loadings)
factor_exposures = factor_model.params[:-1]

# Predicted returns based on factor model
predicted_returns = np.dot(X, factor_model.params)

# Residual returns
residual_returns = portfolio_data - predicted_returns

# Factor covariance matrix
factor_covariance_matrix = np.cov(factor_returns, rowvar=False)

# Factor correlation matrix
factor_correlation_matrix = np.corrcoef(factor_returns, rowvar=False)

# Factor risk contributions
factor_risk_contributions = np.dot(factor_exposures ** 2, factor_covariance_matrix)

# Factor covariance contributions
factor_cov_contributions = factor_exposures[:, np.newaxis] * factor_exposures * factor_covariance_matrix

# Print results
print("Factor Exposures:")
print(factor_exposures)

print("\nPredicted Returns:")
print(predicted_returns)

print("\nResidual Returns:")
print(residual_returns)

print("\nFactor Covariance Matrix:")
print(factor_covariance_matrix)

print("\nFactor Correlation Matrix:")
print(factor_correlation_matrix)

print("\nFactor Risk Contributions:")
print(factor_risk_contributions)

print("\nFactor Covariance Contributions:")
print(factor_cov_contributions)