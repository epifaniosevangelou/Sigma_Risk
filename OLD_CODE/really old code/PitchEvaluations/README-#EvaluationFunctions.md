#EvaluationFunctions.py
Starts by importing necessary Python libraries and modules
            numpy as np: Imports the NumPy library for numerical and mathematical operations.
            pandas as pd: Imports the Pandas library for data manipulation.
            sys: Imports the sys module for system-specific functions.
            sys.path.append('..'): Appends the parent directory to the system path. This is done to import custom modules from a parent directory.
            Data_Analysis_Functions as f: Imports a custom module named Data_Analysis_Functions and aliases it as f. This module likely contains functions for data analysis.
            Portfolio_VaR_Check as var: Imports a custom module named Portfolio_VaR_Check and aliases it as var. This module likely contains functions for calculating Value at Risk (VaR) for a portfolio.
'log_returns' Function: Log returns of a portfolio taking three arguments:
        1. 'closes': DataFrame of CLOSING stock prices.
        2. 'weights': DataFrama of portfolio WEIGHTS
        3. 'extra_tickers': List of EXTRA stock tickers.
            Log returns calculated using 'f.log_returns' function, any row with missing values (NaNs) are dropped. 
            Portfolio log returns are calculated using portfolio weights and the remaining stock prices. 
            Portfolio log returns are inserted into the log returns DataFrame
            The function returns the DataFrame of log returns. 
FINANCIAL RATIOS: 'sharpe_ratio(returns, bench_mark=0)' SHARPE RATIO
                  'bench_mark' argument allows specifying a benchmark return. 
                  'beta(returns, extra_tickers, relative_to)': beta of a portfolio in relation to a stock. Takes the returns series, a list of extra tickers, and the stock to compare to. Beta --> sensitivity to changes.
'evaluate' Function: Computes evaluation metrics for a portfolio, arguments takes:
                'closes': DataFrame CLOSING stock prices
                'weights' DataFrame portfolio WEIGHTS
                'tickers': list of stock tickers in the portfolio.
                'ticker_weights': Weights corresponding to 'tickers'
                'market_ticker': stock ticker of the market index for BETA calculations. 
                Boolean flags for enabling/disabling specific metrics.
                'VaR_of_interest': the level of Value at Risk (VaR) to calculate.
                'x_day_VaR': The number of days for which to calculate VaR. 
                'ticker_sector': Information about the sector of each stock. 
                        The function initializes an empty dictionary called 'results' to store computed metrics. It calculates log returns and inserts them into the dictionary. If enabled it calculates the log returns correlation, Sharpe ratio, Sortino ratio, beta, and incremental VaR using functions defined earlier. The function returns the 'results' dictionary containing various evaluation metrics. 
Code facilitates the evaluation of a portfolio, risk/return measures. 