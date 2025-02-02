import pandas as pd

# Load the data from the CSV file
file_path = "data/portfolio/All_Sectors.csv"  # Adjust the path as needed
data = pd.read_csv(file_path, delimiter=";")

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

# Create a DataFrame to store the additional information
additional_info = pd.DataFrame()

# Extract market caps, share prices, target prices, and header as industry types
# Convert "Market Cap," "Share Price," and "Target Price" columns to numeric
# Convert "Header" columns to string
market_caps = pd.to_numeric(data["Market Cap"], errors="coerce")
share_prices = pd.to_numeric(data["Share Price"].str.replace(',', '.'), errors="coerce")
target_prices = pd.to_numeric(data["Target Price"].str.replace(',', '.'), errors="coerce")
industry_types = data["Header"].astype(str)
# Calculate the "Current Prediction" column as the percentage change
current_prediction = ((target_prices - share_prices) / share_prices)

# Create a DataFrame to store the extracted information
additional_info["Ticker"] = adapted_tickers
additional_info["Market Cap"] = market_caps
additional_info["Share Price"] = share_prices
additional_info["Target Price"] = target_prices
additional_info["Current Prediction"] = current_prediction
additional_info["Industry"] = industry_types

# Save the additional information to a CSV file
additional_info.to_csv("data/portfolio/additional_info.csv", index=False)

# Print summary
print(f"Additional information has been saved to 'additional_info.csv'.")
