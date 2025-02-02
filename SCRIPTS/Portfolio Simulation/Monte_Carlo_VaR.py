# Flexibility: Monte Carlo simulations can
# model complex relationships between assets, including non-linear dependencies
# and fat-tailed distributions, which are common in financial markets.
# Scenario Analysis: You can incorporate a wide range of economic and
# financial scenarios into your simulations, enhancing the robustness of your risk assessment.
# Tail Risk Assessment: Monte Carlo simulations allow
# for a detailed examination of the tail of the portfolio's return distribution,
# providing insights beyond conventional VaR measures.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Step 1: Load the historical stock prices from a CSV file
file_path = 'data/portfolio/historical_prices.csv'  # Update this to your CSV file path
stock_prices = pd.read_csv(file_path, index_col='Date', parse_dates=True)

# Step 2: Calculate daily returns
daily_returns = stock_prices.pct_change().dropna()

# Step 3: Define portfolio weights (assuming equally weighted for simplicity)
weights = np.array([0.02540, 0.02230, 0.01320, 0.01700, 0.04930, 0.02020, 0.00750, 0.03940, 0.02180, 0.02090,
                     0.03590, 0.04590, 0.02160, 0.01440, 0.01670, 0.02330, 0.00970, 0.03320, 0.01690, 0.00930,
                     0.01130, 0.03090, 0.00760, 0.01430, 0.02540, 0.01390, 0.01070, 0.03030, 0.01520])
# Number of simulations and time horizon
n_simulations = 10000
time_horizon = 3  # For example, 1 day
# Monte Carlo simulation
portfolio_simulations = np.zeros(n_simulations)

for i in range(n_simulations):
    random_sample = daily_returns.sample(n=time_horizon, replace=True).values
    simulated_daily_return = np.sum(random_sample * weights, axis=1)
    portfolio_simulations[i] = np.prod(1 + simulated_daily_return) - 1

# Step 4: Calculate the VaR
var_confidence_level = 0.05  # 95% confidence level
VaR = np.percentile(portfolio_simulations, var_confidence_level * 100)

# Print the Value at Risk (VaR)
print(f"Value at Risk (VaR) at {var_confidence_level*100}% confidence level: {VaR*100:.2f}%")

plt.hist(portfolio_simulations, bins=50, alpha=0.75)
plt.xlabel('Portfolio Return')
plt.ylabel('Frequency')
plt.title('Distribution of Simulated Portfolio Returns')
plt.axvline(VaR, color='r', linestyle='dashed', linewidth=2)
output_table_png = "scripts/3_Outputs/portfolio_simulation_plot.png"
plt.savefig(output_table_png, bbox_inches='tight', pad_inches=0.2)
plt.show()
