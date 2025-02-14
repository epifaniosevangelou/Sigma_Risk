import pandas as pd
import numpy as np
import yfinance as yf
import scipy.stats as stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt
# **Step 1: Fetch Historical Price Data**
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Adj Close']

# **Step 2: Compute Daily Returns**
def compute_daily_returns(price_series):
    return price_series.pct_change().dropna()

# **Step 3: Calculate Value at Risk (VaR)**
def calculate_var(returns, confidence_level=0.95):
    # **Gaussian (Parametric) VaR**
    std_dev = returns.std()
    z_score = stats.norm.ppf(1 - confidence_level)
    var_gaussian =  z_score * std_dev

    # **Historical Simulation VaR**
    var_historical = returns.quantile(1 - confidence_level)

    return var_gaussian, var_historical

# **Step 4: Calculate Expected Shortfall (Conditional VaR)**
def calculate_expected_shortfall(returns, confidence_level=0.95):
    var_historical = returns.quantile(1 - confidence_level)
    expected_shortfall = returns[returns <= var_historical].mean()
    return expected_shortfall
# Calculate Worst Realisation 
def calculate_worst_realisation(returns):
    worst_realisation = min(returns)
    return worst_realisation
def calculate_entropic_var(returns, alpha=0.95):
    """
    Compute the Entropic Value at Risk (EVaR) at confidence level alpha.
    
    Parameters:
    - returns: array-like, list of portfolio returns (negative values indicate losses)
    - alpha: float, confidence level (default: 0.95)
    
    Returns:
    - EVaR value
    """
    returns = np.array(returns)
    
    # Define the moment generating function (MGF)-based objective function
    def evar_function(lmbda):
        if lmbda <= 0:
            return np.inf
        mgf = np.mean(np.exp(lmbda * returns))
        return (1 / lmbda) * (np.log(mgf) - np.log(1 - alpha))
    
    # Minimize the EVaR function over λ > 0
    result = minimize(evar_function, x0=1.0, bounds=[(1e-6, None)], method='L-BFGS-B')
    
    if result.success:
        return -result.fun
    else:
        raise ValueError("Optimization failed to compute EVaR.")

#calculate skewness and kurtosis
def calculate_skewness_and_kurtosis(returns):
    skewness = returns.skew()
    kurtosis = returns.kurtosis()
    return skewness, kurtosis

# **Step 7: Main Execution**
tickers = ["C", "COIN", "GS", "O", "NVS","CVS", "ISRG", "AZN"]  # Change this to any stock ticker
start_date = "2024-02-13"
end_date = "2025-02-13"

# **Store results in a DataFrame**
results_list = []

for ticker in tickers: 
    stock_data = get_stock_data(ticker, start_date, end_date)
    returns = compute_daily_returns(stock_data)
    returns = returns.dropna()
    # Compute all risk measures
    var_gaussian, var_historical = calculate_var(returns)
    expected_shortfall = calculate_expected_shortfall(returns)
    worst_realisation = calculate_worst_realisation(returns)
    evar = calculate_entropic_var(returns)
    skewness_kurtosis = calculate_skewness_and_kurtosis(returns)
    # Append results to a list
    results_list.append({
        "Ticker": ticker,
        "Gaussian VaR": var_gaussian,
        "Historical VaR": var_historical,
        "Expected Shortfall": expected_shortfall,
        "Worst Realisation": worst_realisation,
        "Entropic VaR": evar,
        "Skewness": skewness_kurtosis[0],
        "Kurtosis": skewness_kurtosis[1]
    })
    #histograms for each stock with lines for each risk measure
    returns.hist(bins=50, alpha=0.5, color='b', edgecolor='black')
    #use different colours for each risk measure
    plt.axvline(x=var_gaussian, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(x=var_historical, color='g', linestyle='dashed', linewidth=1)
    plt.axvline(x=expected_shortfall, color='y', linestyle='dashed', linewidth=1)
    plt.axvline(x=evar, color='c', linestyle='dashed', linewidth=1)
    plt.title(f'{ticker} Returns Distribution with Risk Measures')
    plt.xlabel('Daily Returns')
    plt.ylabel('Frequency')
    plt.legend(['Gaussian VaR', 'Historical VaR', 'Expected Shortfall', 'Entropic VaR', 'Returns'])
    #save the plot in outputs file
    plt.savefig(f'OUTPUTS/{ticker}_returns_distribution.png')
    plt.close()
    

# Convert list to DataFrame and display
results_df = pd.DataFrame(results_list)
print(results_df)
