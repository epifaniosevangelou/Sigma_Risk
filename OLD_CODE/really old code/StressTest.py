# Import the necessary libraries
import numpy as np
import pandas as pd


# Define a function to calculate the stress test scenario
def stress_test_scenario(portfolio, scenario):
    # Create a copy of the portfolio to avoid modifying the original
    portfolio_copy = portfolio.copy()

    # Apply the scenario to each asset in the portfolio
    for asset, weight in portfolio_copy.items():
        portfolio_copy[asset] = weight * scenario

    # Return the stressed portfolio
    return portfolio_copy


# Define a function to calculate the risk of a portfolio
def portfolio_risk(portfolio, returns):
    # Calculate the weighted returns of the portfolio
    weighted_returns = returns.mul(portfolio, axis=1)

    # Calculate the covariance matrix of the portfolio
    cov_matrix = weighted_returns.cov()

    # Calculate the portfolio variance
    portfolio_variance = (portfolio * cov_matrix * portfolio.T).sum()

    # Calculate the portfolio standard deviation (risk)
    portfolio_risk = np.sqrt(portfolio_variance)

    return portfolio_risk


# Define a function to calculate the stress test for a portfolio
def portfolio_stress_test(portfolio, returns, scenarios):
    # Create a DataFrame to hold the results of the stress test
    stress_test_results = pd.DataFrame()

    # Iterate over the scenarios and calculate the stressed portfolio for each one
    for scenario in scenarios:
        # Calculate the stressed portfolio
        stressed_portfolio = stress_test_scenario(portfolio, scenario)

        # Calculate the risk of the stressed portfolio
        stressed_risk = portfolio_risk(stressed_portfolio, returns)

        # Save the stressed risk to the DataFrame
        stress_test_results[str(scenario)] = stressed_risk

    # Return the results of the stress test
    return stress_test_results


# Define a sample portfolio
portfolio = {
    'Asset 1': 0.2,
    'Asset 2': 0.3,
    'Asset 3': 0.5
}

# Define a sample set of returns for each asset
returns = pd.DataFrame([
    [0.1, 0.15, 0.2],
    [0.2, 0.1, 0.15],
    [0.15, 0.2, 0.1],
    [0.1, 0.1, 0.15]
], columns=['Asset 1', 'Asset 2', 'Asset 3'])

# Define a sample set of stress test scenarios
scenarios = [-0.2, -0.1, 0, 0.1, 0.2]

# Calculate the stress test for the portfolio
stress_test_results = portfolio_stress_test(portfolio, returns, scenarios)

# Print the results of the stress test
print(stress_test_results)
