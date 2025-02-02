import pandas as pd
import Data_Analysis_Functions as daf
import scipy.stats
import numpy as np
import datetime as dt
import warnings
import StockPrices.StockFetcher as sf



""" User Inputs:
    Stock Path
    Relevant Dates
    X Day VaR interested in
    % VaR interested in the """

""" Outputs:
X Day Historical  VaR
X Day Parametric  VaR
X Day Monte Carlo VaR
"""

" Initially use 3% as the trigger for 95% VaR to alert Sigma board"


def stock_historical_VaR(stock_prices, VaR_of_interest, xday_VaR):
    stock_returns = daf.log_returns(stock_prices)
    stock_returns = stock_returns.dropna()
    stock_returns = np.asarray(stock_returns)
    # print("Returns")
    # print(stock_returns)

    return np.percentile(stock_returns, VaR_of_interest*100)*np.sqrt(xday_VaR)


def stock_parametric_VaR(stock_prices, VaR_of_interest, xday_VaR):
    stock_returns = daf.log_returns(stock_prices)
    stock_returns = stock_returns.dropna()
    # print(type(stock_returns))
    # print(stock_returns)
    zscore = scipy.stats.norm.ppf(VaR_of_interest)
    print(np.std(stock_returns))
    print(stock_returns.std())
    return stock_returns.mean() + (np.std(stock_returns) * zscore)*np.sqrt(xday_VaR)


def stock_monte_carlo_VaR(stock_prices, VaR_of_interest, xday_VaR, simulations, ):
    portfolio_value = 10000 # Why is this here?
    stock_returns = daf.log_returns(stock_prices)
    stock_returns = stock_returns.dropna()
    means = 0 # mean of each column
    variances = 0 # variance of each column
    covariance_matrix = np.cov(stock_returns, bias=False)
    forecast_array = np.zeros([xday_VaR, simulations])
    for i in range(simulations):
        random_value = np.random.multivariate_normal(means, covariance_matrix, size=xday_VaR)
        _Close = [portfolio_value]
        for j in range(xday_VaR):
            _Return = 0.0
            for g in range(len(weights)):
                _Return +=  random_value[j,g]
                c = _Close[j] * np.exp(_Return)
                list.append(_Close, c)
            forecast_array[j, i] = _Close[j + 1]
    VaR_day = 1 # wtf is this lol
    outcome = np.percentile(forecast_array[VaR_day - 1], VaR_of_interest)
    return (outcome-portfolio_value)/portfolio_value


def marginal_VaR():
    pass
""" Actually just better to use Incremental VaR"""


if __name__ == "__main__":

    """ Parameters"""
    VaR_of_interest = 0.01
    VaR_threshold = 0.03
    x_day_VaR = 1
    start = dt.datetime(year=2021, month=11, day=3)
    end = dt.datetime(year=2022, month=11, day=3)
    # data = pd.read_csv("ProcessedPortfolio.csv")
    # print(data)
    # data = pd.read_csv("../ProcessedPortfolio.csv")

    " Reading in the data "
    # close_prices, f = sf.get_stock_prices(sf.prepare_tickers(data["Ticker"].tolist(), data["Exchange"].tolist()),
    #                                   start, end, False)

    # close_prices = pd.read_csv("stocks-2020_01_01-2021_09_12.csv")
    # close_prices = close_prices.set_index('Date')

    data = pd.read_csv("C:\\Users\\Tom McGrath\\Desktop\\TempUni\\Sigma\\test_data.csv")
    close_prices = data.loc[:, 'DAX']  # just the prices/returns of the series you're interested in
    print(close_prices)

    xDay_historical_VaR = stock_historical_VaR(close_prices, VaR_of_interest, x_day_VaR)
    xDay_parametric_VaR = stock_parametric_VaR(close_prices, VaR_of_interest, x_day_VaR)
    # xDay_montecarlo_VaR = stock_monte_carlo_VaR(close_prices, VaR_of_interest, x_day_VaR)
    print("Historical VaR is ", xDay_historical_VaR)
    print("Parametric VaR is ", xDay_parametric_VaR)
    # print(xDay_montecarlo_VaR)

    if abs(xDay_historical_VaR) > VaR_threshold:
        warnings.warn("Historical VaR is above the set threshold")
        print("Historical VaR is ", xDay_historical_VaR)

    if abs(xDay_parametric_VaR) > VaR_threshold:
        warnings.warn("Parametric VaR is above the set threshold")
        print("Parametric VaR is ", xDay_parametric_VaR)

    # if abs(xDay_historical_VaR) > VaR_threshold:
    #     warnings.warn("Monte Carlo VaR is above the set threshold")
    #     print("Monte Carlo VaR is ", xDay_montecarlo_VaR)

