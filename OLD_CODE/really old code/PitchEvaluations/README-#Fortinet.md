Analysis on stock with ticker 'FTNT' for a specified time period. 
Code begins by importing custom modules and libraries:
    'Financial_Ratios as fr'
    'Data_Retrieval as dr' 
    'datetime as dt'
    'Data_Analysis_Functions as daf'
Variable Initialization:    'ticker': list containing stock ticker symbols  (FTNT)
                            'start': A 'datetime' object. 
                            'end': a 'datetime' object. 
                            'source': string specifying the data source (yahoo in this case)
Fetching Stock Data:
                Code calls the 'dr.stock_adjusted_closes' function from the 'Data_Retrieval' module. 
                Adjusted closing prices are stored in the variable 'closes'
Calculating Log Returns:
                Code calculates log returns for the retrieved stock data using the 'daf.log_returns' function from the 'Data_Analysis_Function' module. Analyses historical performance of a stock/portfolio. 
                Log returns are stored in the variable 'log_returns'
Calculating Financial Rations:
                'sharpe': Sharpe ratio calculated using the 'fr.sharpe_ratio' function from the 'Financial_Ratios' module.
                'sortino': The Sortino Ratio is calculated using the 'fr.sortino_ratio' function from the 'Financial_Ratios' module. 
Printing Results: 
                the code prints the sharpe and sortino ratios.