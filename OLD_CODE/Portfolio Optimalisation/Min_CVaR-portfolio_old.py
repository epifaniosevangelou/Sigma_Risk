import pandas as pd
import matplotlib.pyplot as plt
from pypfopt import EfficientCVaR
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions

# INPUTS
min_weight = 0.01
max_weight = 0.1
portfolio_value = 40000
rf_rate = 0.05
gam = 0.1  # adjusts the penalty for too low and too high weights
bet = 0.95  # confidence level for CVaR

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


# Returns
returns = expected_returns.returns_from_prices(portfolio).dropna()
mu = expected_returns.mean_historical_return(portfolio)
# Optimize for minimum CVaR with constaints
ec = EfficientCVaR(mu, returns, beta=bet, weight_bounds=(min_weight, max_weight))
# L2 Regularisation
ec.add_objective(objective_functions.L2_reg, gamma=gam)
# continue maximal sharpe ratio optimization
raw_weights = ec.min_cvar()
cleaned_weights = ec.clean_weights()
ec.save_weights_to_file("scripts/Max/output/Min-CVaR_weights.csv")  # saves to file
print(cleaned_weights)
ec.portfolio_performance(verbose=True)



# Bar chart of asset allocation (no performance metrics)
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
# Save the chart as a PNG under the "data/" directory
plt.savefig("scripts/Max/output/Min-CVaR_allocation.png", bbox_inches="tight", dpi = 400)



# actual allocation (experimental)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(portfolio)
da = DiscreteAllocation(
    cleaned_weights, latest_prices, total_portfolio_value=portfolio_value
)
allocation, leftover = da.greedy_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))