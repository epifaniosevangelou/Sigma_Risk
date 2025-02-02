import yfinance as yf
import datetime as dt
import pandas as pd

def fetch_stocks(start, end, tickers_to_fetch):
    """
    Get stock data for a (list of) stock(s): Open, High, Low, CLose, Adj Close and Volume

    :param start: date YYYY-MM-DD
    :param end: date YYYY-MM-DD
    :param tickers_to_fetch: list of tickers

    :return: dictionary of dataframes. Keys of dictionary are tickers.
    """
    data = dict()
    for ticker in tickers_to_fetch:
        try:
            data[ticker] = yf.download(ticker, start, end)
        except Exception:
            print("Could not fetch", ticker)
    return data, list(data.keys())


def tabulate_column(data, column='Close'):
    """
    Turns data into singular Dataframe using only column

    :param data: stock data fetched in form of dictionary (return from 'fetch_stocks')
    :param column: 'Open', 'High', 'Low', 'Close', 'Adj Close', or 'Volume'
    :return:
    """
    table = []
    for stock in data:
        table.append(data[stock][column])

    table = pd.concat(table, axis=1)
    table.columns = list(data.keys())
    return table


if __name__ == "__main__":
    startDate = '2020-01-01'
    endDate = dt.datetime.today().date().__str__()

    stocks, tickers = fetch_stocks(startDate, endDate, ['WDAY', 'CLFD', 'ASML', '9999', 'BEP', 'EDG.V', 'NEE'])

    tabulate_column(stocks, column='Close').to_csv('data.csv')
