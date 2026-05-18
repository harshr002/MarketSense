import yfinance as yf
from datetime import datetime, timezone


def to_float(value):
    try:
        if hasattr(value, "iloc"):
            value = value.iloc[0]
        return float(value)
    except Exception:
        return None


def to_int(value):
    try:
        if hasattr(value, "iloc"):
            value = value.iloc[0]
        return int(value)
    except Exception:
        return None


def fetch_stock_prices(tickers=None, period="5d", interval="1d"):
    if tickers is None:
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]

    stock_records = []

    for ticker in tickers:
        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
            group_by="column"
        )

        if data.empty:
            continue

        latest = data.tail(1)

        record = {
            "ticker": ticker,
            "open": to_float(latest["Open"]),
            "high": to_float(latest["High"]),
            "low": to_float(latest["Low"]),
            "close": to_float(latest["Close"]),
            "volume": to_int(latest["Volume"]),
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }

        stock_records.append(record)

    return stock_records