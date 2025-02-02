import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os


def calculate_var_and_es(historical_prices_path, confidence_level=0.95):
    """
    Calculate VaR and Expected Shortfall for each ticker in a given CSV file of historical prices.

    Parameters:
    - historical_prices_path: Path to the CSV file containing historical prices.
    - confidence_level: The confidence level for VaR and Expected Shortfall calculation.

    Returns:
    - A tuple of dictionaries: (var_dict, expected_shortfall_dict) where keys are ticker symbols.
    """
    historical_prices = pd.read_csv(
        historical_prices_path, index_col="Date", parse_dates=True
    )
    returns = historical_prices.pct_change().dropna()
    var_dict = {
        column: np.quantile(returns[column], 1 - confidence_level)
        for column in returns.columns
    }

    expected_shortfall_dict = {}
    for column in returns.columns:
        ticker_returns = returns[column]
        ticker_var = var_dict[column]
        ticker_es = ticker_returns[ticker_returns <= ticker_var].mean()
        expected_shortfall_dict[column] = ticker_es

    return var_dict, expected_shortfall_dict


def plot_expected_shortfall(expected_shortfall_dict, output_chart_png):
    """
    Plot Expected Shortfall for each ticker.

    Parameters:
    - expected_shortfall_dict: A dictionary with tickers as keys and their Expected Shortfalls as values.
    - output_chart_png: Path to save the output chart.
    """
    bar_color = "#AF0C15"
    plt.figure(figsize=(10, 6))
    plt.rc("font", size=14)
    plt.bar(
        expected_shortfall_dict.keys(),
        expected_shortfall_dict.values(),
        color=bar_color,
    )
    plt.xlabel("Tickers")
    plt.ylabel("Expected Shortfall")
    plt.title("Expected Shortfall for Each Ticker")
    plt.grid(axis="y")

    if not os.path.exists(os.path.dirname(output_chart_png)):
        os.makedirs(os.path.dirname(output_chart_png))

    plt.savefig(output_chart_png, bbox_inches="tight", pad_inches=0.2)
    plt.show()  # Close the plot explicitly after saving to free up memory


# This code block ensures that the following code only executes when the script is run directly,
# and not when imported as a module in another script.
if __name__ == "__main__":
    historical_prices_path = "data/portfolio/historical_prices.csv"
    output_chart_png = "scripts/Step_3_Outputs/expected_shortfall_chart.png"
    var_dict, expected_shortfall_dict = calculate_var_and_es(historical_prices_path)

    print("Expected Shortfall for each ticker:")
    for ticker, es in expected_shortfall_dict.items():
        print(f"{ticker}: {es:.6f}")

    plot_expected_shortfall(expected_shortfall_dict, output_chart_png)
