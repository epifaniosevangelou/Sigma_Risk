import pandas as pd
import numpy as np




"""
Calculate the Sortino ratio of a portfolio or investment.

Parameters:
- returns: pandas Series or DataFrame of historical returns
- risk_free_rate: annual risk-free rate (as a decimal)

Returns:
- Sortino ratio
    """

def sortino_ratio(returns, risk_free_rate):


# Calculate the average return and standard deviation of negative returns
        average_return = returns.mean()

#Filter out negative returns
        negative_returns = returns[returns < 0]

#Calculate the standard deviation of deviation of negative returns

        std_deviation = negative_returns.std()

# Calculate the Sortino ratio
        sortino_ratio_value  = (average_return - risk_free_rate)/ std_deviation
        return sortino_ratio_value

#Load the returns data from the CSV file
data = pd.read_csv("data/portfolio/portfolio_returns.csv", parse_dates=True, index_col='Date')

# Extract the returns column from the Total Return column
returns = data["Returns"]

# Define the risk-free rate, here used 10-year treasury yield.
risk_free_rate = 0.0463

# Calculate the Sortino ratio
sr = sortino_ratio(returns, risk_free_rate)

# Print the result
print(f"Sortino Ratio: {sr:.2f}")