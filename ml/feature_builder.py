import os
import json
import glob
import pandas as pd


BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"


def load_latest_file(folder, pattern):
    files = sorted(glob.glob(os.path.join(folder, pattern)))

    if not files:
        raise FileNotFoundError(f"No files found for pattern: {pattern}")

    with open(files[-1], "r") as file:
        return json.load(file)


def build_market_features():
    stock_data = load_latest_file(
        BRONZE_DIR,
        "stock_prices_*.json"
    )

    news_data = load_latest_file(
        SILVER_DIR,
        "silver_news_*.json"
    )

    stock_df = pd.DataFrame(stock_data)
    news_df = pd.DataFrame(news_data)

    if stock_df.empty or news_df.empty:
        raise ValueError("Stock or news data is empty.")

    avg_sentiment = news_df["sentiment_score"].mean()
    positive_count = (news_df["sentiment_label"] == "positive").sum()
    negative_count = (news_df["sentiment_label"] == "negative").sum()
    neutral_count = (news_df["sentiment_label"] == "neutral").sum()

    stock_df["daily_return"] = (
        (stock_df["close"] - stock_df["open"]) / stock_df["open"]
    )

    stock_df["avg_news_sentiment"] = avg_sentiment
    stock_df["positive_news_count"] = positive_count
    stock_df["negative_news_count"] = negative_count
    stock_df["neutral_news_count"] = neutral_count

    stock_df["target_movement"] = stock_df["daily_return"].apply(
        lambda value: 1 if value > 0 else 0
    )

    features = stock_df[
        [
            "ticker",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "daily_return",
            "avg_news_sentiment",
            "positive_news_count",
            "negative_news_count",
            "neutral_news_count",
            "target_movement"
        ]
    ]

    return features


if __name__ == "__main__":
    features = build_market_features()
    print(features)