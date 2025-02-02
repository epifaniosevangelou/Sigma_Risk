import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from pypfopt import black_litterman
from pypfopt import black_litterman, risk_models
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt import HRPOpt


# Inputs
benchmark = '^GSPC'  # The use of SPY is a consideration
rf_rate = 0.05 # Getting the FED funds rate is a consideration
Tau = 0.05

# Relax the display limits on rows and columns
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# Load the price info file into a DataFrame
portfolio = pd.read_csv(
    "data/portfolio/historical_prices.csv",
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

#Create dictionary for market caps
mcap_column = additional_data["Market Cap"]
mcap_dict = dict(zip(ticker_column, mcap_column))



# Create the priors for the model
S = risk_models.CovarianceShrinkage(portfolio).ledoit_wolf()
delta = black_litterman.market_implied_risk_aversion(market_prices)
market_prior = black_litterman.market_implied_prior_returns(mcap_dict, delta, S)

# Run the Black-Litterman model
bl = BlackLittermanModel(
    S, 
    pi=market_prior, 
    absolute_views=view_dict,
    tau = Tau
)
ret_bl = bl.bl_returns()
S_bl = bl.bl_cov()

# Show the output of BL model
rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(view_dict)], 
index=["Prior", "Posterior", "Views"]).T
ax = rets_df.plot.bar(figsize=(8,6))
plt.savefig("scripts/Max/output/Black-Litterman.png", format="png", dpi=400, bbox_inches="tight")



# BL estimate to returns dataframe
returns = pd.DataFrame(ret_bl).T
# Create the "Date" column
returns["Index"] = "Posterior"
# Reorder the columns to have "Date" as the first column
returns = returns[["Index"] + [col for col in returns if col != "Index"]]
# Assuming "returns" is your DataFrame
returns.set_index("Index", inplace=True)
returns = returns.apply(pd.to_numeric, errors='coerce')



# Number of time periods you want to simulate
num_periods = 252  # Adjust as needed

# Number of assets
num_assets = len(returns.columns)  # Number of columns in returns

# Create a random seed for reproducibility (optional)
np.random.seed(42)

# Extract the tickers from the first row of the returns DataFrame
tickers = returns.columns

# Calculate the expected daily returns (assuming annual returns) for each asset
expected_returns_daily = (1 + returns) ** (1 / 252) - 1

# Initialize an empty DataFrame to store the simulated returns
simulated_returns_df = pd.DataFrame(columns=tickers)

for _ in range(num_periods):
    # Generate random returns using multivariate normal distribution
    mean = expected_returns_daily.mean().to_numpy()  # Convert to a 1D array
    simulated_returns = np.random.multivariate_normal(
        mean, S_bl, size=1
    )
    
    # Create a DataFrame for the simulated returns
    simulated_returns_df = pd.concat(
        [simulated_returns_df, pd.DataFrame(simulated_returns, columns=tickers)],
        ignore_index=True
    )

# Cumulatively product to get a time series of prices
simulated_prices = (1 + simulated_returns_df).cumprod()
#simulated_prices.to_csv('simulated_prices.csv')


# Optimise for allocation using HRP model
hrp = HRPOpt(
    simulated_prices,
    S_bl
)
weights = hrp.optimize()
cleaned_weights = hrp.clean_weights()
# Show results
print(dict(cleaned_weights))
hrp.portfolio_performance(verbose=True, risk_free_rate = rf_rate)
# Save weights to csv
hrp.save_weights_to_file("scripts/Max/output/BL_HRP_weights.csv")



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
plt.savefig("scripts/Max/output/BL-HRP_bar", bbox_inches="tight", dpi = 400)
