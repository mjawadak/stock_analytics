import requests
import pandas as pd
import time
import os

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '4EC30TZBCCU9OCDT')  # Replace with your API key or set as env variable
BASE_URL = 'https://www.alphavantage.co/query'

tickers = ['AAPL', 'GOOGL', 'MSFT']  # Add more tickers as needed
INTERVAL = '1min'

# Download full intraday data for a ticker
def download_intraday(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': INTERVAL,
        'outputsize': 'full',
        'apikey': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if f'Time Series ({INTERVAL})' in data:
            df = pd.DataFrame.from_dict(data[f'Time Series ({INTERVAL})'], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            df['symbol'] = symbol
            filename = os.path.join('data', f'{symbol}_intraday.csv')
            df.to_csv(filename)
            print(f'Data for {symbol} saved to {filename}')
        else:
            print(f'No data for {symbol}: {data.get("Note", data)}')
    except Exception as e:
        print(f'Error downloading {symbol}: {e}')

def main():
    for symbol in tickers:
        download_intraday(symbol)
        time.sleep(12)  # Alpha Vantage free API rate limit

if __name__ == '__main__':
    main()
