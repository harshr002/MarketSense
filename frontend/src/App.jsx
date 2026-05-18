import { useEffect, useState } from "react";
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

function App() {
  const [marketData, setMarketData] = useState(null);
  const [question, setQuestion] = useState(
    "Why is the market sentiment like this today?"
  );
  const [answer, setAnswer] = useState("");
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMarketSummary();
  }, []);

  const fetchMarketSummary = async () => {
    try {
      setError("");

      const response = await axios.get(`${API_BASE_URL}/summary`);

      if (response.data?.summary) {
        setMarketData(response.data.summary);
      } else {
        setError("No market summary found. Run the pipeline first.");
      }
    } catch (err) {
      console.error("Summary API error:", err);
      setError("Unable to connect to MarketSense API.");
    }
  };

  const askMarket = async () => {
    try {
      setLoadingAnswer(true);
      setAnswer("Thinking...");

      const response = await axios.post(`${API_BASE_URL}/ask`, {
        question: question,
      });

      if (response.data?.answer) {
        setAnswer(response.data.answer);
      } else if (response.data?.error) {
        setAnswer(response.data.error);
      } else {
        setAnswer("No answer returned from MarketSense API.");
      }
    } catch (err) {
      console.error("Ask API error:", err);
      setAnswer(
        "Unable to connect to MarketSense API. Make sure FastAPI is running on http://127.0.0.1:8000"
      );
    } finally {
      setLoadingAnswer(false);
    }
  };

  if (error) {
    return (
      <main className="app">
        <section className="hero">
          <div className="hero-content">
            <p className="eyebrow">AI Market Intelligence Platform</p>
            <h1>MarketSense</h1>
            <p className="subtitle">{error}</p>
          </div>
        </section>
      </main>
    );
  }

  if (!marketData) {
    return <div className="loading">Loading MarketSense...</div>;
  }

  const sentimentData = [
    { name: "Positive", value: marketData.positive_articles || 0 },
    { name: "Negative", value: marketData.negative_articles || 0 },
    { name: "Neutral", value: marketData.neutral_articles || 0 },
  ];

  const barData = [
    { name: "Positive", articles: marketData.positive_articles || 0 },
    { name: "Negative", articles: marketData.negative_articles || 0 },
    { name: "Neutral", articles: marketData.neutral_articles || 0 },
  ];

  return (
    <main className="app">
      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow">AI Market Intelligence Platform</p>
          <h1>MarketSense</h1>
          <p className="subtitle">
            Real market data converted into sentiment, signals, predictions,
            and explainable intelligence.
          </p>
        </div>

        <div className="mood-card">
          <span>Market Mood</span>
          <strong>{marketData.market_sentiment?.toUpperCase()}</strong>
        </div>
      </section>

      <section className="cards">
        <div className="card">
          <span>Total Articles</span>
          <strong>{marketData.total_articles}</strong>
        </div>

        <div className="card">
          <span>Positive</span>
          <strong>{marketData.positive_articles}</strong>
        </div>

        <div className="card">
          <span>Negative</span>
          <strong>{marketData.negative_articles}</strong>
        </div>

        <div className="card">
          <span>Avg Score</span>
          <strong>{marketData.average_sentiment_score}</strong>
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Sentiment Distribution</h2>

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
          <h2>Article Sentiment Counts</h2>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData}>
              <XAxis dataKey="name" stroke="#d4af37" />
              <YAxis stroke="#d4af37" />
              <Tooltip />
              <Bar dataKey="articles" fill="#d4af37" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="ai-panel">
        <div>
          <p className="eyebrow">AI Reasoning Agent</p>
          <h2>Ask MarketSense</h2>
          <p>
            Ask why the market is bullish, bearish, or neutral based on the Gold
            intelligence layer.
          </p>
        </div>

        <div className="ask-box">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask something about the market..."
          />

          <button onClick={askMarket} disabled={loadingAnswer}>
            {loadingAnswer ? "Thinking..." : "Ask AI"}
          </button>
        </div>

        {answer && <div className="answer">{answer}</div>}
      </section>

      <footer>
        Real Data → Bronze → Silver → Gold → ML → AI Agent → Dashboard
      </footer>
    </main>
  );
}

export default App;