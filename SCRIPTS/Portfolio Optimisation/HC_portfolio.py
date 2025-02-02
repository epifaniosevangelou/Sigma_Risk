import numpy as np
import pandas as pd
import riskfolio as rp
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
pd.options.display.float_format = "{:.4%}".format

# Set Variables ( Set constraints in EXCEL file )
model = "HRP"  # Could be HRP, HERC or NCO
codependence = "pearson"  # Correlation matrix used to group assets in clusters
covariance = (
    "ewma2"  # Method to estimate covariance matrix, can be ledoit, hist or ewma2
)
rm = "CVaR"  # Risk measure used
rf = 0  # Risk free rate
linkage = "ward"  # Linkage method used to build clusters
max_k = 10  # Max number of clusters used in two difference gap statistic, only for HERC model
leaf_order = True  # Consider optimal order of leafs in dendrogram
alpha = 0.05  # Confidence level for CVaR and EVaR and other risk measures
obj = "MinRisk"  # Objective function for NCO, could be MinRisk, ERC (Equal Risk Contribution), Utility or Sharpe


# Risk Measures available:
# ’equal’: Equally weighted.
# 'vol': Standard Deviation.
# 'MV': Variance.
# 'MAD': Mean Absolute Deviation.
# 'MSV': Semi Standard Deviation.
# 'FLPM': First Lower Partial Moment (Omega Ratio).
# 'SLPM': Second Lower Partial Moment (Sortino Ratio).
# 'VaR': Conditional Value at Risk.
# 'CVaR': Conditional Value at Risk.
# 'EVaR': Entropic Value at Risk.
# 'WR': Worst Realization (Minimax)
# 'MDD': Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
# 'ADD': Average Drawdown of uncompounded cumulative returns.
# 'DaR': Drawdown at Risk of uncompounded cumulative returns.
# 'CDaR': Conditional Drawdown at Risk of uncompounded cumulative returns.
# 'EDaR': Entropic Drawdown at Risk of uncompounded cumulative returns.
# 'UCI': Ulcer Index of uncompounded cumulative returns.
# 'MDD_Rel': Maximum Drawdown of compounded cumulative returns (Calmar Ratio).
# 'ADD_Rel': Average Drawdown of compounded cumulative returns.
# 'DaR_Rel': Drawdown at Risk of compounded cumulative returns.
# 'CDaR_Rel': Conditional Drawdown at Risk of compounded cumulative returns.
# 'EDaR_Rel': Entropic Drawdown at Risk of compounded cumulative returns.
# 'UCI_Rel': Ulcer Index of compounded cumulative returns.


# set pandas options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
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
constraints = pd.read_excel("data/portfolio/hc_constraints.xlsx")
print("Constraints:")
print(constraints)

# calculating returns
Y = portfolio.pct_change().dropna()

# Building the portfolio object
port = rp.HCPortfolio(returns=Y, alpha=alpha)

w_max, w_min = rp.hrp_constraints(constraints, asset_classes)

port.w_max = w_max.astype(float)
port.w_min = w_min.astype(float)

w = port.optimization(
    model=model,
    codependence=codependence,
    covariance=covariance,
    rm=rm,
    rf=rf,
    linkage=linkage,
    max_k=max_k,
    leaf_order=leaf_order,
    obj=obj,
)
# Show asset allocation
print("Weights Allocation:")
print(w)
print(w.sum())

# Save weight to csv in output folder
w.to_csv("scripts/Step_3_Outputs/HC_weights.csv")

# Plot barchart of asset allocation
ax = w.plot.bar(
    figsize=(6, 5),
    legend=False,
    title="HC Portfolio Weights",
    xlabel="Assets",
    ylabel="Weight",
)
# Save plot to png in output folder
ax.figure.savefig("scripts/Step_3_Outputs/HC_bar.png", bbox_inches="tight", dpi=400)

# Show asset allocation by industry
w_classes = pd.concat([asset_classes.set_index("Assets"), w], axis=1)
w_classes = w_classes.groupby(["Industry"]).sum()
print("Weights Allocation by Industry:")
print(w_classes)

# Comparison of risk measures
rms = [
    "vol",
    "MV",
    "MAD",
    "MSV",
    "FLPM",
    "SLPM",
    "VaR",
    "CVaR",
    "EVaR",
    "WR",
    "MDD",
    "ADD",
    "DaR",
    "CDaR",
    "EDaR",
    "UCI",
    "MDD_Rel",
    "ADD_Rel",
    "DaR_Rel",
    "CDaR_Rel",
    "EDaR_Rel",
    "UCI_Rel",
]

w_s = pd.DataFrame([])

for i in rms:
    w = port.optimization(
        model=model,
        codependence=codependence,
        covariance=covariance,
        rm=i,
        rf=rf,
        linkage=linkage,
        max_k=max_k,
        leaf_order=leaf_order,
    )

    w_s = pd.concat([w_s, w], axis=1)

w_s.columns = rms
w_s.style.format("{:.2%}").background_gradient(cmap="YlGn").to_excel(
    "scripts/Step_3_Outputs/HC_comparison.xlsx"
)


# Plot HC dendogram
ax = rp.plot_dendrogram(
    returns=Y,
    codependence=codependence,
    linkage=linkage,
    k=None,
    max_k=10,
    leaf_order=True,
    ax=None,
)
# Save plot to png in output folder
ax.figure.savefig(
    "scripts/Step_3_Outputs/HC_dendogram.png", bbox_inches="tight", dpi=400
)
