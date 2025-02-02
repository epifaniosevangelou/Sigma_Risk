import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pypfopt import risk_models


# INPUTS
file_path_semicomat = "scripts/Max/output/semi-covariance_matrix.png"
file_path_comat = "scripts/Max/output/covariance_matrix.png"
file_path_correlation = "scripts/Max/output/correlation_matrix.png"
file_path_exp_covmat = "scripts/Max/output/exponential_covariance_matrix.png"
palette = 'rocket'
annot = False # Only set to true if figsize is large enough around 10x10

# Relax the display limits on rows and columns
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
# Load the CSV file into a DataFrame
portfolio = pd.read_csv(
    "data/portfolio/all_historical_prices.csv",
    delimiter = ",",
    parse_dates = True,
    index_col = 0,
).dropna()
portfolio = portfolio.apply(pd.to_numeric, errors="coerce")
# Remove spaces and tabs from the ticker names (column names)
portfolio.columns = portfolio.columns.str.replace(r"\s+", "", regex=True)



# Calculate expected returns covariance, semicovariance, correlation
covar = risk_models.sample_cov(portfolio)
semicovar = risk_models.semicovariance(portfolio, threshold = 0)
correlation = portfolio.corr()
exponential_covar = risk_models.exp_cov(portfolio)





# Create a heatmap of the covariance matrix
plt.figure(figsize=(6, 5)) # Adjust the figure size as needed
sns.heatmap(
    covar, 
    cmap = palette, 
    annot = annot,
    fmt = ".2f",
    annot_kws = {"size": 5}  # Set the font size here (adjust as needed)
)
plt.title("Covariance Matrix Heatmap")
plt.savefig(
    file_path_comat, 
    bbox_inches = "tight",
    dpi  = 400
)


# Create a heatmap of the semicovariance matrix
plt.figure(figsize=(6, 5))  # Adjust the figure size as needed
sns.heatmap(
    semicovar, 
    cmap = palette, 
    annot = annot,
    fmt = ".2f",
    annot_kws = {"size": 5}  # Set the font size here (adjust as needed)
)
plt.title("Semi-Covariance Matrix Heatmap")
plt.savefig(
    file_path_semicomat, 
    bbox_inches = "tight",
    dpi = 400
)


# Create a heatmap of the correlation matrix
mask = np.eye(correlation.shape[0])  # Create a mask to hide the diagonal elements

plt.figure(figsize=(6, 5))  # Adjust the figure size as needed
sns.heatmap(
    correlation, 
    cmap = "vlag", 
    annot = annot,
    center = 0,
    fmt = ".2f",
    annot_kws = {"size": 5},  # Set the font size here (adjust as needed)
    mask = mask  # Apply the mask to hide the diagonal
)
plt.title("Correlation Matrix Heatmap")
plt.savefig(
    file_path_correlation, 
    bbox_inches="tight",
    dpi = 400
)


# Create a heatmap of the exponential covariance matrix
plt.figure(figsize=(6, 5))  # Adjust the figure size as needed
sns.heatmap(
    exponential_covar, 
    cmap = palette, 
    annot = annot,
    fmt = ".2f",
    annot_kws = {"size": 5}  # Set the font size here (adjust as needed)
)
plt.title("Exponential Covariance Matrix Heatmap")
plt.savefig(
    file_path_exp_covmat, 
    bbox_inches = "tight",
    dpi = 400
)