import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# Define necessary functions
def calculate_portfolio_return(weights, returns):
    return np.sum(weights * returns)


def calculate_portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))


def calculate_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate):
    portfolio_return = calculate_portfolio_return(weights, returns)
    portfolio_volatility = calculate_portfolio_volatility(weights, cov_matrix)
    return (portfolio_return - risk_free_rate) / portfolio_volatility


def import_historical_prices(filepath):
    historical_prices = pd.read_csv(filepath, index_col="Date", parse_dates=True)
    return historical_prices


def generate_random_portfolios(returns_portfolio, num_portfolios=10000):
    annualized_returns = returns_portfolio.mean() * 252
    cov_matrix = returns_portfolio.cov() * 252
    num_assets = len(returns_portfolio.columns)
    port_returns = []
    port_volatility = []
    port_weights = []

    for _ in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        port_weights.append(weights)
        returns = np.dot(weights, annualized_returns)
        port_returns.append(returns)
        port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        port_sd = np.sqrt(port_variance)
        ann_port_sd = port_sd * np.sqrt(252)
        port_volatility.append(ann_port_sd)

    data = {"Returns": port_returns, "Volatility": port_volatility}
    for counter, symbol in enumerate(returns_portfolio.columns.tolist()):
        data[symbol + "_weight"] = [w[counter] for w in port_weights]

    portfolios = pd.DataFrame(data)
    return portfolios


def plot_efficient_frontier(
    portfolios, min_vol_port, optimal_risky_port, risk_free_rate
):
    plt.subplots(figsize=[8, 8])
    plt.scatter(
        portfolios["Volatility"],
        portfolios["Returns"],
        marker="o",
        s=10,
        alpha=0.3,
        color="green",
    )
    plt.scatter(
        min_vol_port["Volatility"],
        min_vol_port["Returns"],
        color="y",
        marker="*",
        s=500,
        label="Min Volatility Portfolio",
    )
    plt.plot(
        [1.25, optimal_risky_port["Volatility"]],
        [risk_free_rate, optimal_risky_port["Returns"]],
        linestyle="--",
        color="orange",
        label="Sharpe Ratio Line",
    )
    plt.scatter(
        optimal_risky_port["Volatility"],
        optimal_risky_port["Returns"],
        color="b",
        marker="*",
        s=500,
        label="Max Sharpe Ratio Portfolio",
    )
    plt.xlabel("Risk (Volatility)")
    plt.ylabel("Expected Returns")
    plt.title("Efficient Frontier with Min Volatility and Max Sharpe Ratio Portfolios")
    plt.legend()
    # Save figure to a folder in the codespace
    output_folder = "scripts/Step_3_Outputs/"
    figure_name = "efficient_frontier_plot.png"
    output_path = f"{output_folder}/{figure_name}"
    plt.savefig(output_path)
    plt.show()


def main():
    # Importing historical prices and calculating returns
    historical_prices = import_historical_prices("data/portfolio/historical_prices.csv")
    returns_portfolio = historical_prices.pct_change().dropna()

    # Calculating annualized covariance matrix
    cov_matrix = returns_portfolio.cov() * 252

    # Define your portfolio weights here or load them from an external source
    portfolio_weights = [
        0.02540,
        0.02230,
        0.01320,
        0.01700,
        0.04930,
        0.02020,
        0.00750,
        0.03940,
        0.02180,
        0.02090,
        0.03590,
        0.04590,
        0.02160,
        0.01440,
        0.01670,
        0.02330,
        0.00970,
        0.03320,
        0.01690,
        0.00930,
        0.01130,
        0.03090,
        0.00760,
        0.01430,
        0.02540,
        0.01390,
        0.01070,
        0.03030,
        0.01520,
    ]  # Add your portfolio weights here

    # Calculate portfolio variance and standard deviation
    portfolio_variance = (
        np.transpose(portfolio_weights) @ cov_matrix @ portfolio_weights
    )
    portfolio_std = np.sqrt(portfolio_variance)
    print("Portfolio Variance is: ", portfolio_variance)
    print("Portfolio Standard Deviation is: ", portfolio_std)

    # Generating random portfolios
    portfolios = generate_random_portfolios(returns_portfolio)

    # Finding the portfolio with minimum volatility and maximum Sharpe ratio
    rf = 0.0463  # Define the risk-free rate here
    min_vol_port = portfolios.iloc[portfolios["Volatility"].idxmin()]
    optimal_risky_port = portfolios.iloc[
        ((portfolios["Returns"] - rf) / portfolios["Volatility"]).idxmax()
    ]

    print("Portfolio with Minimum Volatility:")
    print(min_vol_port)
    print("Portfolio with Maximum Sharpe Ratio:")
    print(optimal_risky_port)

    # Plotting
    plot_efficient_frontier(portfolios, min_vol_port, optimal_risky_port, rf)


if __name__ == "__main__":
    main()
