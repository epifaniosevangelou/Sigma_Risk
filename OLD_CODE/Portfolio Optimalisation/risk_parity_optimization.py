import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

def load_weights(file_path, weight_column_name='Weight in Portofolio '):
    """
    Load portfolio weights from a specific column in a CSV file.
    
    Args:
    file_path (str): Path to the CSV file containing portfolio weights.
    weight_column_name (str): The column name where weights are stored.
    
    Returns:
    numpy.ndarray: Array of weights.
    """
    # Load the entire CSV into a DataFrame
    data = pd.read_csv(file_path, sep = ";")
    if weight_column_name in data.columns:
        # Replace commas with dots and convert to float
        weights = data[weight_column_name].str.replace(',', '.').astype(float).values
    else:
        raise ValueError(f"Column '{weight_column_name}' not found in the file.")
    
    return weights

def load_historical_prices():
    # Assuming historical prices are loaded from a CSV for simplicity
    return pd.read_csv("data/portfolio/historical_prices.csv", index_col="Date", parse_dates=True)

def calculate_portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def calculate_var(value, volatility, confidence_level):
    return norm.ppf(1 - confidence_level) * value * volatility

def calculate_risk_parity_weights(returns):
    # Calculate the annualized volatility for each asset
    volatilities = returns.std() * np.sqrt(252)

    # Inverse volatility weights
    inverse_volatility = 1 / volatilities

    # Normalize weights so that they sum to 1
    normalized_weights = inverse_volatility / inverse_volatility.sum()

    return normalized_weights

def main():
    historical_prices = load_historical_prices()
    returns = historical_prices.pct_change().dropna()
    cov_matrix = returns.cov()
    portfolio_exposure = 46699.07  # Example exposure
    confidence_level = 0.95
    # Equally weighted portfolio
    num_assets = len(historical_prices.columns)
    equal_weights = np.array([1.0 / num_assets] * num_assets)

    # Calculate VaR for equally weighted portfolio
    equal_volatility = calculate_portfolio_volatility(equal_weights, cov_matrix)
    equal_var = calculate_var(portfolio_exposure, equal_volatility, confidence_level)

    # Original weights (assuming equal weights for simplicity)
    original_weights = load_weights("data/portfolio/All_Sectors.csv", weight_column_name = "Weight in Portofolio ")

    # Calculate VaR with original weights
    original_volatility = calculate_portfolio_volatility(original_weights, cov_matrix)
    original_var = calculate_var(portfolio_exposure, original_volatility, confidence_level)

    # Risk Parity Weights
    risk_parity_weights = calculate_risk_parity_weights(returns)
    risk_parity_volatility = calculate_portfolio_volatility(risk_parity_weights, cov_matrix)
    risk_parity_var = calculate_var(portfolio_exposure, risk_parity_volatility, confidence_level)

    # Print results
    print("Equally Weighted Portfolio VaR: {:.2f}".format(equal_var))
    print("Risk Parity Weights VaR: {:.2f}".format(risk_parity_var))
    print("Original Weights VaR: {:.2f}".format(original_var))
    print("Risk Parity Weights", risk_parity_weights)

if __name__ == "__main__":
    main()
