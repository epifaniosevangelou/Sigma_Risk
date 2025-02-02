import numpy as np
import pandas as pd
import sys
sys.path.append('..')
import Data_Analysis_Functions as fa
import Portfolio_VaR_Check as var

def log_returns(closes, weights, extra_tickers):
    log_ret = f.log_returns(closes).dropna()
    portfolio_log_returns = f.portfolio_log_returns(closes.drop(columns=extra_tickers), weights).mean(axis=1)
    log_ret.insert(0, "Portfolio", portfolio_log_returns)
    return log_ret


# Financial_Ratios
def sharpe_ratio(returns, bench_mark=0):
    """ time_series will need to be a return series if this Sharpe Ratio formulation is used """
    ratio = (returns.mean(axis=0) - bench_mark) / returns.std()
    return ratio


def sortino_ratio(returns, bench_mark=0):
    ratio = (returns.mean(axis=0) - bench_mark) / returns[returns < 0].std()
    return ratio


def beta(returns, extra_tickers, relative_to):
    comb = extra_tickers + [relative_to]
    cov = returns[comb].cov()[relative_to]
    var = returns[relative_to].var()
    return (cov / var).drop(relative_to)


def evaluate(closes, weights, tickers, ticker_weights, market_ticker, LogRetCor=True, Sharpe=True, Sortino=True, Beta=True, IncVar=True,
             VaR_of_interest = 0.05, x_day_VaR = 1, ticker_sector=None):

    results = dict()
    # Compute all evaluation metrics:
    results["log returns"] = log_returns(closes, weights, tickers+[market_ticker])
    if LogRetCor:
        results["log returns correlation"] = results["log returns"].corr()[
            tickers].transpose()  # .add_prefix("LogRetCor_")
    if Sharpe:
        results["Sharpe ratio"] = sharpe_ratio(results["log returns"][tickers])
    if Sortino:
        results["Sortino ratio"] = sortino_ratio(results["log returns"][tickers])
    if Beta:
        results["Beta"] = beta(results["log returns"], tickers, market_ticker)
    if IncVar:
        results["Inc Var"] = var.incremental_VaR(closes.drop(market_ticker, axis=1), np.array(weights.tolist()+ticker_weights), VaR_of_interest, x_day_VaR, 0)
    return results