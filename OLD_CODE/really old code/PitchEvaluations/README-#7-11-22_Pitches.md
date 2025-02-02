#SigmaInvestments



#7-11-22_Pitches.py 
Starts by importing necessary libraries,
'start' and 'end' --> time period,
extra-tickers and extra_tickers_exchange contain additional stock tickers, and associated exchanges
empty dictionary called 'results' and used to store various results and statistics calculated later.
ENSURE that 'extra_tickers' == 'extra_tickers_exchange'
Function 'get_stock_prices' from'StockPrices.StockFetcher' to fetch stock prices, combined with tickers and exchanges from CSV data and 'extra_tickers' lists, historical stock for the introduced time period. Stocks not found --> stored in 'nf'. Prints a message of which stocks are unfound.
Defines 'log_returns(closes,extra_tickers)' and calculates log returns for the portfolio and adds them to the DataFrame,
Importing NumPy
It then defines the Sharpe Ratio and the Sortino Ratio, which both measure risk-adjusted return. Sortino considers only downside risk.
It computes statistics and financial rations
            Log returns for the portfolio + individual stocks
            Correlation of log returns between portfolio and extra tickers
            Sharpe Ratio and Sortino Ratio for the extra tickers
It saves computed results to a CSV file. Combines corr, Sharpe, and Sortino ratios data into a single DataFrame, and saves into a CSV file with a name based on the joined 'extra_tickers'. 