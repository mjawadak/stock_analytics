import requests
import os

def read_keys(key_file):
    with open(key_file, 'r') as f:
        lines = f.read().splitlines()
        return lines[0], lines[1]

# https://api.alpaca.markets
API_KEY = "AKPG5IV4XUJKQEAYYYMKREICER"
SECRET = "9HJf3D6c9e7gxWebrY6bRefQqW8piCzpRXrozLxmC8wX"

BASE_URL = 'https://paper-api.alpaca.markets/v2'
HEADERS = {
    'APCA-API-KEY-ID': "PKKTKUHPPU0OWAUU2TJK",
    'APCA-API-SECRET-KEY': "09NwSsAd0g3PmHeu9UvKDq0iBZNFReHU6JHJIQVV"
}

tickers = ['AAPL', 'GOOGL', 'MSFT']

def get_latest_quote(symbol, account_type='paper'):
    if account_type == 'paper':
        url = f'https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest'
        #url = f"https://paper-api.alpaca.markets/v2/stocks/{symbol}/quotes/latest"
    else:
        url = f'https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        quote = data.get('quote', {})
        price = quote.get('ap', None)  # 'ap' is the ask price
        timestamp = quote.get('t', None)
        print(f'{symbol}: Price={price}, Time={timestamp}')
        return {'symbol': symbol, 'price': price, 'timestamp': timestamp}
    else:
        print(f'Error fetching {symbol}: {response.text}')
        return None

def main():
    for symbol in tickers:
        get_latest_quote(symbol)

if __name__ == '__main__':
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
    from datetime import datetime

    client = StockHistoricalDataClient(API_KEY, SECRET)
    request_params = StockBarsRequest(
        symbol_or_symbols="AAPL",
        timeframe=TimeFrame.Minute,
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 31)
    )
    bars = client.get_stock_bars(request_params)
    print(bars.df)