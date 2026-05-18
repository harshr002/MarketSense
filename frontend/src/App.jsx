import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
} from "recharts";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

const WATCHLIST = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "AMZN", "META"];

function App() {
  const [marketData, setMarketData] = useState(null);
  const [question, setQuestion] = useState("Why is the market sentiment like this today?");
  const [answer, setAnswer] = useState("");
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [ticker, setTicker] = useState("");

  useEffect(() => {
    fetchMarketSummary();
  }, []);

  const fetchMarketSummary = async () => {
    try {
      setLoadingSummary(true);
      const response = await axios.get(`${API_BASE_URL}/summary`);
      setMarketData(response.data.summary);
    } catch (error) {
      console.error("Summary API error:", error);
    } finally {
      setLoadingSummary(false);
    }
  };

  const askMarket = async () => {
    try {
      setLoadingAnswer(true);
      setAnswer("Thinking through the Gold intelligence layer...");

      const response = await axios.post(`${API_BASE_URL}/ask`, {
        question,
      });

      setAnswer(response.data.answer || response.data.error || "No answer returned.");
    } catch (error) {
      console.error("Ask API error:", error);
      setAnswer("Unable to connect to MarketSense API. Make sure FastAPI is running.");
    } finally {
      setLoadingAnswer(false);
    }
  };

  const sentimentData = useMemo(() => {
    if (!marketData) return [];

    return [
      { name: "Positive", value: marketData.positive_articles || 0 },
      { name: "Negative", value: marketData.negative_articles || 0 },
      { name: "Neutral", value: marketData.neutral_articles || 0 },
    ];
  }, [marketData]);

  const sectorCards = useMemo(() => {
    if (!marketData) return [];

    const mood = marketData.market_sentiment || "neutral";

    return [
      { sector: "Technology", signal: mood, risk: mood === "bearish" ? "High" : "Moderate" },
      { sector: "Consumer", signal: "neutral", risk: "Moderate" },
      { sector: "AI & Semiconductors", signal: mood, risk: mood === "bullish" ? "Low" : "Elevated" },
      { sector: "Macro", signal: mood, risk: mood === "bearish" ? "High" : "Balanced" },
    ];
  }, [marketData]);

  const filteredWatchlist = WATCHLIST.filter((item) =>
    item.toLowerCase().includes(ticker.toLowerCase())
  );

  if (!marketData) {
    return (
      <main className="loading-screen">
        <div className="loader"></div>
        <h2>Loading MarketSense...</h2>
        <p>Connecting to FastAPI and Gold intelligence layer.</p>
      </main>
    );
  }

  return (
    <main className="app">
      <section className="hero">
        <div>
          <p className="eyebrow">AI Market Intelligence Platform</p>
          <h1>MarketSense</h1>
          <p className="subtitle">
            Real market data transformed into sentiment signals, ML predictions,
            and explainable AI intelligence.
          </p>
        </div>

        <div className="hero-actions">
          <div className="mood-card">
            <span>Market Mood</span>
            <strong>{marketData.market_sentiment?.toUpperCase()}</strong>
          </div>

          <button className="refresh-btn" onClick={fetchMarketSummary}>
            {loadingSummary ? "Refreshing..." : "Refresh Live Data"}
          </button>
        </div>
      </section>

      <section className="cards">
        <div className="card">
          <span>Total Articles</span>
          <strong>{marketData.total_articles}</strong>
          <small>News analyzed</small>
        </div>

        <div className="card">
          <span>Positive</span>
          <strong>{marketData.positive_articles}</strong>
          <small>Bullish signals</small>
        </div>

        <div className="card">
          <span>Negative</span>
          <strong>{marketData.negative_articles}</strong>
          <small>Risk signals</small>
        </div>

        <div className="card">
          <span>Avg Score</span>
          <strong>{marketData.average_sentiment_score}</strong>
          <small>FinBERT sentiment score</small>
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <div className="panel-header">
            <h2>Sentiment Distribution</h2>
            <span>Gold Layer</span>
          </div>

          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={sentimentData} dataKey="value" outerRadius={95} label>
                <Cell fill="#d4af37" />
                <Cell fill="#8b0000" />
                <Cell fill="#9ca3af" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Article Sentiment Counts</h2>
            <span>Analytics</span>
          </div>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sentimentData.map((x) => ({ name: x.name, articles: x.value }))}>
              <XAxis dataKey="name" stroke="#d4af37" />
              <YAxis stroke="#d4af37" />
              <Tooltip />
              <Bar dataKey="articles" fill="#d4af37" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="product-grid">
        <div className="panel">
          <div className="panel-header">
            <h2>Stock Watchlist</h2>
            <span>Search</span>
          </div>

          <input
            className="ticker-search"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Search ticker e.g. NVDA"
          />

          <div className="watchlist">
            {filteredWatchlist.map((symbol) => (
              <div className="watch-card" key={symbol}>
                <strong>{symbol}</strong>
                <span>{marketData.market_sentiment}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Sector Intelligence</h2>
            <span>Signals</span>
          </div>

          <div className="sectors">
            {sectorCards.map((item) => (
              <div className="sector-card" key={item.sector}>
                <div>
                  <strong>{item.sector}</strong>
                  <span>{item.signal}</span>
                </div>
                <p>Risk: {item.risk}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="ai-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">AI Reasoning Agent</p>
            <h2>Ask MarketSense</h2>
          </div>
          <span>Question-aware responses</span>
        </div>

        <p className="ai-help">
          Ask about sentiment, risk, sources, negative news, positive news, or market overview.
        </p>

        <div className="ask-box">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask something about market sentiment..."
          />

          <button onClick={askMarket} disabled={loadingAnswer}>
            {loadingAnswer ? "Thinking..." : "Ask AI"}
          </button>
        </div>

        {answer && (
          <div className={`answer ${loadingAnswer ? "pulse" : ""}`}>
            {answer}
          </div>
        )}
      </section>

      <footer>
        Real Data → Bronze → Silver → Gold → ML → AI Agent → Dashboard
      </footer>
    </main>
  );
}

export default App;