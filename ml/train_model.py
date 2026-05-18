import os
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from ml.feature_builder import build_market_features


MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "market_direction_model.pkl")


def train_market_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = build_market_features()

    feature_columns = [
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
    ]

    X = df[feature_columns]
    y = df["target_movement"]

    if len(df) < 5:
        print("Not enough data for train/test split. Training on available data.")
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        model.fit(X, y)
        accuracy = None
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42
        )

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)

    print(f"Model saved → {MODEL_PATH}")

    if accuracy is not None:
        print(f"Validation accuracy: {accuracy:.2f}")

    return model


if __name__ == "__main__":
    train_market_model()