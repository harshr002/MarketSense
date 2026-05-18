import feedparser
from datetime import datetime, timezone


RSS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "CNBC Markets": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "MarketWatch": "https://feeds.content.dowjones.io/public/rss/mw_topstories"
}


def fetch_financial_news():
    news_records = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:
            news_records.append({
                "source": source,
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published_at": entry.get("published", ""),
                "fetched_at": datetime.now(timezone.utc).isoformat()
            })

    return news_records