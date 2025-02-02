import numpy as np
import pandas as pd
import yfinance as yf
import warnings
import matplotlib.pyplot as plt
import riskfolio as rp
from scipy.stats import norm
import os

warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:.4%}'.format


# Inputs

# Confidence level in %
confidence_level = 0.05

# Date range
start_date = '2023-11-08'
end_date = '2024-11-08'

# Tickers of assets
tickers = ['FIDU', 'VHT']
tickers.sort()

# Risk free rate
risk_free_rate = 0.04

# Output base directory
base_output_dir = "outputs/Reporting/Stock Reporting"



for ticker in tickers:
    # Fetch historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    base_ticker = ticker.split('.')[0]

    # Calculate Arithmetic returns
    Y = stock_data['Adj Close'].pct_change().dropna()

    # Convert returns Series to DataFrame
    Y = pd.DataFrame(Y) 
    Y.rename(columns={'Adj Close': ticker}, inplace=True) # Set ticker as column name
    #display(Y.head())

    # Define weights as DataFrame
    w = pd.DataFrame(data=[[1.0]], columns=[ticker], index=[0]).T 
    #display(w.T)

    # Create a subdirectory for each ticker
    ticker_output_dir = os.path.join(base_output_dir, ticker)
    os.makedirs(ticker_output_dir, exist_ok=True)


    # Create a separate figure and axis for each ticker's plot
    fig, ax_stat = plt.subplots(figsize=(12, 10), dpi=300)  # Adjust figure size

    # Plotting the basic table
    ax_stat = rp.plot_table(returns=Y,
                   w=w,
                   MAR=risk_free_rate/252,
                   alpha=confidence_level,
                   ax=ax_stat)

    # Adding title with ticker name
    ax_stat.set_title(f'Statistics for {ticker}', fontsize=20, fontweight='bold')  # Increase font size and make it bold

    # Show the plot for each ticker
    plt.savefig(os.path.join(ticker_output_dir, f'{base_ticker}-statistics.png'), bbox_inches='tight', dpi=400)
    plt.close()


    fig, ax_hist = plt.subplots(figsize=(10, 6), dpi=300)

    # Display the histogram plot
    ax_hist = rp.plot_hist(returns=Y,
                  w=w,
                  alpha=confidence_level,
                  bins=50,
                  height=6,
                  width=10,
                  ax=ax_hist)
    
    # Adding title with ticker name
    ax_hist.set_title(f'Returns Histogram for {ticker}', fontsize=20, fontweight='bold')  # Increase font size and make it bold
    
    plt.savefig(os.path.join(ticker_output_dir, f'{base_ticker}-histogram.png'), bbox_inches='tight', dpi=400)    
    plt.close()


    # Create a separate figure and axis for each ticker's plot
    fig, ax_draw = plt.subplots(figsize=(10,8), dpi=300)  # Adjust figure size

        # Adding title with ticker name
    fig.suptitle(f'Drawdown for {ticker}', fontsize=20, fontweight='bold')  # Increase font size and make it bold

    # Plotting the drawdown table
    ax_draw = rp.plot_drawdown(returns=Y,
                    w=w,
                    alpha=confidence_level,
                    height=10,
                    width=10,
                    ax=ax_draw) 

    plt.savefig(os.path.join(ticker_output_dir, f'{base_ticker}-drawdown.png'), bbox_inches='tight', dpi=400)
    plt.close()

    # Create a statistics report in excel format
    rp.excel_report(returns=Y,
                w=w,
                rf=risk_free_rate/252,
                alpha=confidence_level,
                t_factor=252,
                ini_days=1,
                days_per_year=252,
                name=os.path.join(ticker_output_dir, f'{base_ticker}-excel')
    )
