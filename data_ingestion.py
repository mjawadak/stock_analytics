import requests
import pandas as pd
import time
import os

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '4EC30TZBCCU9OCDT')  # Replace with your API key or set as env variable
BASE_URL = 'https://www.alphavantage.co/query'

# List of stock symbols to fetch
tickers = ['AAPL', 'GOOGL', 'MSFT']

# Function to fetch real-time data for a symbol
def fetch_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'Time Series (1min)' in data:
            df = pd.DataFrame.from_dict(data['Time Series (1min)'], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            df['symbol'] = symbol
            return df
        else:
            print(f"No data for {symbol}: {data.get('Note', data)}")
            return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def fetch_latest_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'Time Series (1min)' in data:
            timeseries = data['Time Series (1min)']
            latest_timestamp = max(timeseries.keys())
            latest_data = timeseries[latest_timestamp]
            price = float(latest_data['4. close'])
            return {
                'symbol': symbol,
                'timestamp': latest_timestamp,
                'price': price
            }
        else:
            print(f"No data for {symbol}: {data.get('Note', data)}")
            return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def main():
    latest_prices = []
    for symbol in tickers:
        result = fetch_latest_price(symbol)
        if result:
            latest_prices.append(result)
        time.sleep(12)  # Alpha Vantage free API rate limit
    if latest_prices:
        df = pd.DataFrame(latest_prices)
        df.to_csv('latest_prices.csv', mode='w', index=False)
        print('Latest prices saved to latest_prices.csv')
    else:
        print('No latest prices fetched.')

if __name__ == '__main__':
    main()
