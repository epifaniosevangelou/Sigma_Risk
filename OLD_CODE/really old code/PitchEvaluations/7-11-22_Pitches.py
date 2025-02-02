import pandas as pd
import datetime as dt
import StockPrices.StockFetcher as Fetcher
import Data_Analysis_Functions as f
import Financial_Ratios as fin_ra

data = pd.read_csv("ProcessedPortfolio.csv")
start = dt.datetime(year=2021, month=11, day=3)
end = dt.datetime(year=2022, month=11, day=3)
extra_tickers = ["PG", "TGT", "KO", "RTX", "CARR", "BA", "HII"]
extra_tickers_exchange = ["", "", "", "", "", "", ""]
results = dict()
assert len(extra_tickers) == len(extra_tickers_exchange)

closes, nf = Fetcher.get_stock_prices(Fetcher.prepare_tickers(data["Ticker"].tolist() + extra_tickers,
                                                              data["Exchange"].tolist() + extra_tickers_exchange),
                                      start, end, True)

print("Could not find stocks:", nf)


def log_returns(closes, extra_tickers):
    log_returns = f.log_returns(closes).dropna()
    portfolio_log_returns = f.portfolio_log_returns(closes.drop(columns=extra_tickers),
                                                    data['Weight in Portofolio ']).mean(axis=1)
    log_returns.insert(0, "Portfolio", portfolio_log_returns)
    return log_returns


# Financial_Ratios
import numpy as np


def sharpe_ratio(returns, bench_mark=0):
    """ time_series will need to be a return series if this Sharpe Ratio formulation is used """
    ratio = (returns.mean(axis=0) - bench_mark) / returns.std()
    return ratio


def sortino_ratio(returns, bench_mark=0):
    ratio = (returns.mean(axis=0) - bench_mark) / returns[returns < 0].std()
    return ratio


# Compute all statistics/other
results["log returns"] = log_returns(closes, extra_tickers)
results["log returns correlation"] = results["log returns"].corr()[extra_tickers]
results["sharpe ratio"] = sharpe_ratio(results["log returns"][extra_tickers])
results["sortino ratio"] = sortino_ratio(results["log returns"][extra_tickers])

# saving to csv
r = results["log returns correlation"].transpose()
r.insert(0, "Sharpe Ratio", results["sharpe ratio"])
r.insert(0, "Sortino Ratio", results["sortino ratio"])
r = r.transpose()
r.to_csv("_".join(extra_tickers)+"-Corr-Sharpe-Sortino.csv")
