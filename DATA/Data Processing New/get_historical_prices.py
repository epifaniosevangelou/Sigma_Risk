import pandas as pd
import yfinance as yf

# Define file paths
cleaned_csv_file = "cleaned_portfolio.csv"  # The corrected tickers file
historical_prices_csv = "historical_stock_prices.csv"

# Define the time period (Last 2 years)
start_date = "2022-02-11"
end_date = "2024-02-11"

# **Step 1: Exchange Code Mapping for Yahoo Finance**
exchange_suffix_mapping = {
    'NL': 'AS',  # Amsterdam Stock Exchange
    'DE': 'DE',  # Germany (XETRA)
    'US': '',    # US stocks do not require a suffix
    'GB': 'L',   # London Stock Exchange
    'HK': 'HK',  # Hong Kong Stock Exchange
    'DK': 'CO',  # Copenhagen Stock Exchange
    'BE': 'BR',  # Brussels Stock Exchange
    'ES': 'MC'   # Madrid Stock Exchange
}

# **Step 2: Load the cleaned CSV file**
df = pd.read_csv(cleaned_csv_file, delimiter=";", encoding="utf-8")

# **Step 3: Remove "CASH" from the ticker list**
df = df[df["Ticker"] != "CASH"]

# **Step 4: Fix Ticker Symbols**
def format_ticker(ticker):
    parts = ticker.split("-")

    # If there's only one part, it's likely a US stock (return unchanged)
    if len(parts) == 1:
        return ticker

    # Extract the last part as exchange code
    base_ticker = "-".join(parts[:-1])  # Everything except the last part
    exchange_code = parts[-1]  # Last part is the exchange code

    # If it's a US stock, return it unchanged
    if exchange_code == "US":
        return base_ticker

    # Apply mapping if the exchange code exists
    if exchange_code in exchange_suffix_mapping:
        return f"{base_ticker}.{exchange_suffix_mapping[exchange_code]}"
    
    # If no valid mapping found, return the original ticker
    return ticker  

# Apply the correction
df["Ticker"] = df["Ticker"].astype(str).apply(format_ticker)

# **Step 5: Extract the List of Valid Yahoo Finance Tickers**
tickers = df["Ticker"].dropna().tolist()

# **Step 6: Download Historical Stock Prices**
historical_prices = pd.DataFrame()

for ticker in tickers:
    try:
        print(f"Fetching data for {ticker}...")
        stock_data = yf.download(ticker, start=start_date, end=end_date)["Close"]
        historical_prices[ticker] = stock_data  # Store closing prices
    except Exception as e:
        print(f"⚠️ Could not fetch data for {ticker}: {e}")


# **Step 8: Save to CSV**
historical_prices.to_csv(historical_prices_csv, sep=";")
print(f"✅ Historical prices saved to {historical_prices_csv}")
