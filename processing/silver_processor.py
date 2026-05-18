import os
import json
import uuid
from datetime import datetime, timezone

from processing.text_cleaner import clean_text
from processing.sentiment_analyzer import analyze_sentiment


BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"


def load_latest_news_file():
    """
    Load latest financial news from Bronze.
    """

    files = [
        f for f in os.listdir(
            BRONZE_DIR
        )
        if "financial_news" in f
    ]

    files.sort()

    latest_file = files[-1]

    filepath = os.path.join(
        BRONZE_DIR,
        latest_file
    )

    with open(filepath, "r") as file:
        return json.load(file)


def process_news():
    """
    Bronze → Silver transformation.
    """

    raw_news = load_latest_news_file()

    silver_records = []

    for record in raw_news:

        title = record.get(
            "title",
            ""
        )

        summary = record.get(
            "summary",
            ""
        )

        combined_text = f"{title} {summary}"

        cleaned_text = clean_text(
            combined_text
        )

        sentiment = analyze_sentiment(
            cleaned_text
        )

        processed_record = {
            **record,

            "silver_record_id": str(
                uuid.uuid4()
            ),

            "layer": "silver",

            "cleaned_text": cleaned_text,

            "sentiment_label":
                sentiment[
                    "sentiment_label"
                ],

            "sentiment_score":
                sentiment[
                    "sentiment_score"
                ],

            "processed_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }

        silver_records.append(
            processed_record
        )

    return silver_records


def save_silver(records):
    """
    Save Silver records.
    """

    os.makedirs(
        SILVER_DIR,
        exist_ok=True
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"silver_news_{timestamp}.json"
    )

    filepath = os.path.join(
        SILVER_DIR,
        filename
    )

    with open(filepath, "w") as file:
        json.dump(
            records,
            file,
            indent=2
        )

    print(
        f"Saved {len(records)} records → {filepath}"
    )


if __name__ == "__main__":

    processed_news = process_news()

    save_silver(
        processed_news
    )

    print(
        "Silver processing complete."
    )