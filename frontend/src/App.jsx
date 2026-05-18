import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [marketData, setMarketData] = useState(null);

  useEffect(() => {
    fetchMarketSummary();
  }, []);

  const fetchMarketSummary = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/summary"
      );

      setMarketData(
        response.data.summary
      );

    } catch (error) {
      console.error(
        error
      );
    }
  };

  return (
    <div style={{
      padding: "30px",
      fontFamily: "Arial"
    }}>
      <h1>
        MarketSense Dashboard
      </h1>

      {!marketData ? (
        <p>
          Loading...
        </p>
      ) : (
        <div>

          <h2>
            Market Sentiment:
            {" "}
            {marketData.market_sentiment}
          </h2>

          <p>
            Total Articles:
            {" "}
            {marketData.total_articles}
          </p>

          <p>
            Positive:
            {" "}
            {marketData.positive_articles}
          </p>

          <p>
            Negative:
            {" "}
            {marketData.negative_articles}
          </p>

          <p>
            Neutral:
            {" "}
            {marketData.neutral_articles}
          </p>

          <p>
            Avg Score:
            {" "}
            {marketData.average_sentiment_score}
          </p>

        </div>
      )}
    </div>
  );
}

export default App;