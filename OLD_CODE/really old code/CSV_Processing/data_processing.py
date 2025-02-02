import pandas as pd

# Given the Positions DD.MM.YY.xlsx file => 
# To right end of table:
# Column title: Ticker. Row under: =C5.[Ticker symbol] and drag down
# Column title: Exchange. Row under: =C5.[Exchange abbreviation] and drag down

df = pd.read_excel("old_code/CSV_Processing/Positions 19.11.22.xlsx") # Base csv


def process(data):
    temp = data.copy()
    temp.columns = temp.iloc[2] # Set column names
    endIdx = temp.index[temp['Sector'] == "CASH"].tolist()[0] # Last row of table (Own discretion)

    temp = temp.iloc[3:endIdx-1] # Only keep rows from table
    temp = temp.dropna(how='all').iloc[: , 1:].reset_index(drop=True) # Drop all empty rows + first column
    temp['Optimization Weight (Risk Team)'] = temp['Optimization Weight (Risk Team)'].fillna(-1)
    temp = temp.ffill() # Propagate values down to NaNs (for Sector and Industry columns)
    temp = temp.drop(columns="Company")
    return temp


data = process(df)

data.to_csv("../ProcessedPortfolio.csv", index=False)