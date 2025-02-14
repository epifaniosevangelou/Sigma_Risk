import pandas as pd

# Define file paths
cleaned_csv_file = "cleaned_portfolio.csv"  # Original cleaned portfolio
converted_portfolio_csv = "extra_cleaned_portfolio.csv"  # Output file

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

# **Step 2: Load the cleaned portfolio file**
df = pd.read_csv(cleaned_csv_file, delimiter=";", encoding="utf-8")

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

# **Step 5: Save the updated portfolio with converted tickers**
df.to_csv(converted_portfolio_csv, index=False, sep=";")

print(f"✅ Converted cleaned portfolio saved as {converted_portfolio_csv}")
