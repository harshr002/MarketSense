def generate_market_explanation(summary, question=""):
    """
    Local AI-style reasoning agent.

    It answers different market questions using Gold layer intelligence.
    No paid API required.
    """

    question = question.lower()

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

    source_names = [
        item.get("source", "unknown")
        for item in top_sources[:3]
    ]

    sources_text = ", ".join(source_names) if source_names else "available news sources"

    if "why" in question:
        if market_sentiment == "bullish":
            return (
                f"The market is bullish because positive news coverage is stronger "
                f"than negative coverage. Out of {total} articles, {positive} were "
                f"positive, {negative} were negative, and {neutral} were neutral. "
                f"The average sentiment score is {avg_score}. Main contributing "
                f"sources include {sources_text}."
            )

        if market_sentiment == "bearish":
            return (
                f"The market is bearish because negative news coverage is outweighing "
                f"positive coverage. Out of {total} articles, {negative} were negative, "
                f"{positive} were positive, and {neutral} were neutral. The average "
                f"sentiment score is {avg_score}. Main contributing sources include "
                f"{sources_text}."
            )

        return (
            f"The market is neutral because positive and negative signals are balanced. "
            f"The system analyzed {total} articles with {positive} positive, "
            f"{negative} negative, and {neutral} neutral articles."
        )

    if "sentiment" in question or "mood" in question:
        return (
            f"The current market sentiment is {market_sentiment}. "
            f"The average sentiment score is {avg_score}, based on {total} analyzed articles."
        )

    if "positive" in question:
        return (
            f"The system found {positive} positive articles out of {total}. "
            f"This contributes to the current {market_sentiment} market sentiment."
        )

    if "negative" in question or "risk" in question:
        return (
            f"The system found {negative} negative articles out of {total}. "
            f"This indicates the current downside risk in the market sentiment layer."
        )

    if "source" in question or "news" in question:
        return (
            f"The top contributing news sources are {sources_text}. "
            f"These sources contributed to the latest Gold layer market intelligence."
        )

    if "summary" in question or "overview" in question:
        return (
            f"Market overview: sentiment is {market_sentiment}, average score is "
            f"{avg_score}, with {positive} positive, {negative} negative, and "
            f"{neutral} neutral articles from {total} total articles."
        )

    return (
        f"MarketSense analyzed {total} articles and detected a {market_sentiment} "
        f"market condition with an average sentiment score of {avg_score}. "
        f"Ask about sentiment, risk, sources, positive news, negative news, or why the market moved."
    )