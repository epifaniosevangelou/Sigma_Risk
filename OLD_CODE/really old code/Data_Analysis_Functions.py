import numpy as np
import pandas as pd

""" These two functions don't work atm"""
# def arithmetic_returns1(stocks):
#     arithmetic_returns = (stocks-stocks.shift(1))/stocks.shift(1)
#     return arithmetic_returns
#
#
# def arithmatic_returns2(stocks):
#     arithmetic_returns = (stocks[1:len(stocks)-1]-stocks[0:len(stocks)-2]/stocks[0:len(stocks)-2]
#     return arithmetic_returns


def arithmethic_returns(stocks):
    return stocks.pct_change()


def log_returns(stocks):
    logReturns = np.log(stocks / stocks.shift(1))
    return logReturns


def portfolio_log_returns(closes, weights):
    weights_normalised = weights / weights.sum()

    logReturns = log_returns(closes)

    logReturns = logReturns.dropna()

    np_weights_normalised = np.asarray(weights_normalised)

    np_logreturns = np.asarray(logReturns)

    portfolio_returns = np_logreturns * np_weights_normalised
    return portfolio_returns