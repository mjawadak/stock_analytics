# Stock Trading App Architecture

## Overview
This app provides real-time trading and forecasting for a set of stocks. It fetches historical and real-time data, generates weekly, monthly, and yearly forecasts, and allows users to execute and track trades.

## Key Features
- Select and manage a set of stocks to monitor and trade. Let's start with 100 popular stocks. We can have that saved in a document in the data folder.
- Fetch historical daily data for each stock for the last one year. This can be updated every day. This data is used to get weekly, monthly, and yearly forecasts.
- Fetch real-time data for each stock and keep it saved for the last 7 days based on a rolling window.
- Real-time price updates and trading capability 
- Track all buy/sell transactions and current holdings
- Maintain a portfolio with purchase prices and P&L

## Architecture Plan

### 1. Data Ingestion
- Integrate with stock data APIs (e.g., Alpaca, Alpha Vantage)
- Fetch historical data (daily, weekly, monthly, yearly)
- Fetch real-time prices for selected stocks
- Fetch and integrate publicly available stock ratings and analyst recommendations (e.g., Yahoo Finance, Finnhub, IEX Cloud)

### 2. Forecasting Engine
- Use statistical or ML models to forecast prices (weekly, monthly, yearly)
- Store and update forecasts for each stock

### 3. Trading Engine
- Place real-time buy/sell orders via broker API (e.g., Alpaca)
- Track open positions, purchase prices, and trade history
- Update portfolio and calculate P&L in real time

### 4. Portfolio Management
- Maintain a record of all trades (timestamp, price, quantity, action)
- Track current holdings and their purchase prices
- Calculate and display current portfolio value and performance

### 5. User Interface (optional)
- Dashboard to view stocks, forecasts, and portfolio
- Real-time updates and trade execution

### 6. Storage
- Use a database or files to store historical data, forecasts, and trade history

## Next Steps
1. Set up data ingestion for historical and real-time prices
2. Implement forecasting for each stock
3. Integrate real-time trading and portfolio tracking
4. Build user interface (if required)
5. Test end-to-end workflow