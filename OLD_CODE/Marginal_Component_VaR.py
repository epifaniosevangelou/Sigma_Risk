import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_historical_prices():
    return pd.read_csv(
        "data/portfolio/historical_prices.csv", index_col="Date", parse_dates=True
    )


def calculate_portfolio_return(weights, returns):
    return np.sum(weights * returns)


def calculate_portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))


def calculate_var(
    portfolio_exposure,
    portfolio_volatility,
    asset_volatility,
    portfolio_weights,
    cov_matrix,
    vol_p,
):
    var_d = 1.65 * np.sqrt((portfolio_exposure**2) * (portfolio_volatility**2))
    var_i = 1.65 * abs(asset_volatility * (portfolio_exposure * portfolio_weights))
    uvar_p = sum(var_i)
    portfolio_betas = cov_matrix @ portfolio_weights / portfolio_volatility
    asset_exposure = portfolio_weights * portfolio_exposure
    cov_weighted_exposure = cov_matrix @ asset_exposure
    dVaR = 1.65 * cov_weighted_exposure / vol_p
    cVaR = 100 * dVaR * asset_exposure / var_d
    return var_d, uvar_p, cVaR, var_i, dVaR, asset_exposure  # Updated to return dVaR


def bankformat(amount):
    return "${:,.2f}".format(amount)


def plot_component_var(ticker_names, cVaR, historical_prices):
    plt.figure(figsize=(12, 6))
    bar_color = "#0D3580"
    edge_color = "black"
    transparency = 0.7
    plt.bar(
        ticker_names, cVaR, color=bar_color, edgecolor=edge_color, alpha=transparency
    )
    plt.xlabel("Assets", fontsize=12, fontweight="bold")
    plt.ylabel("Component VaR (%)", fontsize=12, fontweight="bold")
    plt.title("Component VaR for Each Asset", fontsize=14, fontweight="bold")
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    output_folder = "scripts/Step_3_Outputs/"
    figure_name = "component_var_chart.png"
    output_path = f"{output_folder}/{figure_name}"
    plt.savefig(output_path)
    plt.show()


def save_var_table(ticker_names, cVaR, asset_exposure, dVaR, var_i, var_d, uvar_p):
    df_var = pd.DataFrame(
        {
            "Ticker": ticker_names,
            "Component VaR (%)": cVaR.round(2),
            "Dollar VaR": (asset_exposure * dVaR).round(2),
            "Individual VaR": var_i.round(2),
        }
    )
    diversified_row = pd.DataFrame(
        {
            "Ticker": ["Diversified Portfolio"],
            "Component VaR (%)": [var_d],
            "Dollar VaR": ["N/A"],
            "Individual VaR": ["N/A"],
        }
    )
    undiversified_row = pd.DataFrame(
        {
            "Ticker": ["Undiversified Portfolio"],
            "Component VaR (%)": [uvar_p],
            "Dollar VaR": ["N/A"],
            "Individual VaR": ["N/A"],
        }
    )
    df_var = pd.concat([diversified_row, undiversified_row, df_var], ignore_index=True)

    # Visualization
    fig, ax = plt.subplots(figsize=(12, len(df_var) * 0.4))  # Adjust size as needed
    ax.axis("off")

    table = ax.table(
        cellText=df_var.values,
        colLabels=df_var.columns,
        cellLoc="center",
        loc="center",
        colColours=["palegreen"]
        * len(df_var.columns),  # Optional: colors for column headers
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size as needed
    table.scale(1.2, 1.2)  # Adjust scaling as needed

    # Apply conditional formatting if desired
    for (i, j), val in np.ndenumerate(df_var.values):
        if j in [1, 2, 3]:  # Assuming these are the columns with numeric values
            table[(i + 1, j)].set_facecolor(
                "yellow" if i % 2 == 0 else "lightblue"
            )  # Example conditional coloring

    plt.tight_layout()
    output_table = "scripts/Step_3_Outputs/var_table.png"
    plt.savefig(output_table, bbox_inches="tight", pad_inches=0.05)
    plt.close()  # Close the plot to prevent it from displaying in notebooks or Python environments


def save_var_table(ticker_names, cVaR, asset_exposure, dVaR, var_i, var_d, uvar_p):
    # Creating DataFrame from the calculated values
    df_var = pd.DataFrame(
        {
            "Ticker": ticker_names,
            "Component VaR (%)": np.round(cVaR, 2),
            "Dollar VaR": np.round(asset_exposure * dVaR, 2),
            "Individual VaR": np.round(var_i, 2),
        }
    )

    # Adding diversified and undiversified portfolio VaR to the DataFrame
    diversified_row = pd.DataFrame(
        {
            "Ticker": ["Diversified Portfolio"],
            "Component VaR (%)": [var_d],
            "Dollar VaR": ["N/A"],
            "Individual VaR": ["N/A"],
        }
    )
    undiversified_row = pd.DataFrame(
        {
            "Ticker": ["Undiversified Portfolio"],
            "Component VaR (%)": [uvar_p],
            "Dollar VaR": ["N/A"],
            "Individual VaR": ["N/A"],
        }
    )
    df_var = pd.concat([diversified_row, undiversified_row, df_var], ignore_index=True)

    # Visualization settings
    fig, ax = plt.subplots(figsize=(12, len(df_var) * 0.4))  # Adjust size as needed
    ax.axis("off")

    # Create the table
    table = ax.table(
        cellText=df_var.values,
        colLabels=df_var.columns,
        cellLoc="center",
        loc="center",
        colColours=["palegreen"] * len(df_var.columns),  # Color for column headers
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size
    table.scale(1.2, 1.2)  # Adjust scaling

    plt.tight_layout()
    output_table = "scripts/Step_3_Outputs/var_table.png"
    plt.savefig(output_table, bbox_inches="tight", pad_inches=0.05)
    plt.show()  # Prevent display in notebooks/interactive environments using plt.close()


def main():
    historical_prices = load_historical_prices()
    returns_portfolio = historical_prices.pct_change().dropna()
    portfolio_weights = np.array(
        [
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
        ]
    )
    portfolio_exposure = 46699.07
    cov_matrix = returns_portfolio.cov()
    # Calculating necessary variables for VaR assessment
    portfolio_return = calculate_portfolio_return(
        portfolio_weights, returns_portfolio.mean()
    )
    portfolio_volatility = calculate_portfolio_volatility(portfolio_weights, cov_matrix)
    asset_volatility = returns_portfolio.std()
    vol_p = np.sqrt((portfolio_exposure**2) * (portfolio_volatility**2))
    var_d, uvar_p, cVaR, var_i, dVaR, asset_exposure = calculate_var(
        portfolio_exposure,
        portfolio_volatility,
        asset_volatility,
        portfolio_weights,
        cov_matrix,
        vol_p,
    )

    ticker_names = list(historical_prices.columns)
    plot_component_var(ticker_names, cVaR, historical_prices)

    # Generating and saving the VaR report/table
    save_var_table(ticker_names, cVaR, asset_exposure, dVaR, var_i, var_d, uvar_p)


if __name__ == "__main__":
    main()
