import pandas as pd
import Data_Analysis_Functions as daf
import scipy.stats
import numpy as np
import datetime as dt
import warnings
import StockPrices.StockFetcher as sf
import seaborn as sb
import matplotlib.pyplot as plt

""" User Inputs:
    Portfolio Path
    Relevant Dates
    X Day VaR interested in
    % VaR interested in the """

""" Outputs:
X Day Historical Portfolio VaR
X Day Parametric Portfolio VaR
X Day Monte Carlo Portfolio VaR
"""

" Initially use 3% as the trigger for 95% VaR to alert Sigma board"


def portfolio_historical_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR):
    weights_normalised = weights / weights.sum()
    portfolio_returns = daf.log_returns(portfolio_prices)
    portfolio_returns = portfolio_returns.dropna()
    portfolio_returns = np.asarray(portfolio_returns)
    # print("Weights")
    # print(weights_normalised)
    # print(weights_normalised.shape)
    # print("Returns")
    # print(portfolio_returns)
    # print(portfolio_returns.shape)
    portfolio_return = np.dot(portfolio_returns, weights_normalised)
    return np.percentile(portfolio_return, VaR_of_interest * 100) * np.sqrt(xday_VaR)


def portfolio_parametric_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR):
    weights_normalised = weights / weights.sum()
    portfolio_returns = daf.log_returns(portfolio_prices)
    portfolio_returns = portfolio_returns.dropna()
    # print(type(portfolio_returns))
    # print(portfolio_returns)
    portfolio_return = np.dot(portfolio_returns, weights_normalised)
    portfolio_stdev = np.sqrt(np.dot(weights_normalised.T, np.dot(portfolio_returns.cov(), weights_normalised)))
    zscore = scipy.stats.norm.ppf(VaR_of_interest)
    mean_portfolio_return = portfolio_return.mean()
    return mean_portfolio_return + (portfolio_stdev * zscore) * np.sqrt(xday_VaR)


# Simulate Portfolio outcomes
# def portfolio_monte_carlo_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR, simulations):

# def portfolio_monte_carlo_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR, simulations):
#     # print(weights)
#     # print(portfolio_prices.tail(1))
#     # print(portfolio_prices.iloc[-1])
#     portfolio_value = np.dot(portfolio_prices.iloc[-1], weights.T) # latest portfolio prices* weights
#     # print(portfolio_value)
#     portfolio_returns = daf.log_returns(portfolio_prices)
#     portfolio_returns = portfolio_returns.dropna()
#     means = portfolio_returns.mean(axis=0) # mean return of each portfolio, take the mean of each column of the portfolio returns df
#     # print(means)
#     covariance_matrix = portfolio_returns.cov() # covariance matrix of the portfolio returns df
#     ForecastArray = np.zeros([xday_VaR, simulations])
#     AssetN = len(weights)
#     for i in range(simulations):
#         RandValue = np.random.multivariate_normal(means, covariance_matrix, size=xday_VaR)
#         _Close = [portfolio_value]
#         for j in range(xday_VaR):
#             _Return = 0.0
#             for g in range(AssetN):
#                 _Return += weights[g] * RandValue[j,g]
#                 c = _Close[j] * np.exp(_Return)
#                 list.append(_Close, c)
#             ForecastArray[j, i] = _Close[j + 1]
#     outcome = np.percentile(ForecastArray[xday_VaR-1],VaR_of_interest*100)
#     VAR = (outcome-portfolio_value)/portfolio_value
#     return VAR


def portfolio_monte_carlo_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR, simulations):
    weights = weights / weights.sum()
    # print(weights)
    # print(portfolio_prices.tail(1))
    # print(portfolio_prices.iloc[-1])
    portfolio_value = np.dot(portfolio_prices.iloc[-2], weights.T)  # latest portfolio prices* weights
    print(portfolio_value)
    portfolio_returns = daf.log_returns(portfolio_prices)
    portfolio_returns = portfolio_returns.dropna()
    means = portfolio_returns.mean(
        axis=0)  # mean return of each portfolio, take the mean of each column of the portfolio returns df
    # print(means)
    covariance_matrix = portfolio_returns.cov()  # covariance matrix of the portfolio returns df
    ForecastArray = np.zeros([xday_VaR, simulations])
    AssetN = len(weights)
    for i in range(simulations):
        RandValue = np.random.multivariate_normal(means, covariance_matrix, size=xday_VaR)
        _Close = [portfolio_value]
        for j in range(xday_VaR):
            _Return = 0.0
            for g in range(AssetN):
                _Return += weights[g] * RandValue[j, g]
            c = _Close[j] * np.exp(_Return)
            list.append(_Close, c)
            ForecastArray[j, i] = _Close[j + 1]
    outcome = np.percentile(ForecastArray[xday_VaR - 1], VaR_of_interest * 100)
    # print(outcome)
    # print(portfolio_value)
    VAR = np.log(outcome / portfolio_value)
    # print(VAR)
    return VAR


def incremental_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR, method=0):
    df = pd.DataFrame({'Stock': [], 'Incremental VaR': []})
    portfolio_VaR = portfolio_historical_VaR(portfolio_prices, weights, VaR_of_interest, xday_VaR)
    if method == 0:
        for i in range(len(weights)):
            temp_weights = weights.copy()
            temp_weights[i] = 0
            VaR_without_stock = portfolio_historical_VaR(portfolio_prices, temp_weights, VaR_of_interest, xday_VaR)
            incremental_Var = portfolio_VaR - VaR_without_stock
            df.loc[len(df.index)] = [portfolio_prices.columns[i], incremental_Var]
        return df
    elif method == 1:
        for i in range(len(weights)):
            temp_weights = weights.copy()
            temp_weights[i] = 0
            VaR_without_stock = portfolio_parametric_VaR(portfolio_prices, temp_weights, VaR_of_interest, xday_VaR)
            incremental_Var = portfolio_VaR - VaR_without_stock
            df.loc[len(df.index)] = [portfolio_prices.columns[i], incremental_Var]
        return df
    elif method == 2:
        sims = 100
        for i in range(len(weights)):
            temp_weights = weights.copy()
            temp_weights[i] = 0
            VaR_without_stock = portfolio_monte_carlo_VaR(portfolio_prices, temp_weights, VaR_of_interest, xday_VaR, sims)
            incremental_Var = portfolio_VaR - VaR_without_stock
            df.loc[len(df.index)] = [portfolio_prices.columns[i], incremental_Var]
        return df
    return 0


if __name__ == "__main__":
    " Initially use 3% as the trigger for 95% VaR to alert Sigma board"

    """ Parameters"""
    VaR_of_interest = 0.05
    VaR_threshold = 0.03
    x_day_VaR = 7

    # """ Test Data"""
    # data = pd.read_csv("test_data.csv")
    # close_prices = data.loc[:, 'DAX': "SMI"]  # just the prices/returns of the series you're interested in
    # weights = [0.501428642, 0.498571358]
    # weights = np.asarray(weights)

    " Reading in the data "

    " Getting the Data Via the Fetcher"
    # start = dt.datetime(year=2021, month=11, day=3)
    # end = dt.datetime(year=2022, month=11, day=3)
    # data = pd.read_csv("ProcessedPortfolio.csv")
    # print(data)
    # data = pd.read_csv("../ProcessedPortfolio.csv")
    # close_prices, f = sf.get_stock_prices(sf.prepare_tickers(data["Ticker"].tolist(), data["Exchange"].tolist()),
    #                                    start, end, False)

    " Getting the Data from the CSV"
    close_prices = pd.read_csv("stocks-2022_05_24-2022_11_27.csv")
    close_prices = close_prices.set_index('Date')
    close_prices = close_prices.ffill(axis = 0)

    """ Getting Portfolio Weights"""
    processed_csv = pd.read_csv("ProcessedPortfolio.csv")
    weights = processed_csv['Weight in Portofolio ']
    weights = weights / weights.sum()

    xDay_historical_VaR = portfolio_historical_VaR(close_prices, weights, VaR_of_interest, x_day_VaR)
    print("Historical VaR is ", xDay_historical_VaR)
    xDay_parametric_VaR = portfolio_parametric_VaR(close_prices, weights, VaR_of_interest, x_day_VaR)
    print("Parametric VaR is ", xDay_parametric_VaR)
    xDay_montecarlo_VaR = portfolio_monte_carlo_VaR(close_prices, weights, VaR_of_interest, x_day_VaR, 1000)
    print("Monte Carlo VaR is ", xDay_montecarlo_VaR)

    if abs(xDay_historical_VaR) > VaR_threshold:
        warnings.warn("Historical VaR is above the set threshold")
        print("Historical VaR is ", xDay_historical_VaR)

    if abs(xDay_parametric_VaR) > VaR_threshold:
        warnings.warn("Parametric VaR is above the set threshold")
        print("Parametric VaR is ", xDay_parametric_VaR)

    if abs(xDay_historical_VaR) > VaR_threshold:
        warnings.warn("Monte Carlo VaR is above the set threshold")
        print("Monte Carlo VaR is ", xDay_montecarlo_VaR)


    """ Getting the Correlation and heat map matrix"""
    portfolio_returns = daf.log_returns(close_prices)
    portfolio_returns = portfolio_returns.dropna()
    corr = portfolio_returns.corr()
    corr.to_csv("..CorrelationMatrix.csv", index=False)
    fig = plt.figure(figsize=(10, 5))
    heat_plot = sb.heatmap(corr)
    # heat_plot = sb.heatmap(portfolio_returns.corr(), cmap="YlGnBu", annot=True)
    fig.savefig('corr map.jpg', bbox_inches='tight', dpi=150)
    plt.show()

    incremental_VaRs = incremental_VaR(close_prices, weights, VaR_of_interest, x_day_VaR, 0)
    print(incremental_VaRs)
    incremental_VaRs.to_csv("incremental_VaRs.csv", index=False)

    # 10% at risk 10% of the time - Look for something that doesn't trigger too often but often enough to be valid
    # Mix of time frames, 6month, 1 year, 2year, similar economic climate - look at macro data
    # Maybe scrape dtaa from ING
    #
