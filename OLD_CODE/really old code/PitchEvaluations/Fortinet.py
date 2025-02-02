import Financial_Ratios as fr
import Data_Retrieval as dr
import datetime as dt
import Data_Analysis_Functions as daf

ticker = ["FTNT"]
start = dt.datetime(year=2021, month=10, day=10)
end = dt.datetime(year=2022, month=10, day=10)
source = 'yahoo'

closes = dr.stock_adjusted_closes(ticker, source, start, end)
log_returns = daf.log_returns(closes)
sharpe = fr.sharpe_ratio(log_returns)
sortino = fr.sortino_ratio(log_returns)
print(sharpe)
print(sortino)

