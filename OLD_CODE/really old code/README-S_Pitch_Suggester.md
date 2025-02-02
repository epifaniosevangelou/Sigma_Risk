#SigmaInvestments

Importing Python modules and functions to conduct evaluations and fetch stock prices:
    'import PitchEvaluations.EvaluationFunctions as eva': imports the 'EvaluationFunctions' module from the 'PitchEvaluations' package and gives it the alias 'eva'
    'import StockPrices.StockFetcher as Fetcher'
    'import pandas as pd': imports Pandas lilbrary, gives alia 'pd'.
    'import datetime as dt'


Reading Portfolio Data
    't = pd.read_csv("ProcessedPortfolio.csv")': reads data from a CSV file "ProcessedPortfolio.csv" and stores it in a Pandas DataFrame called 't'. 
Creating a Unique Portfolio with Mean Weights:
    'portfolio = t.groupby("Ticker").head(1).reset_index()': this code groups the data in the 't' DataFrame by the "Ticker" column, selects the first row for each unique ticker (head(1)), and then resets the index. This operation creates a new DataFrame called "portfolio". 
    'portfolio["Weight in Portfolio"] = t.groupby("Ticker").mean().reset_index()["Weight in Portfolio"]': this line calculates the mean weight for each unique ticker in the original 't' DataFrame and adds this mean weight as a new column called "Weight in Portfolio" to the 'portfolio' DataFrame.
Reading Options Data from "constituents.csv", and stores it in a Pandas Dataframe called 'options'
Removing Stocks Already in the Portfolio:
    'options = options.set_index("Symbol").drop(portfolio["Ticker"], errors='ignore').reset_index()': this code sets the "Symbol" column of the 'options' DataFrame as the index. It then removes rows from the DataFrame where the stock ticker matches those already present in the 'portfolio' DataFrame. The 'errors='ignore'' argument ensures that any errors resulting from attempting to drop non-existent tickers are ignored. Finally, it resets the index of the 'options' DataFrame. 



Defining the 'end' Date:
    'end = dt.date.today()': this line sets the 'end' variable to the current date using 'dt.date.today()'. it represents the date until which stock values will be fetched.
Calculating the 'start' date:
    'start = end - dt.timedelta(days=0.1*365)': this line calculates the start date by substracting 10% of a year from the end date. 
Setting the 'market_ticker':
    'market_ticker = "^GSPC"': this line sets the market_ticker variable to the symbol "^GSPC", which likely represents the S&P 500 index. Used for beta valvulations.
Filter Options Data:
    'options = options[options ["Sector]=="Industrials"].head(5)': this code filters the 'options' DataFrame to include only riws where the "Sector" column has the value "Industrials". It then selects the first 5 rows of the filtered DataFrame using 'hear(5)'. This operation reduces the list of options to those within the "INdustrials" sector and limits it to the top 5 options based on some criteria. 
Extracting Options Tickers:
    'options_tickers = options["Symbol"].tolist()': this line extracts the "Symbol" column from the filtered 'options' DataFrame and converts it into a Python list called 'options_tickers'. These represent the stock symbols.



Preparing Tickers and Exchanges for Fetching:
    'updated_tickers = Fetcher.prepare_tickers(portfolio["Ticker"].tolist()+[market_ticker], portfolio["Exchange"].tolist()+[""])': this line calls the 'prepare_tickers' function from the 'Fetcher' module to prepare a list fo tickers and their corresponding exchanges for fetching stock prices. It combines the tickers from the "Ticker" column of the 'portfolio' DataFrame with the market ticker ('market_ticker') and combines their respective exchanges. This prepares a list of ticker-exhcnage pairs for fetching data. 
Fetching Historical Stock Prices: 
    'portfolio_closes, nf = Fetcher.get_stock_prices(updated_tickers, start, end, True)': this line calls the 'get_stock_prices' function from the 'Fetcher' module to fetch historical stock prices for the prepared tickers. It passes the following arguments:
        'updated_tickers': the list of tickers and exchanges prepared earlier. 
        'start': the start date for fetching historical data. 
        'end': the end date for fetching historical data.
        'True': boolean arguments indicates whether to log the tickers that could not be found/ The result of the fetch operation is stored in 'portfolio_closes', and any tickers that could not be found are logged and stored in 'nf'. 
Printing Stocks Not Found
    'print("Could not find stocks:", nf)': this line prints the tickers of stocks that could not be found in the data fetch operation. 



Preparing Tickers for Fetching:
    'Fetcher.prepare_tickers(options_tickers, [""]*len(options_tickers))': this line calls the 'prepare_tickers' function from the 'Fetcher' module to prepare a list of tickers for fetching data. Uses the 'options_tickers' list and a corresponding list of empty strings ([""]) for exchanges. This prepares a list of ticker-exchange pairs for data fetching. 
Fetching Historical Stock Prices:
    optional_closes, nf = Fetcher.get_stock_prices(...)': this line calls the 'get_stock_prices' function from the 'Fetcher' module to fetch historical stock prices for the prepared tickers. It passes the following arguments:
        'options_tickers': the list of tickers prepared for fetching. 
        'start': the start date for fetching historical data. 
        'end': the end date for fetching historical data.
        'True': boolean arguments indicates whether to log the tickers that could not be found/ The result of the fetch operation is stored in 'optional_closes', and any tickers that could not be found are logged and stored in 'nf'. 
Dropping Stocks Not Found:
    'optional_closes = optional_closes.drop(nf, axis=1)': This line removes columns (tickers) from the optional_closes DataFrame that correspond to tickers that could not be found in the data fetch process. It effectively eliminates stocks that could not be retrieved.
Updating the Options Tickers List:
    'options_tickers = list(set(options_tickers) - set(nf))': updates the 'options_tickers' list by removing tickers that could not be found from the original list. It does so by converting the list to a set, substracting the set of tickers not found and then converting the result back to a list. This ensures that the list only contains tickers for which data was successfully retrieved. 
Printing Stocks Not Found.



Combining Historical Stock Price Data
    'closes = pd.concat([portfolio_closes, optional_closes], axis = 1)': this line concatonates (combines) the historical stock price data from the 'portfolio_closes' and 'optional_closes' DataFrames along the columns (axis=1). This operation effectively combines the stock price data for both portfolio assets and optional assets into a single DataFrame called 'closes'. The columns will represent the tickers, including those from the portoflio and optional assets. 
Evaluating Financial Metrics:
    'r = eva.evaluate(closes=closes, weights=portfolio['Weight in Portofolio '], tickers=options_tickers, market_ticker=market_ticker)': this line calls the 'evaluate' function from the 'eva' module to evaluate various financial metrics using the combined stock price data. It passes the following arguments:
        'closes': The DataFrame containing historical stock price data for all assets.
        'weights=portfolio['Weight in Portofolio ']': The weights of assets in the portfolio, likely representing the allocation of capital to each asset.
        'tickers=options_tickers': The list of tickers for the optional assets (likely stock options).
        'market_ticker=market_ticker': The market index ticker used for beta calculation.
The evaluate function is expected to calculate and return various financial metrics, which may include performance measures like Sharpe ratio, Sortino ratio, beta, and other relevant statistics.
After evaluating the metrics, the results are stored in the variable r.



