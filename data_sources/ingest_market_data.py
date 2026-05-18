import json
import os
from datetime import datetime, timezone

from data_sources.stock_prices import fetch_stock_prices
from data_sources.news_rss import fetch_financial_news

from processing.bronze_processor import add_bronze_metadata


BRONZE_DIR = "data/bronze"


def save_json(data, filename):
    """
    Save raw/enriched records to Bronze storage.
    """

    os.makedirs(BRONZE_DIR, exist_ok=True)

    filepath = os.path.join(
        BRONZE_DIR,
        filename
    )

    with open(filepath, "w") as file:
        json.dump(
            data,
            file,
            indent=2
        )

    print(
        f"Saved {len(data)} records → {filepath}"
    )


def run_ingestion():
    """
    Main ingestion pipeline.
    """

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S"
    )

    print("Fetching live stock data...")
    raw_stock_data = fetch_stock_prices()

    print("Fetching live financial news...")
    raw_news_data = fetch_financial_news()

    print("Applying Bronze metadata...")

    bronze_stock_data = add_bronze_metadata(
        raw_stock_data,
        "market_prices"
    )

    bronze_news_data = add_bronze_metadata(
        raw_news_data,
        "financial_news"
    )

    print("Saving Bronze layer data...")

    save_json(
        bronze_stock_data,
        f"stock_prices_{timestamp}.json"
    )

    save_json(
        bronze_news_data,
        f"financial_news_{timestamp}.json"
    )

    print("Bronze ingestion complete.")


if __name__ == "__main__":
    run_ingestion()