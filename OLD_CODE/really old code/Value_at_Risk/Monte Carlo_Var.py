import numpy as np
import datetime as dt
import pandas_datareader.data as web
import datetime as dt
import pandas as pd
import scipy.stats as sp

tickers = ['GOOGL', 'MSFT']

" Start and end dates of analysis "
start = dt.datetime(2020, 9, 14)
end = dt.datetime(2022, 4, 14)  # datetime.today().strftime('%Y-%m-%d')

source = 'yahoo'


def stock_adjusted_closes(tickers, source, start, end):
    adjustedCloses = web.DataReader(tickers, source, start, end)['Close']
    return adjustedCloses

def log_returns(stocks):
    logReturns = np.log(stocks / stocks.shift(1))
    return logReturns


Asset1 = stock_adjusted_closes("MSFT", source, start, end)
Asset2 = stock_adjusted_closes("AAPL", source, start, end)
AddedAsset = stock_adjusted_closes("NFLX", source, start, end)

# Get Log returns
r1 = np.array(log_returns(Asset1))
r2 = np.array(log_returns(Asset2))
AddedAssetReturn = np.array(log_returns(AddedAsset))

# Remove NAN
r1 = r1[~np.isnan(r1)]
r2 = r2[~np.isnan(r2)]
AddedAssetReturn = AddedAssetReturn[~np.isnan(AddedAssetReturn)]
# Mean and Variance: Asset 1
mu1 = np.mean(r1)
sig1 = np.var(r1, ddof=1)

# Mean and Variance: Asset 2
mu2 = np.mean(r2)
sig2 = np.var(r2, ddof=1)

# Mean and Vriance: Asset 3
mu3 = np.mean(AddedAssetReturn)
sig3 = np.var(AddedAssetReturn, ddof=1)

# Returns of portfolio 1 and 2
PortfolioR1 = np.array([r1, r2])
PortfolioR2 = np.array([r1, r2, AddedAssetReturn])

# Simulate Portfolio outcomes
def MonteCarloSimulation(PortfolioValue,Simulate, NofDays, Means, Weights, CovarianceMatrix):
    ForecastArray = np.zeros([NofDays, Simulate])
    AssetN = len(Weights)
    for i in range(Simulate):
        RandValue = np.random.multivariate_normal(Means, CovarianceMatrix, size=NofDays)
        _Close = [PortfolioValue]
        for j in range(NofDays):
            _Return = 0.0
            for g in range(AssetN):
                _Return += Weights[g] * RandValue[j,g]
                c = _Close[j] * np.exp(_Return)
                list.append(_Close, c)
            ForecastArray[j, i] = _Close[j + 1]
    return ForecastArray

# Conditional value at risk function
def Cvar(PortfolioValue,SimulatedOutcomesArray,Confidence,VarDay,RangeDivide):
    step = (100-Confidence)/RangeDivide
    Var_List = []
    alpha = 0.0
    for i in range(RangeDivide):
        alpha += step
        VAR = (np.percentile(SimulatedOutcomesArray[VarDay-1],alpha)-PortfolioValue)/PortfolioValue
        Var_List.append(VAR)
    Cvar = np.mean(Var_List)
    return Cvar

#Parameters for monte carlo simulation
PortfolioValue = 10000
Simulate = 100000
N_of_days = 7
WeightsPortfolio1 = [0.5, 0.5]
WeightsPortfolio2 = [0.3, 0.3, 0.4]
Means1 = [mu1, mu2]
Means2 = [mu1, mu2, mu3]
CovarianceMatrix1 = np.cov(PortfolioR1, bias=False)
CovarianceMatrix2 = np.cov(PortfolioR2, bias=False)

#Simulated outcomes
OutcomesPortfolio1 = MonteCarloSimulation(PortfolioValue,Simulate, N_of_days, Means1, WeightsPortfolio1, CovarianceMatrix1)
OutcomesPortfolio2 = MonteCarloSimulation(PortfolioValue,Simulate, N_of_days, Means2, WeightsPortfolio2, CovarianceMatrix2)

#Value at risk parameters
ConfidenceLevel = 95
VARday = 7

# Incremental VAR
OutcomeP1= np.percentile(OutcomesPortfolio1[VARday-1],100-ConfidenceLevel)
OutcomeP2= np.percentile(OutcomesPortfolio2[VARday-1],100-ConfidenceLevel)

VAR1 = (OutcomeP1-PortfolioValue)/PortfolioValue
VAR2 = (OutcomeP2-PortfolioValue)/PortfolioValue
IncrementalVar = VAR1-VAR2

# Conditional Value at Risk : Average outcome of a tail event with specified confidence
ConditionalVAR_Portfolio1 = Cvar(PortfolioValue,OutcomesPortfolio1,ConfidenceLevel,VARday,100)

print(VAR1)
print(ConditionalVAR_Portfolio1)


