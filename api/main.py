import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.market_reasoner import generate_market_explanation


app = FastAPI(
    title="MarketSense API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GOLD_DIR = "data/gold"


class UserQuestion(BaseModel):
    question: str


def load_latest_gold_summary():
    files = [
        file
        for file in os.listdir(GOLD_DIR)
        if file.endswith(".json")
    ]

    if not files:
        return None

    files.sort()
    latest_file = files[-1]

    path = os.path.join(
        GOLD_DIR,
        latest_file
    )

    with open(path, "r") as file:
        data = json.load(file)

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
def ask_market(user_input: UserQuestion):
    data = load_latest_gold_summary()

    if not data:
        return {
            "error": "No market intelligence available."
        }

    summary = data["summary"]

    answer = generate_market_explanation(summary, user_input.question)

    return {
        "question": user_input.question,
        "answer": answer,
        "source": "gold_layer_market_intelligence"
    }