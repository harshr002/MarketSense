from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime, timezone

from database.db import Base


class MarketSummary(Base):
    __tablename__ = "market_summaries"

    id = Column(Integer, primary_key=True, index=True)

    total_articles = Column(Integer)
    positive_articles = Column(Integer)
    negative_articles = Column(Integer)
    neutral_articles = Column(Integer)

    average_sentiment_score = Column(Float)
    market_sentiment = Column(String)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )