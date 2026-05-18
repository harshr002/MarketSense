import json
import os
from datetime import datetime, timezone

from data_sources.stock_prices import fetch_stock_prices
from data_sources.news_rss import fetch_financial_news


BRONZE_DIR = "data/bronze"


def save_json(data, filename):
    os.makedirs(BRONZE_DIR, exist_ok=True)

    path = os.path.join(BRONZE_DIR, filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} records -> {path}")


def run_ingestion():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    stock_data = fetch_stock_prices()
    news_data = fetch_financial_news()

    save_json(stock_data, f"stock_prices_{timestamp}.json")
    save_json(news_data, f"financial_news_{timestamp}.json")

    print("Bronze ingestion complete.")


if __name__ == "__main__":
    run_ingestion()