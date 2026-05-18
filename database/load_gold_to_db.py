import os
import json
import glob

from database.db import Base, engine, SessionLocal
from database.models import MarketSummary


GOLD_DIR = "data/gold"


def load_latest_gold_file():
    files = sorted(
        glob.glob(
            os.path.join(
                GOLD_DIR,
                "market_summary_*.json"
            )
        )
    )

    if not files:
        raise FileNotFoundError(
            "No Gold summary files found."
        )

    with open(files[-1], "r") as file:
        return json.load(file)


def save_gold_summary_to_db():
    Base.metadata.create_all(bind=engine)

    gold_data = load_latest_gold_file()
    summary = gold_data["summary"]

    db = SessionLocal()

    record = MarketSummary(
        total_articles=summary.get("total_articles", 0),
        positive_articles=summary.get("positive_articles", 0),
        negative_articles=summary.get("negative_articles", 0),
        neutral_articles=summary.get("neutral_articles", 0),
        average_sentiment_score=summary.get("average_sentiment_score", 0),
        market_sentiment=summary.get("market_sentiment", "neutral")
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    print(
        f"Saved Gold summary to DB with id={record.id}"
    )


if __name__ == "__main__":
    save_gold_summary_to_db()