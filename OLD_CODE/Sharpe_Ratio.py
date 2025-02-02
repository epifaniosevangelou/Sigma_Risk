import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os


def fetch_stock_data(ticker_symbols):
    """
    Fetch historical adjusted close prices for a list of ticker symbols.

    Parameters:
    - ticker_symbols: List of ticker symbols (e.g., ["AAPL", "AMZN", "TSLA"]).

    Returns:
    - Dictionary containing historical price data for each ticker symbol.
    """
    stock_data = {}
    for ticker in ticker_symbols:
        stock_data[ticker] = yf.download(ticker, start="2022-12-02", end="2023-12-02")[
            "Adj Close"
        ].ffill()
    return stock_data


def calculate_daily_returns(stock_data):
    """
    Calculate daily returns for each stock in the provided data.

    Parameters:
    - stock_data: Dictionary containing historical price data for each stock.

    Returns:
    - DataFrame containing daily returns for each stock.
    """
    daily_returns = pd.DataFrame()
    for ticker in stock_data:
        daily_returns[ticker] = stock_data[ticker].pct_change()
    return daily_returns


def calculate_sharpe_ratios(daily_returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratios for each stock based on daily returns.

    Parameters:
    - daily_returns: DataFrame containing daily returns for each stock.
    - risk_free_rate: Risk-free rate of return (default is 0.02).

    Returns:
    - List of Sharpe Ratios for each stock.
    """
    sharpe_ratios = []
    for ticker in daily_returns:
        mean_daily_return = daily_returns[ticker].mean()
        std_daily_return = daily_returns[ticker].std()
        sharpe_ratio = (
            (mean_daily_return - risk_free_rate) / std_daily_return * (252**0.5)
        )  # 252 trading days in a year
        sharpe_ratios.append(sharpe_ratio)
    return sharpe_ratios


def plot_sharpe_ratios(ticker_symbols, sharpe_ratios):
    """
    Plot Sharpe Ratios for the provided ticker symbols.

    Parameters:
    - ticker_symbols: List of ticker symbols.
    - sharpe_ratios: List of Sharpe Ratios for each ticker.
    """
    plt.figure(figsize=(10, 6))
    plt.barh(ticker_symbols, sharpe_ratios, color="#0D3580")
    plt.xlabel("Sharpe Ratio")
    plt.title("Sharpe Ratio for Selected Airlines Stocks")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    for i, ratio in enumerate(sharpe_ratios):
        plt.text(ratio + 0.05, i, f"{ratio:.2f}", va="center")
    plt.tight_layout()


def save_output_chart(output_chart_png):
    """
    Save the output chart as a PNG file.

    Parameters:
    - output_chart_png: Path to save the output chart.
    """
    plt.savefig(output_chart_png, bbox_inches="tight", pad_inches=0.2)
    plt.show()


def main():
    ticker_symbols = [
        "LUV",
        "DAL",
        "AAL",
        "UAL",
        "ALK",
        "JBLU",
        "SAVE",
        "HA",
        "SKYW",
        "MESA",
        "ALGT",
        "CPA",
        "GOL",
        "AZUL",
        "VLRS",
        "JETS",
        "BA",
        "LMT",
        "RTX",
        "GD",
        "NOC",
        "LHX",
        "TDG",
        "HEI",
        "SPR",
        "HII",
        "CW",
    ]
    stock_data = fetch_stock_data(ticker_symbols)
    daily_returns = calculate_daily_returns(stock_data)
    sharpe_ratios = calculate_sharpe_ratios(daily_returns)
    plot_sharpe_ratios(ticker_symbols, sharpe_ratios)
    output_dir = "scripts/Step_3_Outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_chart_png = os.path.join(output_dir, "Sharpe_Ratio.png")
    save_output_chart(output_chart_png)


if __name__ == "__main__":
    main()
