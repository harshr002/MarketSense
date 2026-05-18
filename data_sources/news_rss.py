from datetime import datetime, timezone
import yfinance as yf


TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "AMZN", "META"]


def fetch_financial_news():
    news_records = []

    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            news_items = stock.news or []

            print(f"{ticker}: {len(news_items)} news items")

            for item in news_items[:5]:
                content = item.get("content", item)

                title = content.get("title", "")
                summary = content.get("summary", "")
                link = content.get("canonicalUrl", {}).get("url", "")

                provider = content.get("provider", {})
                source = provider.get("displayName", "Yahoo Finance")

                published_at = content.get("pubDate", "")

                if title:
                    news_records.append({
                        "ticker": ticker,
                        "source": source,
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "published_at": published_at,
                        "fetched_at": datetime.now(timezone.utc).isoformat()
                    })

        except Exception as error:
            print(f"Error fetching news for {ticker}: {error}")

    print(f"Total fetched news: {len(news_records)}")

    return news_records