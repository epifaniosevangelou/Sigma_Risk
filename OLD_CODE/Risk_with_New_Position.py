import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def fetch_data(stock_ticker, benchmark_ticker, start_date, end_date):
    """
    Fetch historical stock and market data from Yahoo Finance.
    """
    # Fetch stock data
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    benchmark_data = yf.download(benchmark_ticker, start=start_date, end=end_date)

    # Calculate returns from 'Adj Close' prices
    stock_returns = stock_data['Adj Close'].pct_change().dropna()
    benchmark_returns = benchmark_data['Adj Close'].pct_change().dropna()

    return stock_returns, benchmark_returns


def calculate_beta(portfolio_returns, market_returns):
    """
    Calculate Beta as the covariance between portfolio and market returns divided by market variance.
    """
    covariance = np.cov(portfolio_returns, market_returns)[0, 1]
    market_variance = np.var(market_returns)
    beta = covariance / market_variance
    return beta


def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio: (Portfolio Return - Risk-Free Rate) / Portfolio Std Dev.
    """
    excess_return = returns.mean() - risk_free_rate / 252  # Assuming risk-free rate is annualized
    std_dev = returns.std()
    sharpe_ratio = excess_return / std_dev
    return sharpe_ratio


def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sortino Ratio: (Portfolio Return - Risk-Free Rate) / Downside Std Dev.
    """
    excess_return = returns.mean() - risk_free_rate / 252
    negative_returns = returns[returns < 0]
    downside_std_dev = negative_returns.std()
    sortino_ratio = excess_return / downside_std_dev
    return sortino_ratio


def compare_risks(existing_portfolio_returns, new_stock_returns, new_stock_allocation):
    """
    Combine portfolio returns with new stock returns and calculate combined statistics.
    """
    combined_returns = (
        existing_portfolio_returns + new_stock_allocation * new_stock_returns
    )
    mean_return, std_return = portfolio_stats(combined_returns)
    return std_return, combined_returns


def portfolio_stats(returns):
    """
    Returns the mean and standard deviation of the portfolio returns.
    """
    mean_return = returns.mean()
    std_return = returns.std()
    return mean_return, std_return


def visualize_portfolio(
    portfolio_returns,
    combined_std,
    beta_before,
    beta_after,
    sharpe_before,
    sharpe_after,
    sortino_before,
    sortino_after,
    output_dir,
    show_plot=False
):
    """
    Visualize the portfolio's risk, beta, Sharpe, and Sortino ratios before and after adding the new stock.
    """
    labels = ["Before", "After"]
    std_dev = [portfolio_returns.std(), combined_std]
    beta_values = [beta_before, beta_after]
    sharpe_values = [sharpe_before, sharpe_after]
    sortino_values = [sortino_before, sortino_after]

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))  # Create 2x2 subplots for Std Dev, Beta, Sharpe, Sortino
    
    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.4, wspace=0.4)  # Reduce the space between the plots

    # Standard Deviation plot
    bars1 = ax[0, 0].bar(labels, std_dev, color=["blue", "orange"], width=0.4)
    ax[0, 0].set_ylabel("Standard Deviation")
    ax[0, 0].set_title("Portfolio Risk Comparison (Std Dev)")
    
    for bar in bars1:
        height = bar.get_height()
        ax[0, 0].annotate(f"{round(height, 4)}", xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                          textcoords="offset points", ha="center", va="bottom")

    # Beta plot
    bars2 = ax[0, 1].bar(labels, beta_values, color=["green", "red"], width=0.4)
    ax[0, 1].set_ylabel("Beta")
    ax[0, 1].set_title("Portfolio Beta Comparison")
    
    for bar in bars2:
        height = bar.get_height()
        ax[0, 1].annotate(f"{round(height, 4)}", xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                          textcoords="offset points", ha="center", va="bottom")

    # Sharpe Ratio plot
    bars3 = ax[1, 0].bar(labels, sharpe_values, color=["purple", "yellow"], width=0.4)
    ax[1, 0].set_ylabel("Sharpe Ratio")
    ax[1, 0].set_title("Sharpe Ratio Comparison")
    
    for bar in bars3:
        height = bar.get_height()
        ax[1, 0].annotate(f"{round(height, 4)}", xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                          textcoords="offset points", ha="center", va="bottom")

    # Sortino Ratio plot
    bars4 = ax[1, 1].bar(labels, sortino_values, color=["cyan", "pink"], width=0.4)
    ax[1, 1].set_ylabel("Sortino Ratio")
    ax[1, 1].set_title("Sortino Ratio Comparison")
    
    for bar in bars4:
        height = bar.get_height()
        ax[1, 1].annotate(f"{round(height, 4)}", xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                          textcoords="offset points", ha="center", va="bottom")

    # Use tight_layout to automatically adjust subplot parameters
    plt.tight_layout()

    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir, "portfolio_risk_comparison_with_ratios.png"), bbox_inches="tight")
    if show_plot:
        plt.show()

    plt.close(fig)  # Close the plot to free up memory


def main():
    # Define the stock ticker and benchmark (e.g., S&P 500 as ^GSPC)
    stock_ticker = "LOW"  # Lowe's Companies, Inc.
    benchmark_ticker = "^GSPC"  # S&P 500
    start_date = "2020-01-01"
    end_date = "2023-01-01"

    # Fetch stock and benchmark data
    new_stock_returns, benchmark_returns = fetch_data(stock_ticker, benchmark_ticker, start_date, end_date)

    # Simulate existing portfolio returns (this can be loaded or computed as you see fit)
    portfolio_returns = np.random.normal(0.001, 0.02, len(new_stock_returns))  # Example: Random portfolio returns

    # Calculate Beta before adding the new stock
    beta_before = calculate_beta(portfolio_returns, benchmark_returns)

    # Define the allocation for the new stock
    new_stock_allocation = 0.03

    # Compare risks and get combined portfolio stats
    combined_std, combined_returns = compare_risks(portfolio_returns, new_stock_returns, new_stock_allocation)

    # Calculate Beta after adding the new stock
    beta_after = calculate_beta(combined_returns, benchmark_returns)

    # Calculate Sharpe and Sortino ratios
    sharpe_before = calculate_sharpe_ratio(portfolio_returns)
    sharpe_after = calculate_sharpe_ratio(combined_returns)
    sortino_before = calculate_sortino_ratio(portfolio_returns)
    sortino_after = calculate_sortino_ratio(combined_returns)

    print("Portfolio Risk Before Adding", stock_ticker, ":", portfolio_returns.std())
    print("Portfolio Risk After Adding", stock_ticker, ":", combined_std)
    print("Portfolio Beta Before Adding", stock_ticker, ":", beta_before)
    print("Portfolio Beta After Adding", stock_ticker, ":", beta_after)
    print("Portfolio Sharpe Ratio Before Adding", stock_ticker, ":", sharpe_before)
    print("Portfolio Sharpe Ratio After Adding", stock_ticker, ":", sharpe_after)
    print("Portfolio Sortino Ratio Before Adding", stock_ticker, ":", sortino_before)
    print("Portfolio Sortino Ratio After Adding", stock_ticker, ":", sortino_after)

    # Visualization output directory
    output_dir = "outputs/stock reporting/"
    visualize_portfolio(portfolio_returns, combined_std, beta_before, beta_after, sharpe_before, sharpe_after, sortino_before, sortino_after, output_dir, show_plot=False)


if __name__ == "__main__":
    main()
