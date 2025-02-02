import pandas as pd
import yfinance as yf

# add file paths
input_path = 'DATA/Portfolio/Sigma Investments Portfolio 16092024.csv'

clean_file_path = 'DATA/Portfolio/clean_portfolio.csv'

price_file_path = 'DATA/Portfolio/all_historical_prices.csv'

returns_file_path = 'DATA/Portfolio/portfolio_returns.csv'

start_date = '2023-09-25'

end_date = '2024-09-25'

# Define the mapping for yahoo finance exchange suffixes
exchange_suffix_mapping = {
    'NL': 'AS',  # Amsterdam Stock Exchange
    'DE': 'DE',  # Germany
    'US': '',    # US stocks have no suffix
    'GB': 'L',   # London Stock Exchange (UK)
    'HK': 'HK',  # Hong Kong Stock Exchange
    'DK': 'CO',  # Copenhagen
    'BE': 'BR'   # Brussels Stock Exchange
}

# Load the uploaded file
with open(input_path, 'r') as file:
    raw_data = file.readlines()

# Process the data and clean it, focusing on Ticker, Industry, and Weight in Portfolio
cleaned_data_correct_column = []

for line in raw_data:
    # Split the line by semicolon
    split_line = line.split(';')
      
    # Check and extract the correct "Weight in Portfolio" column (this time one more to the right)
    if len(split_line) > 1 and split_line[0] != '' and split_line[-5].strip():
        ticker = split_line[0].strip()
        industry = split_line[1].strip()
        weight_portfolio = split_line[-5].strip()  # This should now be the correct column for "Weight in Portfolio"
        cleaned_data_correct_column.append([ticker, industry, weight_portfolio])


# Convert the corrected data into a DataFrame
cleaned_df_correct_column = pd.DataFrame(cleaned_data_correct_column, columns=['Ticker', 'Industry', 'Weight_Portfolio'])

# Fill missing industries
cleaned_df_correct_column['Industry'] = cleaned_df_correct_column['Industry'].replace('', pd.NA).ffill()

# Remove the second title row (index 0) from the cleaned data
final_cleaned_df = cleaned_df_correct_column.drop(index=0).reset_index(drop=True)

# Replace dots with a temporary placeholder, then replace dashes with dots, and finally replace the placeholder with dashes
final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].str.replace('.', 'TEMP_DOT', regex=False)
final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].str.replace('-', 'TEMP_DASH', regex=False)
final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].str.replace('TEMP_DOT', '-', regex=False)
final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].str.replace('TEMP_DASH', '.', regex=False)

# Fix the weight column
final_cleaned_df['Weight_Portfolio'] = final_cleaned_df['Weight_Portfolio'].str.rstrip('%')
final_cleaned_df['Weight_Portfolio'] = final_cleaned_df['Weight_Portfolio'].str.replace(',', '.')
final_cleaned_df['Weight_Portfolio'] = pd.to_numeric(final_cleaned_df['Weight_Portfolio'], errors='coerce')
final_cleaned_df['Weight_Portfolio'] = final_cleaned_df['Weight_Portfolio'] / 100
final_cleaned_df['Weight_Portfolio'] = final_cleaned_df['Weight_Portfolio'].round(4)

def switch_ticker_suffix(ticker):
    base_ticker, exchange_code = ticker.split('.')
    if exchange_code in exchange_suffix_mapping:
        return f"{base_ticker}.{exchange_suffix_mapping[exchange_code]}"
    return ticker

final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].apply(switch_ticker_suffix)
final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].str.rstrip('.')

# Special case: Replace '992.HK' with '0992.HK'
final_cleaned_df['Ticker'] = final_cleaned_df['Ticker'].replace('992.HK', '0992.HK')

print(final_cleaned_df['Ticker'])

# Save the cleaned data to a new CSV file
final_cleaned_df.to_csv(clean_file_path, index=False, sep=';')

# print the sum of the weights
print('Sum of the weights in the portfolio:')
print(final_cleaned_df['Weight_Portfolio'].sum())




# Download historical stock prices for all tickers in the cleaned data

# Use the 'Ticker' column from the final_cleaned_df DataFrame
tickers = final_cleaned_df['Ticker'].to_list()

# Initialize an empty DataFrame to hold the Adj Close prices
adj_close_prices = pd.DataFrame()

# Loop through each ticker and download the Adj Close prices
for ticker in tickers:
    # Download historical data for the current ticker
    historical_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Extract the 'Adj Close' column
    adj_close_prices[ticker] = historical_data['Adj Close']

# Save the 'Adj Close' prices to a new CSV file
adj_close_prices.to_csv(price_file_path, sep=';')

print(f"Historical prices saved to {price_file_path}")



# Calculate the daily returns for each stock in the portfolio
portfolio_returns = adj_close_prices.pct_change().dropna()
portfolio_returns.to_csv(returns_file_path, sep=';')
