
import pandas as pd
import yfinance as yf
from datetime import datetime
import time

def get_historical_prices(input_csv_path, output_csv_path):
    # Load the data from the CSV file
    data = pd.read_csv(input_csv_path, delimiter=";")

    # Clean column names by stripping whitespaces
    data.columns = [col.strip() for col in data.columns]

    # Extract and clean tickers, exchanges, and buy dates
    tickers = [ticker.strip() for ticker in data["Ticker"].tolist()]
    exchanges = [exchange.strip() for exchange in data["Exchange"].tolist()]
    buy_dates = (
        pd.to_datetime(data["Buying Date"].str.strip(), format="%d/%m/%Y")
        .dt.strftime("%Y-%m-%d")
        .tolist()
    )

    # Mapping of exchanges to Yahoo Finance suffixes
    exchange_suffixes = {
        "XAMS": ".AS",
        "XFRA": ".DE",
        "XLON": ".L",
        "XNYS": "",
        "XTSE": ".TO",
        "XCSE": ".CO",
        "XSWX": ".SW",
        "XBRU": ".BR",
        "XDUB": ".IR",
        # Add more exchanges as needed
    }

    # Adapt tickers based on their exchange
    adapted_tickers = [
        ticker + exchange_suffixes.get(exchange, "")
        for ticker, exchange in zip(tickers, exchanges)
    ]

    # Create a DataFrame to store the historical prices
    hist_prices = pd.DataFrame()

    # Get today's date
    end_date = datetime.now().strftime("%Y-%m-%d")

    # Initialize lists to store download results and errors
    successful_downloads = []
    failed_downloads = []
    errors = []

    # Fetch data and calculate portfolio values
    for adapted_ticker, buy_date in zip(adapted_tickers, buy_dates):
        print(f"\nFetching data for {adapted_ticker}...")
        time.sleep(0.33)
        try:
            # Fetch data
            prices = yf.download(adapted_ticker, start=buy_date, end=end_date)

            # Validate non-empty data
            if prices.empty:
                print(f"No data found for {adapted_ticker}")
                failed_downloads.append(adapted_ticker)
                errors.append(f"No data found for {adapted_ticker}")
                continue

            # Keep only the adjusted close prices
            prices = prices[["Adj Close"]]

            # Rename the column to the ticker symbol
            prices.columns = [adapted_ticker]

            # Concatenate to the historical prices DataFrame
            if hist_prices.empty:
                hist_prices = prices
            else:
                hist_prices = pd.concat([hist_prices, prices], axis=1)

            # Add to successful downloads
            successful_downloads.append(adapted_ticker)
        except Exception as e:
            print(f"Failed to download data for {adapted_ticker}. Error: {str(e)}")
            failed_downloads.append(adapted_ticker)
            errors.append(str(e))

    # Save the historical prices to a CSV file
    hist_prices.to_csv(output_csv_path)

    # Print summary
    print(f"\nDownload Summary:")
    print(f"Total tickers: {len(adapted_tickers)}")
    print(f"Successful downloads: {len(successful_downloads)}")
    print(f"Failed downloads: {len(failed_downloads)}")

    # Print details of failed downloads
    if failed_downloads:
        print("\nDetails of failed downloads:")
        for ticker, error in zip(failed_downloads, errors):
            print(f"{ticker}: {error}")

if __name__ == "__main__":
    # Example usage
    input_csv_path = "data/portfolio/All_Sectors.csv"  # Adjust the path as needed
    output_csv_path = "data/portfolio/historical_prices.csv"  # Adjust the path as needed
    get_historical_prices(input_csv_path, output_csv_path)
