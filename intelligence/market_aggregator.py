from collections import Counter


def aggregate_market_sentiment(records):
    total = len(records)

    if total == 0:
        return {
            "total_articles": 0,
            "positive_articles": 0,
            "negative_articles": 0,
            "neutral_articles": 0,
            "average_sentiment_score": 0,
            "market_sentiment": "neutral",
            "top_sources": []
        }

    positive = sum(1 for r in records if r.get("sentiment_label") == "positive")
    negative = sum(1 for r in records if r.get("sentiment_label") == "negative")
    neutral = sum(1 for r in records if r.get("sentiment_label") == "neutral")

    avg_score = sum(float(r.get("sentiment_score", 0)) for r in records) / total

    if avg_score > 0.05:
        market_sentiment = "bullish"
    elif avg_score < -0.05:
        market_sentiment = "bearish"
    else:
        market_sentiment = "neutral"

    sources = [r.get("source", "unknown") for r in records]
    top_sources = Counter(sources).most_common(5)

    return {
        "total_articles": total,
        "positive_articles": positive,
        "negative_articles": negative,
        "neutral_articles": neutral,
        "average_sentiment_score": round(avg_score, 4),
        "market_sentiment": market_sentiment,
        "top_sources": [
            {"source": source, "count": count}
            for source, count in top_sources
        ]
    }