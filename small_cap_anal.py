import pandas as pd
import yfinance as yf
import csv
import json
from urllib.error import HTTPError


# clean IWC data
print('scrub scrub scrub')
df = pd.read_csv('IWC.csv')
df_new = df[['symbol', 'name', 'current_mv']]
df_new = df_new.dropna(subset=['symbol'])
df['current_mv'] = pd.to_numeric(df['current_mv'])
df_new['current_mv'] = df_new['current_mv'].apply(lambda x: f"{x:,.0f} USD")
df_new = df_new.sort_values(by='current_mv', ascending=False)


# Remove the row with ADRO.CVR
print('goodbye bad tickers')
df_new = df_new[df_new['symbol'] != 'ADRO.CVR']
df_new = df_new[df_new['symbol'] != 'PIC.UN1']

# Remove any rows with symbols that include a "." or a "-"
print('looks like we got some bad syntax')
# Using a hyphen at the beginning or the end of the character class
df_new = df_new[~df_new['symbol'].str.contains('[.-:]')]

# Escaping the hyphen with a backslash
df_new = df_new[~df_new['symbol'].str.contains('[\.|\-:]')]


# Save as a new CSV File
print('saving new csv')
df_new.to_csv('IWC_new.csv', index=False)

# Open the CSV file and read the tickers into a list
print('lets scrape some data')
with open('IWC_new.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    tickers = [row['symbol'] for row in reader if row['symbol'].strip()]

# Create a JSON file to store the output
print('lets get jason over here')
with open('ticker_info.json', 'w', encoding='utf-8') as f:
    for ticker in tickers:
        # Get the information for the ticker
        try:
            info = yf.Ticker(ticker).info
        except Exception as e:
            print(f'The ticker {ticker} is not recognized by Yahoo Finance.')
            tickers.remove(ticker)

        # Save the information to the JSON file
        f.write(json.dumps(info) + '\n')

# Read the JSON file into a DataFrame
print('new dataframe i hardly know her')
df = pd.read_json('ticker_info.json', lines=True)

