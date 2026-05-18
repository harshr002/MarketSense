import os
import json

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="MarketSense API",
    version="1.0.0"
)


GOLD_DIR = "data/gold"


class UserQuestion(BaseModel):
    question: str


def load_latest_gold_summary():
    files = [
        f for f in os.listdir(
            GOLD_DIR
        )
        if f.endswith(
            ".json"
        )
    ]

    if not files:
        return None

    files.sort()

    latest_file = files[-1]

    path = os.path.join(
        GOLD_DIR,
        latest_file
    )

    with open(
        path,
        "r"
    ) as file:

        data = json.load(
            file
        )

    return data


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "MarketSense API"
    }


@app.get("/summary")
def get_market_summary():

    data = load_latest_gold_summary()

    if not data:
        return {
            "error": "No market intelligence available."
        }

    return data


@app.post("/ask")
def ask_market(
    user_input: UserQuestion
):

    data = load_latest_gold_summary()

    if not data:
        return {
            "error": "No market intelligence available."
        }

    summary = data[
        "summary"
    ]

    market_sentiment = summary[
        "market_sentiment"
    ]

    avg_score = summary[
        "average_sentiment_score"
    ]

    answer = (
        f"Current market sentiment is "
        f"{market_sentiment}. "
        f"Average sentiment score is "
        f"{avg_score}."
    )

    return {
        "question":
            user_input.question,

        "answer":
            answer
    }