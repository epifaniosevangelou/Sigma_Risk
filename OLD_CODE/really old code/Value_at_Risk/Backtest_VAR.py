import numpy as np
import datetime as dt
import pandas_datareader.data as web
import datetime as dt
import pandas as pd
import scipy.stats as sp
import matplotlib.pyplot as plt


def stock_adjusted_closes(tickers, source, start, end):
    adjustedCloses = web.DataReader(tickers, source, start, end)['Close']
    return adjustedCloses


def log_returns(stocks):
    logReturns = np.log(stocks / stocks.shift(1))
    return logReturns

#Parametric VAR - function
def P_var(alpha,AveragePortfolioReturn,CovarianceMatrix):
    Variance = np.dot(np.transpose(Weights),np.dot(CovMatrix,Weights))
    Mean = AveragePortfolioReturn
    Z = sp.norm.ppf(alpha)
    VAR = Mean + Z*np.sqrt(Variance)
    return VAR

#Historical VAR - function
def H_var(alpha,PortfolioReturns):
    VAR = np.percentile(PortfolioReturns,100*alpha)
    return VAR


tickers = ['GOOGL', 'MSFT']
" Start and end dates of analysis "
start = dt.datetime(2008, 9, 14)
end = dt.datetime(2022, 4, 14)  # datetime.today().strftime('%Y-%m-%d')
source = 'yahoo'
Asset1 = stock_adjusted_closes("MSFT", source, start, end)
Asset2 = stock_adjusted_closes("AAPL", source, start, end)

r1x = np.array(log_returns(Asset1))
r2x = np.array(log_returns(Asset2))
Weights = [0.5,0.5]

# Get entire series of returns
HistoricalReturnsPortfolio = []
for i in range(len(Asset1)):
    PortfolioReturn = r1x[i] * Weights[0] + r2x[i] * Weights[1]
    HistoricalReturnsPortfolio.append(PortfolioReturn)

#We will assume Asset1 and Asset 2 are arrays of same size
Pvar = []
Hvar = []
VARSamplingPeriod = 365
#Rolling VAR parametric vs historical
for i in range(VARSamplingPeriod,len(Asset1)):
    array1 = Asset1[i-VARSamplingPeriod:i]
    array2 = Asset2[i-VARSamplingPeriod:i]
    # Get Log returns
    r1 = np.array(log_returns(array1))
    r2 = np.array(log_returns(array2))
    # Remove NAN
    r1 = r1[~np.isnan(r1)]
    r2 = r2[~np.isnan(r2)]
    # Calculating the portfolio return at each timestep (Assumes r1 and r2 are lists of the same length)
    Rp = []
    for i in range(len(r1)):
        PortfolioReturn = r1[i] * Weights[0] + r2[i] * Weights[1]
        Rp.append(PortfolioReturn)
    IndividualAssetReturns = np.array([r1, r2])
    PortfolioReturns = np.array(Rp)
    AvgPortfolioReturn = np.mean(PortfolioReturns)
    # Covariance Matrix
    CovMatrix = np.cov(IndividualAssetReturns, bias=False)

    ParametricVar = P_var(0.05,AvgPortfolioReturn,CovMatrix)
    HistoricalVar = H_var(0.05,PortfolioReturns)
    Pvar.append(ParametricVar)
    Hvar.append(HistoricalVar)

#Count outliers
ParametricCount, HistoricalCount = 0, 0
for i in range(VARSamplingPeriod,len(Asset1)):
    if HistoricalReturnsPortfolio[i] < Pvar[i-VARSamplingPeriod]:
        ParametricCount += 1
    if HistoricalReturnsPortfolio[i] < Hvar[i-VARSamplingPeriod]:
        HistoricalCount += 1

print(ParametricCount)
print(HistoricalCount)

plt.plot(HistoricalReturnsPortfolio[VARSamplingPeriod:len(Asset1)])
plt.plot(Pvar)
plt.plot(Hvar)
plt.show()