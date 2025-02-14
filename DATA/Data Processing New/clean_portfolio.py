import pandas as pd

# Define file paths
input_excel_file = "DATA/Portfolio/Copy of Sigma Investments Current Holdings 07.02.2025(1).xlsx"  # Replace with your actual Excel file
output_csv_file = "converted_portfolio.csv"

# Load the Excel file and convert it to CSV (picking the correct sheet)
df = pd.read_excel(input_excel_file, sheet_name=0, dtype=str)  # Reads the first sheet

# Save as CSV
df.to_csv(output_csv_file, index=False, sep=";")  # Ensures correct formatting
print(f"✅ Excel successfully converted to CSV: {output_csv_file}")

# Define the new input file
input_csv_file = "converted_portfolio.csv"
cleaned_csv_file = "cleaned_portfolio.csv"

# Step 1: Load CSV
df = pd.read_csv(input_csv_file, delimiter=";", encoding="utf-8", skip_blank_lines=True, header=None)

# Step 2: Find the correct header row
header_row_index = 4  # Adjust if necessary
df.columns = df.iloc[header_row_index]  # Set correct headers
df = df[header_row_index + 1:].reset_index(drop=True)  # Remove unnecessary rows

# Step 3: Remove duplicate "Ticker" columns
df = df.loc[:, ~df.columns.duplicated()]

# Step 4: Rename the first column as "Ticker"
df.rename(columns={df.columns[0]: "Ticker"}, inplace=True)

# Step 5: Trim spaces & fix naming inconsistencies
df.columns = df.columns.str.strip().str.replace('"', '')

# Step 6: Extract relevant columns (Ticker, Industry, Weight in Portfolio)
expected_columns = ["Ticker", "Sector", "Weight in Portfolio"]
actual_columns = [col for col in df.columns if any(expected in col for expected in expected_columns)]

if len(actual_columns) == 3:
    clean_df = df[actual_columns]
    clean_df.columns = ["Ticker", "Industry", "Weight_Portfolio"]
else:
    print("⚠️ Warning: Expected columns not found. Please inspect the output.")
    print(f"Columns Found: {df.columns}")
    exit()

# Step 7: Convert "Weight in Portfolio" to Decimal Format
clean_df["Weight_Portfolio"] = (
    clean_df["Weight_Portfolio"]
    .astype(str)
    .str.replace("%", "")
    .str.replace(",", ".")
    .astype(float)
    / 100
)

# Step 8: Fix Ticker Symbols
clean_df["Ticker"] = clean_df["Ticker"].str.replace(".", "-", regex=False)

# Step 9: Save Cleaned CSV
clean_df.to_csv(cleaned_csv_file, index=False, sep=";")
print(f"✅ Cleaned CSV saved as {cleaned_csv_file}")
