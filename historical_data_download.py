import os
import time
from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed

# Alpaca API credentials
API_KEY = os.environ["ALPACA_API_KEY"]
SECRET = os.environ["ALPACA_SECRET"]

OUTPUT_DIR = "historical_data"

# Top 500 US stocks (S&P 500 tickers)
SP500_TICKERS = [
    "AAPL", "ABBV", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE",
    "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALK",
    "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN",
    "ANET", "ANSS", "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE", "ATO",
    "ATVI", "AVB", "AVGO", "AVY", "AWK", "AXP", "AZO", "BA", "BAC", "BAX",
    "BBWI", "BBY", "BDX", "BEN", "BF.B", "BIIB", "BIO", "BK", "BKNG", "BKR",
    "BLK", "BMY", "BR", "BRK.B", "BRO", "BSX", "BWA", "BXP", "C", "CAG",
    "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL", "CDAY", "CDNS",
    "CDW", "CE", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF",
    "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP",
    "COF", "COO", "COP", "COST", "CPB", "CPRT", "CPT", "CRL", "CRM", "CSCO",
    "CSGP", "CSX", "CTAS", "CTLT", "CTRA", "CTSH", "CTVA", "CVS", "CVX", "CZR",
    "D", "DAL", "DD", "DE", "DFS", "DG", "DGX", "DHI", "DHR", "DIS",
    "DISH", "DLR", "DLTR", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA",
    "DVN", "DXC", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL",
    "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ES", "ESS",
    "ETN", "ETR", "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F",
    "FANG", "FAST", "FBHS", "FCX", "FDS", "FDX", "FE", "FFIV", "FIS", "FISV",
    "FITB", "FLT", "FMC", "FOX", "FOXA", "FRC", "FRT", "FTNT", "FTV", "GD",
    "GE", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC",
    "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HOLX", "HD",
    "PEAK", "HES", "HIG", "HII", "HLT", "HON", "HPE", "HPQ", "HRL", "HSIC",
    "HST", "HSY", "HUM", "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN",
    "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", "ISRG",
    "IT", "ITW", "IVZ", "J", "JBHT", "JCI", "JKHY", "JNJ", "JNPR", "JPM",
    "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KLAC", "KMB", "KMI", "KMX",
    "KO", "KR", "L", "LDOS", "LEN", "LH", "LHX", "LIN", "LKQ", "LLY",
    "LMT", "LNC", "LNT", "LOW", "LRCX", "LUMN", "LUV", "LVS", "LW", "LYB",
    "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ",
    "MDT", "MET", "META", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM",
    "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRK", "MRNA", "MRO", "MS",
    "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", "NDSN",
    "NEE", "NEM", "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP",
    "NTRS", "NUE", "NVDA", "NVR", "NWL", "NWS", "NWSA", "NXPI", "O", "ODFL",
    "OGN", "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", "PARA", "PAYC",
    "PAYX", "PCAR", "PCG", "PEAK", "PEG", "PEP", "PFE", "PFG", "PG", "PGR",
    "PH", "PHM", "PKG", "PKI", "PLD", "PM", "PNC", "PNR", "PNW", "POOL",
    "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PVH", "PWR", "PXD", "PYPL",
    "QCOM", "QRVO", "RCL", "RE", "REG", "REGN", "RF", "RHI", "RJF", "RL",
    "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "SBAC", "SBNY", "SBUX",
    "SCHW", "SEE", "SHW", "SIVB", "SJM", "SLB", "SNA", "SNPS", "SO", "SPG",
    "SPGI", "SRE", "STE", "STT", "STX", "STZ", "SWK", "SWKS", "SYF", "SYK",
    "SYY", "T", "TAP", "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TFX",
    "TGT", "TJX", "TMO", "TMUS", "TPR", "TRGP", "TRMB", "TROW", "TRV", "TSCO",
    "TSLA", "TSN", "TT", "TTWO", "TXN", "TXT", "TYL", "UAL", "UDR", "UHS",
    "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VFC", "VICI", "VLO",
    "VMC", "VNO", "VRSK", "VRSN", "VRTX", "VTR", "VTRS", "VZ", "WAB", "WAT",
    "WBA", "WBD", "WDC", "WEC", "WELL", "WFC", "WHR", "WM", "WMB", "WMT",
    "WRB", "WRK", "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XRAY", "XYL",
    "YUM", "ZBH", "ZBRA", "ZION", "ZTS"
]

# Data download configurations
DOWNLOAD_CONFIGS = [
    {
        "label": "5y_daily",
        "timeframe": TimeFrame.Day,
        "start": datetime.now() - timedelta(days=5 * 365),
        "end": datetime.now(),
    },
    {
        "label": "1y_daily",
        "timeframe": TimeFrame.Day,
        "start": datetime.now() - timedelta(days=365),
        "end": datetime.now(),
    },
    {
        "label": "6m_hourly",
        "timeframe": TimeFrame.Hour,
        "start": datetime.now() - timedelta(days=180),
        "end": datetime.now(),
    },
    {
        "label": "3m_5min",
        "timeframe": TimeFrame(5, TimeFrame.Minute.unit),
        "start": datetime.now() - timedelta(days=90),
        "end": datetime.now(),
    },
]


def download_stock_data(client, symbol, config):
    """Download data for a single stock at a given granularity and save as parquet.
    If local data already exists, only fetch new data since the last stored timestamp.
    """
    import pandas as pd

    label = config["label"]
    stock_dir = os.path.join(OUTPUT_DIR, symbol)
    os.makedirs(stock_dir, exist_ok=True)
    output_path = os.path.join(stock_dir, f"{label}.parquet")

    # Determine the start date: use last stored timestamp if file exists
    fetch_start = config["start"]
    existing_df = None

    if os.path.exists(output_path):
        try:
            existing_df = pd.read_parquet(output_path)
            if "timestamp" in existing_df.columns and not existing_df.empty:
                last_ts = pd.to_datetime(existing_df["timestamp"]).max()
                # Start fetching from the next moment after the last stored bar
                fetch_start = last_ts.replace(tzinfo=None) + timedelta(minutes=1)
                if fetch_start >= datetime.now():
                    print(f"  [UP-TO-DATE] {symbol} {label}")
                    return True
                print(f"  [UPDATE] {symbol} {label}: fetching from {fetch_start.date()}")
            else:
                print(f"  [REDOWNLOAD] {symbol} {label}: no timestamp column found")
        except Exception as e:
            print(f"  [WARN] {symbol} {label}: could not read existing file ({e}), redownloading")

    try:
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=config["timeframe"],
            start=fetch_start,
            end=config["end"],
            feed=DataFeed.IEX,
        )
        bars = client.get_stock_bars(request_params)
        df = bars.df

        if df.empty:
            if existing_df is not None:
                print(f"  [UP-TO-DATE] {symbol} {label}: no new data")
            else:
                print(f"  [WARN] {symbol} {label}: no data returned")
            return existing_df is not None

        # Reset multi-index (symbol, timestamp) to columns
        df = df.reset_index()

        # Append to existing data if present
        if existing_df is not None and not existing_df.empty:
            df = pd.concat([existing_df, df], ignore_index=True)
            df = df.drop_duplicates(subset=["symbol", "timestamp"], keep="last")
            df = df.sort_values("timestamp").reset_index(drop=True)

        # Trim to the configured window (e.g. keep only last 5 years)
        cutoff = config["start"]
        if "timestamp" in df.columns:
            ts = pd.to_datetime(df["timestamp"])
            # Make cutoff timezone-aware if timestamps are
            if ts.dt.tz is not None:
                cutoff = pd.Timestamp(cutoff).tz_localize(ts.dt.tz)
            df = df[ts >= cutoff].reset_index(drop=True)

        df.to_parquet(output_path, index=False)
        print(f"  [OK] {symbol} {label}: {len(df)} rows saved")
        return True

    except Exception as e:
        print(f"  [ERR] {symbol} {label}: {e}")
        return False


def main():
    client = StockHistoricalDataClient(API_KEY, SECRET)

    total = len(SP500_TICKERS)
    for i, symbol in enumerate(SP500_TICKERS, 1):
        print(f"\n[{i}/{total}] Downloading {symbol}...")
        for config in DOWNLOAD_CONFIGS:
            download_stock_data(client, symbol, config)
            time.sleep(0.3)  # Rate limit: ~200 req/min

    print("\n✅ All downloads complete.")


if __name__ == "__main__":
    main()
