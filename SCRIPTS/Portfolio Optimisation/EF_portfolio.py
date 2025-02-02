import numpy as np
import pandas as pd
import riskfolio as rp
import matplotlib.pyplot as plt
import warnings


# Set Variables ( Set constraints in EXCEL file )

alpha = 0.05  # Confidence level for CVaR and EVaR and other risk measures
method_mu = "hist"  # Method to estimate expected returns, hist for historical mean and ewma2 fir Exponential Weighted Moving Average with Adjust=False
method_cov = (
    "ledoit"  # Method to estimate covariance matrix, can be ledoit, hist or ewma2
)
model = "Classic"  # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
rm = "MV"  # Risk measure used, this time will be variance
obj = "MinRisk"  # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True  # Use historical scenarios for risk measures that depend on scenarios
rf = 0  # Risk free rate
l = 0  # Risk aversion factor, only useful when obj is 'Utility'

# Risk Measures available:
# ’MV’: Standard Deviation.
# ’KT’: Square Root of Kurtosis.
# ’MAD’: Mean Absolute Deviation.
# ’GMD’: Gini Mean Difference.
# ’MSV’: Semi Standard Deviation.
# ’SKT’: Square Root of Semi Kurtosis.
# ’FLPM’: First Lower Partial Moment (Omega Ratio).
# ’SLPM’: Second Lower Partial Moment (Sortino Ratio).
# ’CVaR’: Conditional Value at Risk.
# ’TG’: Tail Gini.
# ’EVaR’: Entropic Value at Risk.
# ’RLVaR’: Relativistic Value at Risk.
# ’WR’: Worst Realization (Minimax).
# ’RG’: Range of returns.
# ’CVRG’: CVaR range of returns.
# ’TGRG’: Tail Gini range of returns.
# ’MDD’: Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
# ’ADD’: Average Drawdown of uncompounded cumulative returns.
# ’CDaR’: Conditional Drawdown at Risk of uncompounded cumulative returns.
# ’EDaR’: Entropic Drawdown at Risk of uncompounded cumulative returns.
# ’RLDaR’: Relativistic Drawdown at Risk of uncompounded cumulative returns.
# ’UCI’: Ulcer Index of uncompounded cumulative returns.


# set pandas options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.options.display.float_format = "{:.4%}".format
warnings.filterwarnings("ignore")
pd.options.display.float_format = "{:.4%}".format


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

# Load industry information from additional_info.csv
additional_info = pd.read_csv("data/portfolio/additional_info.csv", index_col=0)


# Set Constraints
asset_classes = {
    "Assets": additional_info.reset_index()["Ticker"].tolist(),
    "Industry": additional_info["Industry"].tolist(),
}
asset_classes = pd.DataFrame(asset_classes)
print("Asset Classes:")
print(asset_classes)

# Create constraints dataframe from excel file
constraints = pd.read_excel("data/portfolio/ef_constraints.xlsx")
print("Constraints:")
print(constraints)

# calculating returns
Y = portfolio.pct_change().dropna()

# Building the portfolio object
port = rp.Portfolio(returns=Y, alpha=alpha)

# Setting portfolio constraints
A, B = rp.assets_constraints(constraints, asset_classes)
port.ainequality = A
port.binequality = B

# Set methods for expected returns and covariance matrix
port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal weights:
w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
print("Weights Allocation:")
print(w)
print(w.sum())

# Save weight to csv in output folder
w.to_csv("scripts/Step_3_Outputs/EF_weights.csv")

# Plot barchart of asset allocation
ax = w.plot.bar(
    figsize=(6, 5),
    legend=False,
    title="EF Portfolio Weights",
    xlabel="Assets",
    ylabel="Weight",
)
# Save plot to png in output folder
ax.figure.savefig("scripts/Step_3_Outputs/EF_bar.png", bbox_inches="tight", dpi=400)

# Show asset allocation by industry
w_classes = pd.concat([asset_classes.set_index("Assets"), w], axis=1)
w_classes = w_classes.groupby(["Industry"]).sum()
print("Weights Allocation by Industry:")
print(w_classes)


# Compare risk measures
rms = [
    "MV",
    "MAD",
    "MSV",
    "FLPM",
    "SLPM",
    "CVaR",
    "EVaR",
    "WR",
    "MDD",
    "ADD",
    "CDaR",
    "UCI",
    "EDaR",
]

w_s = pd.DataFrame([])

for i in rms:
    w = port.optimization(model=model, rm=i, obj=obj, rf=rf, l=l, hist=hist)
    w_s = pd.concat([w_s, w], axis=1)

w_s.columns = rms
w_s.style.format("{:.2%}").background_gradient(cmap="YlGn").to_excel(
    "scripts/Max/output/EF_comparison.xlsx"
)


# Calculate Efficient Frontier
points = 60  # Number of points of the frontier
frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)


# Plotting the efficient frontier

label = "Minimum Variance"  # Title of point
mu = port.mu  # Expected returns
cov = port.cov  # Covariance matrix
returns = port.returns  # Returns of the assets

ax = rp.plot_frontier(
    w_frontier=frontier,
    mu=mu,
    cov=cov,
    returns=returns,
    rm=rm,
    rf=rf,
    alpha=alpha,
    cmap="viridis",
    w=w,
    label=label,
    marker="*",
    s=16,
    c="r",
    height=5,
    width=6,
    ax=None,
    kelly=True,
)
# Save plot to png in output folder
ax.figure.savefig("scripts/Max/output/EF_frontier.png", bbox_inches="tight", dpi=400)
