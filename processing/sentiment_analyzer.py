from transformers import pipeline


finbert = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)


def analyze_sentiment(text):
    """
    Financial sentiment analysis using FinBERT.
    """

    if not text:
        return {
            "sentiment_label": "neutral",
            "sentiment_score": 0.0
        }

    result = finbert(text[:512])[0]

    label = result["label"].lower()
    score = float(result["score"])

    if label == "positive":
        compound = score
    elif label == "negative":
        compound = -score
    else:
        compound = 0.0

    return {
        "sentiment_label": label,
        "sentiment_score": round(compound, 4)
    }