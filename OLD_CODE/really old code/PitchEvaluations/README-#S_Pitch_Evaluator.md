The notebook begings by Importing Modules and Libraries
    'sys': imports the sys module for system specific functions. 
    'sys.path.append('..'): Appends the parent directory to the system path. Done to import custom modules. 
    'pandas as pd': Imports the Pandas library and aliases it as 'pd' for data manipulation and analysis. 
    'datetime as dt': Imports the 'datetime' module for working with date and time.
    'EvaluationFunctions as eva': Imports a custom module named 'EvaluationFunctions' and aliases it as 'eva'/
    'StockPrices.StockFetcher as Fetcher' imports custom module named 'StockFetcher' from a package called 'StockPrices' and aliases it as Fetcher.
    'matplotlib.pyplot as plt': Imports the Matplotlib library's Pyplot module and aliases as 'plt' for creating plots and visualisations. 
    'seaborn as sb': Imports the Seaborn library and aliases as 'sb' for data visualization enhancements

    'sys.path.append('..')': Modifies the python system path to include the parent directory. 



Reading Portfolio Data:
    'data = pd.read_csv("../ProcessedPortfolio.csv")': Reads data from a CSV file named "ProcessedPortfolio.csv" located in the directory. It assumed that the CSV file contains a portfolio with "Ticker" and "Exchange" columns. The data is loaded into a Pandas DataFrame named 'data'. 
Preparing Tickers for Fetching:
    'portfolio_stock = Fetcher.prepare_tickers(data["Ticker"].to_list(), data["Exchange"].to_list()): This line uses the 'prepare_tickers' function from the custom module 'Fetcher' to prepare a list of stock tickers and their associate exchanged. 
Defining Time Period:
    'end = dt.date.today()': retrieves the current date and stores it as end. 
    'start = end - dt.timedelta(days=1*365)': Calculates start date which is 365 days before the end date. 
Market Ticker for Beta Calculation:
    'market_ticker = "^GSPV": specifies a market ticker symbol, GSPC, which typically represents the S&P 500 index. Benchmark for beta calculation.
Additional Tickers for Evaluation:
    'extra_tickers': List of additional stock tickers.
    'extra_tickers_exchange': list of exchanges corresponding to the additional tickers. 
    'ticker_sector': specifies sector of each ticker. 
Assertion Checks:
    'assert len(extra_tickers) == len(extra_tickers_exchange)': checks that the lengths of the 'extra_tickers' and 'extra_tickers_exchange' are equal.
    'asset len(extra_tickers) == len(ticker_sector)', once again ensuring equality. 



Fetching Historical Stock Prices
    'port_closes, nf = Fetcher.get_stock_prices(...)': calls the 'get_stock_prices' function from the custom module 'Fetcher' to fetch historical stock prices. The function takes arguments:
        First arguments: 'Fetcher.prepare_tickers(data["Ticker"].tolist() + [market_ticker], data["Exchange"].tolist() + [""])' combines the list of portfolio stock tickers and their exchanges from the 'data'DataFrame with an additional market ticker (market_ticker) and an empty string (""), which typically represents the default exchange (here for market index)
        Second argument: 'start' specifies start date.
        Third argument: 'end' specifies end date. 
        Fourth argument: 'True' indicates that you want to include 'not found' tickers in the result. 
Handling "Not Found" Stocks:
    'print("Could not find stocks:", nf)': prints a message for the stocks that are not found. 



Same as the above, but for the Additional Tickers 'extra_tickers'



Merging Historical Stock Price Data:
    'pd.marge(port_closes.reset_index(), pitch_closes.reset_index())' uses the 'pd.merge' function from Pandas to merge two DataFrames:
        'port_closes.reset_index()': The 'reset_index()' method is applied to the 'port_closes' DataFrame. which resets the index of the DataFrame and creates a new default integer index. Done to ensure that "Date" becomes a column in the DataFrame. 
        'pitch_closes.reset_index()': 'reset_index()' method is applied to the 'pitch_closes' DataFrame. 
        'pd.merge' function combines these two DataFrames based on common columns. 
Setting "Date" as Index:    'set_index("Date")': date column will become the DataFrame's index, used for time-based indexing and analysis. 



Calculating Mean Industry Weights:
    'mean_industry_weights = data.groupby("Sector").mean()["Weight in Portfolio"]': calculates the mean weights in the "Weight in Portfolio" colu,n of the 'data' DataFrame grouped by the "Sector" column. It computes the average weight for each sector in the portfolio, resulting in: Pandas Series with sectors as index. 
Calculating Ticker Weights:
    'ticker_weights = []': initializes an empty list called 'ticker_weights' to store the weights for the additional tickers.
    'for i in range(0, len(extra_tickers)): loop iterates over the range of additional tickers:
        'if ticker_secotr is not None and ticker_sector[i]= "":': this condition sector checks if 'ticker_sector' is not None (info provided) and if the sector for the current ticker is not an empty string. 
        Inside the conditional block, it appends the mean weight of the sector associated with the current ticker to the 'ticker_weights' list. 
        If info is not available or sector is empty string, it appends the mean weight of all sectors in the portfolio to the 'ticker_weights' list. 



Evaluating the Portfolio:
    'res = eva.evaluate(closes=closes, weights=data['Weight in Portofolio '], tickers=extra_tickers ticker_weights=ticker_weights, market_ticker=market_ticker)': This line calls the 'evaluation' function from the custom module 'eva' to evaluate the portfolio. It passes several arguments to  the function:
        'closes': historical stock price data.
        'weights': weights of stocks in the portfolio. 
        'tickers': list of additional tickers (extra_tickers) to evaluate. 
        'ticker_weights': calculated weights for the additional tickers based on their sectors or default weights. 
        'market_ticker': market ticker symbol used for beta calculations. 
    Results stored in the 'res' variable.
Accessing Evaluation Results:
    'res.keys()' retrieves the leys from the 'red' dictionary. 



This part of the notebook Tabulates the results of the portfolio evaluation:
Creating an Empty DataFrame for Results:
    'r = pd.DataFrame()': this line initializes an empty Pandas Dataframe to store tabulated results.
Iterating Through Evaluation Results:
    'for key in res:': this loop iterates through the keys in the 'res' dictionary. 
Skipping Certain Metrics:
    'if key == "log returns" or key == "Inc Var": continue': this condition certain metrics depending on their keys (skip "log returns" or "Inc Var".)
Concatenating DataFrames:
    'if insistance(res[key], pd.DataFrame): r = pd.concat([r, res[key]])': this block of code checks if the result associated with the current key is a Pandas DataFrame, and if it is it concatenates (vertical) the DataFrame with the 'r' DataFrame. This is done to combine multiple DataFrames into a single one. 
Inserting Non-DataFrame Results:
    'else: r.insert(0, key, res[key])': if the result associated with the current key is not a DataFrame it inserts that result into the 'r' DataFrame as a new column. 
Transforming and Renaming the DataFrame:
    'r = r.reset_index().rename(columns = {"Symbols":"Tickers"}).set_index("Tickers").transpose()': After collecting all the results, this code resets the index of the 'r' DataFrame, renames the column "Symbols" to "Tickers", and sets the "Tickers" column as the index. Then, it transposes the DataFrame to have metrics as rows and tickers as columns. 
Displaying The Tabulated Results:
    'r.transpose().head()': displayed the first few rows of the tabulated results. It tranposes the DataFrame back to its original orientation and displays the top rows. 



'r.to_csv(str(end)+"-"+"_".join(extra_tickers)+"-Evaluation.csv")': this code used the "to_csv" method of the Pandas DataFrame 'r' to export the data to a CSV file, named based on:
    'str(end)': this converts the 'end' date to a string. 
    '"-"' A hyphen character is included as a separator in the file name. 
    '"_"+"_".join(extra_tickers)"': thid part combines the tickers from the 'extra_tickers' list into a single string separated by underscores("_")
    '"-Evaluation.csv"': This is a suffix that is added to the file name to indicate that it contains evaluation results in CSV format.



Creating a Heatmap for Self-Correlations of Extra Tickers:
    'sizeRatio = len(extra_tickers)/len(extra_tickers)': calculates the 'sizeRatio', intended to adjust the size of the heatmap. However, len(extra_tickers)/len(extra_tickers) always equals 1, so this calculation doesn't impact the size. 
    'size = 5': This sets the size of the heatmap.
    'fig = plt.figure(figsize=(sizeRatio*size, size))': This line creates a Matplotlib figure with a specified size. 
    'heat_plot = sb.heatmap(r.transpose()[extra_tickers])': this code generates a heatmap using Seaborn's 'heatmap' function. It uses the transposed 'r' DataFrame and selects columns corresponding to the tickers in 'extra_tickers'. This heatmap represents the correlation of log returns for the selected tickers against themselves. 
    'plt.title("Correlations of log returns "+", ".join(extra_tickers)+" against themselves")': sets the title of heatmap. 
Creating a Heatmap for Correlations with Portfolio:
    'sizeRatio = len(portfolio_stocks)/len(extra_tickers)': This line calculates another 'sizeRatio' based on the number of portfolio stocks and extra tickers. 
    'size = 2': this sets the size of the heatmap/ 
    'fig = plt.figure(figsize=(sizeRatio*size,size))': this line creates a Matplotlib figure with a size adjusted based on the 'sizeRatio'. 
    'heat_plot = sb.heatmap(r.transpose() [ ["Portfolio"]+portfolio_stocks])': heatmap using Seaborn's 'heatmap' function. Selects columns corresponding to the portfolio and the portfolio stocks and represents the correlation of log returns for the selected tickers against the portoflio. 
    'plt.title("Correlation of log returns of "+", ".join(extra_tickers)+" against portfolio")': this sets the title of heatmap. 



Next, the code creates bar plots to visualize the Sortino ratio, Sharpe ratio, and beta values for the selected tickers. 
Visualizing Sotino and Sharpe Ratios
        The code first selects the "Sortino ratio" and "Sharpe ratio" columns from the transposed 'r'. DataFrame and resets the index. 
        It then uses 'pd.melt' to reshape the data so that the "Tickers" column remains the same, and the "Sortino ratio" and "Sharpe ratio" values are combined into a single "value" to the y-axis, and differentiates between "Sortino ratio" and "Sharpe ratio" using colours.
        'g.axes[0][0].axhline(y = 0, color='black', ls='--', lw=2)' adds a horizontal line at y=0 for reference.
        'plt.title("Sortino and Sharpe Ratio of "+", ".join(extra_tickers))' sets the title for the plot. 
        Finally, 'plt.show()' displays the bar plot. 

Visualizing Beta:
        The code selects the "Beta" column from the transposed 'r' DataFrame and resets the index. 
        It uses 'sb.catplot' again to create a categorical bar plot, mapping "Tickers" to the x-axis and "Beta" to the y-axis. 
        'plt.title("Beta of "+", ".join(extra_tickers))' sets the title for the plot. 
        Finally, plt.show()' displays the bar plot. 
These visualisations aid in comparing Sortino, Share and beta values. 



Creating a Histogram:
    'plt.hist(res["Inc Var"]["Incremental VaR"])': This line generates a histogram using Matplotlib's 'hist' function. It plots the distribution of incremental VaR values from the 'res' dictionary for all stocks. 
Selecting Extra Tickers with Lowest Incremental VaR:
    'inc_var_extra = res["Inc Var"][res["Inc Var"]["Stock"].isin(extra_tickers)].sort_values(by="Incremental VaR")': This code extracts the incremental VaR values for the selected extra tickers from the 'res' dictionary/ It then sorts these values in ascending order of incremental VaR.
Adding Vertical Lines and Labels: 
    'biggestBin = 8': This sets the maximum value for the vertical lines. 
    'steps = biggestBin / len(extra_tickers)': This calculates the step size for positioning the labels.
    The code then iterates through the sorted 'inc_var_extra' DataFrame and does the following for each ticker:
        'plt.axvline(x=xc["Incremental VaR"], color="orange")': adds a vertical line at the incremental VaR value for the current ticker, represented by "xc". 
        'plt.text(xc["Incremental VaR"], biggestBin*0.1+steps*idx, xc["Stock"], color="black", size=13, ha='center', va='center)': This line adds a text label next to the vertical line, displaying the ticker symbol and positioning it based on the step size. 
        'plt.title("Incremental VaR of "+", ".join(extra_tickers)+" with mean of industry weights")': This sets the title for plot. 
Displaying the Plot:
    'plt.show()': this line displays the histogram and the added vertical lines and labels. 