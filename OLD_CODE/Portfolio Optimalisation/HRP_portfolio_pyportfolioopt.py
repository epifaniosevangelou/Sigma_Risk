import pandas as pd
import matplotlib.pyplot as plt
from pypfopt import HRPOpt
import pypfopt.plotting as plotting


# Set Inputs
min_weight = 0.01
max_weight = 0.1
portfolio_value = 40000
rf_rate = 0.05
file_path_weights="scripts/Max/output/HRP_weights.csv"
file_path_bar="scripts/Max/output/HRP_bar.png"



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
returns = portfolio.pct_change().dropna()
# HRP Optimisation
hrp = HRPOpt(returns)
weights = hrp.optimize()
cleaned_weights = hrp.clean_weights()
# Show results
print(dict(cleaned_weights))
hrp.portfolio_performance(verbose=True, risk_free_rate = rf_rate)
# Save weights to csv
hrp.save_weights_to_file(file_path_weights)

# dendogram of HRP
ax = plotting.plot_dendrogram(hrp);
plt.savefig("scripts/Max/output/HRP_dendogram.png", format="png", dpi=400, bbox_inches="tight")


# Bar chart of asset allocation
fig, ax = plt.subplots(figsize=(10, 6))
weights_series = pd.Series(cleaned_weights)
bar_width = 0.6
weights_series.plot(kind="bar", ax=ax, width=bar_width)
plt.title("Asset Allocation")
plt.ylabel("Weight")
plt.xlabel("Asset")
plt.xticks(rotation=90)
# Display return, volatility, and Sharpe ratio above the chart
return_val, volatility_val, sharpe_ratio = hrp.portfolio_performance(risk_free_rate = rf_rate)
return_str = f"Return: {return_val:.2%}"
volatility_str = f"Volatility: {volatility_val:.2%}"
sharpe_str = f"Sharpe Ratio: {sharpe_ratio:.4f}"
plt.annotate(return_str, xy=(0.05, 1.15), xycoords="axes fraction")
plt.annotate(volatility_str, xy=(0.05, 1.10), xycoords="axes fraction")
plt.annotate(sharpe_str, xy=(0.05, 1.05), xycoords="axes fraction")
# Save the chart as a PNG under the "charts/" directory
plt.savefig(file_path_bar, bbox_inches="tight", dpi = 400)



# actual allocation (experimental)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(portfolio)
da = DiscreteAllocation(
    cleaned_weights, latest_prices, total_portfolio_value=portfolio_value
)
allocation, leftover = da.greedy_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))