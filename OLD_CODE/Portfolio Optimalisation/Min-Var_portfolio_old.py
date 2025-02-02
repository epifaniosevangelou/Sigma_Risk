import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions

# INPUTS
min_weight = 0.01
max_weight = 0.1
portfolio_value = 40000
rf_rate = 0.05
gam = 0.1  # adjusts the penalty for too low and too high weights

# Relax the display limits on rows and columns
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
# Load the CSV file into a DataFrame
portfolio = pd.read_csv(
    "data/portfolio/all_historical_prices.csv",
    delimiter=",",
    parse_dates=True,
    index_col=0,
).dropna()
portfolio = portfolio.apply(pd.to_numeric, errors="coerce")
# Remove spaces and tabs from the ticker names (column names)
portfolio.columns = portfolio.columns.str.replace(r"\s+", "", regex=True)


# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(portfolio)
S = risk_models.CovarianceShrinkage(portfolio).ledoit_wolf()
# Optimize for maximal Sharpe ratio with constaints
ef = EfficientFrontier(mu, S, weight_bounds=(min_weight, max_weight))
# L2 Regularisation
ef.add_objective(objective_functions.L2_reg, gamma=gam)
# continue maximal sharpe ratio optimization
raw_weights = ef.min_volatility()
cleaned_weights = ef.clean_weights()
ef.save_weights_to_file("scripts/Max/output/Min-Var_weights.csv")  # saves to file
print(cleaned_weights)
ef.portfolio_performance(verbose=True, risk_free_rate=rf_rate)





# Bar chart of asset allocation
fig, ax = plt.subplots(figsize=(10, 6))
weights_series = pd.Series(cleaned_weights)
bar_width = 0.6  # Adjust the bar width as needed
weights_series.plot(
    kind="bar",
    ax=ax,
    width=bar_width,
)
plt.title("Asset Allocation")
plt.ylabel("Weight")
plt.xlabel("Asset")
plt.xticks(rotation=90)
# Display return, volatility, and Sharpe ratio above the chart
return_val, volatility_val, sharpe_ratio = ef.portfolio_performance()
return_str = f"Return: {return_val:.2%}"
volatility_str = f"Volatility: {volatility_val:.2%}"
sharpe_str = f"Sharpe Ratio: {sharpe_ratio:.4f}"
# Adjust the y-coordinate to prevent overlap
plt.annotate(return_str, xy=(0.05, 1.15), xycoords="axes fraction")
plt.annotate(volatility_str, xy=(0.05, 1.10), xycoords="axes fraction")
plt.annotate(sharpe_str, xy=(0.05, 1.05), xycoords="axes fraction")
# Save the chart as a PNG under the "data/" directory
plt.savefig("scripts/Max/output/Min-Var_allocation.png", bbox_inches="tight", dpi = 400)



# actual allocation (experimental)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(portfolio)
da = DiscreteAllocation(
    cleaned_weights, latest_prices, total_portfolio_value=portfolio_value
)
allocation, leftover = da.greedy_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))