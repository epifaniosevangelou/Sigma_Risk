import numpy as np


def sharpe_ratio(returns, bench_mark=0):
    """ time_series will need to be a return series if this Sharpe Ratio formulation is used """
    ratio = (np.mean(returns) - bench_mark) / np.std(returns)
    ratio = np.asarray(ratio)
    # print(np.mean(returns))
    # print(np.std(returns))
    # print("sharpe is ")
    # print(ratio)
    return ratio[0]


def sortino_ratio(returns, bench_mark=0):
    ratio = (np.mean(returns) - bench_mark) / np.std(returns[returns < 0])
    ratio = np.asarray(ratio)
    # print(np.mean(returns))
    # print(np.std(returns[returns < 0]))
    # print("sharpe is ")
    # print(ratio)
    return ratio[0]

