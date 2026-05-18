def generate_market_explanation(summary):
    """
    Local AI-style reasoning agent.

    It explains market sentiment using Gold layer intelligence.
    No paid API required.
    """

    market_sentiment = summary.get("market_sentiment", "neutral")
    avg_score = summary.get("average_sentiment_score", 0)

    positive = summary.get("positive_articles", 0)
    negative = summary.get("negative_articles", 0)
    neutral = summary.get("neutral_articles", 0)
    total = summary.get("total_articles", 0)

    top_sources = summary.get("top_sources", [])

    if total == 0:
        return (
            "There is not enough market news data available yet. "
            "Run the ingestion, silver, and gold pipelines first."
        )

    if market_sentiment == "bullish":
        reason = (
            "The market is showing bullish sentiment because positive news "
            "coverage is stronger than negative coverage."
        )
    elif market_sentiment == "bearish":
        reason = (
            "The market is showing bearish sentiment because negative news "
            "coverage is outweighing positive coverage."
        )
    else:
        reason = (
            "The market sentiment is neutral because positive and negative "
            "signals are relatively balanced."
        )

    source_text = ""

    if top_sources:
        source_names = [
            source.get("source", "unknown")
            for source in top_sources[:3]
        ]

        source_text = (
            " The strongest news sources contributing to this signal are "
            + ", ".join(source_names)
            + "."
        )

    explanation = (
        f"{reason} "
        f"The system analyzed {total} articles: "
        f"{positive} positive, {negative} negative, and {neutral} neutral. "
        f"The average sentiment score is {avg_score}."
        f"{source_text}"
    )

    return explanation