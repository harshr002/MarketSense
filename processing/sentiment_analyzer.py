from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Returns sentiment score + label.
    """

    scores = analyzer.polarity_scores(
        text
    )

    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"

    elif compound <= -0.05:
        label = "negative"

    else:
        label = "neutral"

    return {
        "sentiment_label": label,
        "sentiment_score": compound
    }