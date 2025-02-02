import pandas_datareader.data as web


def stock_adjusted_closes(tickers, source, start, end):
    adjustedCloses = web.DataReader(tickers, source, start, end)['Adj Close']
    return adjustedCloses


