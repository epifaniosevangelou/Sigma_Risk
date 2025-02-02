import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

ticker = "AAPL"
start_date = "2019-01-01"
end_date = "2020-01-01"
benchmark = "^GSPC"
show_plot = True

# Fetch stock data
stock_data = yf.download(ticker, start=start_date, end=end_date)
# Fetch S&P500 (market) data
market_data = yf.download(benchmark, start=start_date, end=end_date)
stock_data, market_data


# Calculate Arithmetic and logarithmic returns for both stock and market data
stock_data["Logarithmic Returns"] = np.log(
stock_data["Adj Close"] / stock_data["Adj Close"].shift(1)
)
market_data["Logarithmic Returns"] = np.log(
market_data["Adj Close"] / market_data["Adj Close"].shift(1)
)
stock_data, market_data


# Calculate beta
covariance_matrix = np.cov(
stock_data["Logarithmic Returns"].dropna(),
market_data["Logarithmic Returns"].dropna(),
)
covariance = covariance_matrix[0, 1]
market_variance = covariance_matrix[1, 1]
beta = covariance / market_variance



# Scatterplot of stock returns vs. market returns
plt.figure(figsize=(8, 6))
plt.scatter(
    market_data["Logarithmic Returns"].dropna(),
    stock_data["Logarithmic Returns"].dropna(),
    alpha=0.5
)
plt.xlabel("Market Returns")
plt.ylabel("Stock Returns")
plt.title(f"{ticker} Risk vs. Return")

# axis lines
plt.axhline(0, color="black", linestyle="--", linewidth=1)
plt.axvline(0, color="black", linestyle="--", linewidth=1)

# 45 degree line
max_value = max(
    np.abs(market_data["Logarithmic Returns"].max()),
    np.abs(stock_data["Logarithmic Returns"].max())
)
    
# Custom text
plt.text(
    -max_value,
    -max_value * 1.1,
    f"Actual Beta: {beta:.4f}", 
    fontsize=12, 
    color="blue",
)

plt.legend()
plt.grid(True)
output_path = r"OUTPUTS/Stock Reporting/Beta Report.png"


plt.savefig(output_path, bbox_inches="tight")
if show_plot:
    plt.show()