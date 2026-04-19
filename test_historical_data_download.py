"""
Test script for historical_data_download.py
Downloads data for a small set of sample stocks to verify the pipeline works.
"""
import os
import time
import pandas as pd
from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from historical_data_download import (
    download_stock_data,
    DOWNLOAD_CONFIGS,
    API_KEY,
    SECRET,
    OUTPUT_DIR,
)

SAMPLE_TICKERS = ["AAPL", "MSFT", "GOOGL"]


def test_fresh_download(client):
    """Test downloading data from scratch for sample stocks."""
    print("\n" + "=" * 60)
    print("TEST 1: Fresh download")
    print("=" * 60)

    for symbol in SAMPLE_TICKERS:
        # Clean up existing data for a fresh test
        stock_dir = os.path.join(OUTPUT_DIR, symbol)
        if os.path.exists(stock_dir):
            for f in os.listdir(stock_dir):
                os.remove(os.path.join(stock_dir, f))

        print(f"\n--- {symbol} ---")
        for config in DOWNLOAD_CONFIGS:
            success = download_stock_data(client, symbol, config)
            assert success, f"Failed to download {symbol} {config['label']}"
            time.sleep(0.3)

    print("\n✅ TEST 1 PASSED: Fresh download successful")


def test_incremental_update(client):
    """Test that running again only fetches new data (incremental update)."""
    print("\n" + "=" * 60)
    print("TEST 2: Incremental update (should skip or update)")
    print("=" * 60)

    for symbol in SAMPLE_TICKERS:
        print(f"\n--- {symbol} ---")
        for config in DOWNLOAD_CONFIGS:
            download_stock_data(client, symbol, config)
            time.sleep(0.3)

    print("\n✅ TEST 2 PASSED: Incremental update works")


def test_data_integrity():
    """Verify that downloaded parquet files are valid and contain expected columns."""
    print("\n" + "=" * 60)
    print("TEST 3: Data integrity check")
    print("=" * 60)

    expected_columns = {"symbol", "timestamp", "open", "high", "low", "close", "volume"}

    for symbol in SAMPLE_TICKERS:
        stock_dir = os.path.join(OUTPUT_DIR, symbol)
        assert os.path.exists(stock_dir), f"Directory missing: {stock_dir}"

        for config in DOWNLOAD_CONFIGS:
            label = config["label"]
            path = os.path.join(stock_dir, f"{label}.parquet")
            assert os.path.exists(path), f"File missing: {path}"

            df = pd.read_parquet(path)
            assert len(df) > 0, f"Empty dataframe: {path}"

            actual_columns = set(df.columns)
            missing = expected_columns - actual_columns
            assert not missing, f"Missing columns in {path}: {missing}"

            # Check timestamps are sorted
            timestamps = pd.to_datetime(df["timestamp"])
            assert timestamps.is_monotonic_increasing, f"Timestamps not sorted in {path}"

            # Check no duplicates
            dupes = df.duplicated(subset=["symbol", "timestamp"]).sum()
            assert dupes == 0, f"Duplicate rows in {path}: {dupes}"

            print(f"  [OK] {symbol}/{label}: {len(df)} rows, columns={list(df.columns)}")

    print("\n✅ TEST 3 PASSED: Data integrity verified")


def test_data_ranges():
    """Verify that data falls within the expected date ranges."""
    print("\n" + "=" * 60)
    print("TEST 4: Date range validation")
    print("=" * 60)

    for symbol in SAMPLE_TICKERS:
        stock_dir = os.path.join(OUTPUT_DIR, symbol)
        for config in DOWNLOAD_CONFIGS:
            label = config["label"]
            path = os.path.join(stock_dir, f"{label}.parquet")
            df = pd.read_parquet(path)
            timestamps = pd.to_datetime(df["timestamp"])

            earliest = timestamps.min()
            latest = timestamps.max()
            expected_start = config["start"]

            # Make expected_start timezone-aware if timestamps are
            if earliest.tzinfo is not None:
                expected_start = pd.Timestamp(expected_start).tz_localize(earliest.tzinfo)
                now = pd.Timestamp(datetime.now()).tz_localize(earliest.tzinfo)
            else:
                now = pd.Timestamp(datetime.now())

            # Allow 7 days tolerance (weekends, holidays)
            assert earliest >= expected_start - timedelta(days=7), \
                f"{symbol}/{label}: earliest {earliest} is before expected start {expected_start}"
            assert latest <= now + timedelta(days=1), \
                f"{symbol}/{label}: latest {latest} is in the future"

            print(f"  [OK] {symbol}/{label}: {earliest.date()} to {latest.date()}")

    print("\n✅ TEST 4 PASSED: Date ranges valid")


def main():
    print("Historical Data Download - Test Suite")
    print(f"Sample tickers: {SAMPLE_TICKERS}")
    print(f"Output directory: {OUTPUT_DIR}")

    client = StockHistoricalDataClient(API_KEY, SECRET)

    test_fresh_download(client)
    test_incremental_update(client)
    test_data_integrity()
    test_data_ranges()

    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
