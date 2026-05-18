import os
import json
from datetime import datetime, timezone

from intelligence.market_aggregator import aggregate_market_sentiment


SILVER_DIR = "data/silver"
GOLD_DIR = "data/gold"


def load_latest_silver_file():
    files = [
        f for f in os.listdir(SILVER_DIR)
        if f.endswith(".json")
    ]

    if not files:
        raise FileNotFoundError("No silver files found. Run silver processor first.")

    files.sort()
    latest_file = files[-1]

    path = os.path.join(SILVER_DIR, latest_file)

    with open(path, "r") as file:
        return json.load(file)


def save_gold_summary(summary):
    os.makedirs(GOLD_DIR, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    output = {
        "layer": "gold",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary
    }

    path = os.path.join(GOLD_DIR, f"market_summary_{timestamp}.json")

    with open(path, "w") as file:
        json.dump(output, file, indent=2)

    print(f"Saved Gold summary → {path}")


def run_gold_generation():
    silver_records = load_latest_silver_file()
    summary = aggregate_market_sentiment(silver_records)
    save_gold_summary(summary)
    print("Gold generation complete.")


if __name__ == "__main__":
    run_gold_generation()