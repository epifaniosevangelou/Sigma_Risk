import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pypfopt import black_litterman
from pypfopt import black_litterman, risk_models
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt import EfficientFrontier, objective_functions
import seaborn as sns


# Inputs
benchmark = "^GSPC"  # The use of SPY is a consideration
rf_rate = 0.05  # Getting the FED funds rate is a consideration
min_weight = 0.01
max_weight = 0.1
portfolio_value = 40000
gam = 2  # adjusts the penalty for too low and too high weights
Tau = 0.05  # Controls the weighting of views

# Relax the display limits on rows and columns
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# Load the price info file into a DataFrame
portfolio = pd.read_csv(
    "data/portfolio/all_historical_prices.csv",
    delimiter=",",
    parse_dates=True,
    index_col=0,
).dropna()
portfolio = portfolio.apply(pd.to_numeric, errors="coerce")
# Remove spaces and tabs from the ticker names (column names)
portfolio.columns = portfolio.columns.str.replace(r"\s+", "", regex=True)

# Load the additional data into a Dataframe
additional_data = pd.read_csv(
    "data/portfolio/additional_info.csv",
    delimiter=",",
)


# Fetch the historical performance of benchmark
market_prices = yf.download(benchmark, period="max")["Adj Close"]

# Create dictionary for absolute views
ticker_column = additional_data["Ticker"]
prediction_column = additional_data["Current Prediction"]
view_dict = dict(zip(ticker_column, prediction_column))

# Create dictionary for market caps
mcap_column = additional_data["Market Cap"]
mcap_dict = dict(zip(ticker_column, mcap_column))


# Create the priors for the model
S = risk_models.CovarianceShrinkage(portfolio).ledoit_wolf()
delta = black_litterman.market_implied_risk_aversion(market_prices)
market_prior = black_litterman.market_implied_prior_returns(mcap_dict, delta, S)

# Run the Black-Litterman model
bl = BlackLittermanModel(S, pi=market_prior, absolute_views=view_dict, tau=Tau)
ret_bl = bl.bl_returns()
S_bl = bl.bl_cov()

# Show the output of BL model
rets_df = pd.DataFrame(
    [market_prior, ret_bl, pd.Series(view_dict)], index=["Prior", "Posterior", "Views"]
).T
ax = rets_df.plot.bar(figsize=(6, 5))
plt.savefig(
    "scripts/Step_3_Outputs/Black-Litterman.png",
    format="png",
    dpi=400,
    bbox_inches="tight",
)


# BL estimate to returns dataframe
returns = pd.DataFrame(ret_bl).T
# Create the "Date" column
returns["Index"] = "Posterior"
# Reorder the columns to have "Date" as the first column
returns = returns[["Index"] + [col for col in returns if col != "Index"]]
# Assuming "returns" is your DataFrame
returns.set_index("Index", inplace=True)
returns = returns.apply(pd.to_numeric, errors="coerce")


# Make the portfolio allocation using Efficient Frontier
ef = EfficientFrontier(ret_bl, S_bl, weight_bounds=(min_weight, max_weight))
ef.add_objective(objective_functions.L2_reg, gamma=gam)
raw_weights = ef.max_sharpe(risk_free_rate=rf_rate)
cleaned_weights = ef.clean_weights()
ef.save_weights_to_file("scripts/Step_3_Outputs/BL_weights.csv")
print(cleaned_weights)
ef.portfolio_performance(verbose=True, risk_free_rate=rf_rate)


# Bar chart of asset allocation
fig, ax = plt.subplots(figsize=(6, 5))
weights_series = pd.Series(cleaned_weights)
bar_width = 0.6
weights_series.plot(kind="bar", ax=ax, width=bar_width)
plt.title("BL Portfolio Weights")
plt.ylabel("Weight")
plt.xlabel("Asset")
plt.xticks(rotation=90)
# # Display return, volatility, and Sharpe ratio above the chart
# return_val, volatility_val, sharpe_ratio = ef.portfolio_performance()
# return_str = f"Return: {return_val:.2%}"
# volatility_str = f"Volatility: {volatility_val:.2%}"
# sharpe_str = f"Sharpe Ratio: {sharpe_ratio:.4f}"
# plt.annotate(return_str, xy=(0.05, 1.15), xycoords="axes fraction")
# plt.annotate(volatility_str, xy=(0.05, 1.10), xycoords="axes fraction")
# plt.annotate(sharpe_str, xy=(0.05, 1.05), xycoords="axes fraction")
# Save the chart as a PNG under the "scripts/Step_3_Outputs/" directory
plt.savefig("scripts/Step_3_Outputs/BL_bar.png", bbox_inches="tight", dpi=400)


# actual allocation (experimental)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(portfolio)
da = DiscreteAllocation(
    cleaned_weights, latest_prices, total_portfolio_value=portfolio_value
)
allocation, leftover = da.greedy_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))
