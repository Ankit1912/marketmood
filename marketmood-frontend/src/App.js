import React, { useState } from "react";
import StockData from "./components/StockData";
import NewsData from "./components/NewsData";
import SentimentChart from "./components/SentimentChart";

import "./App.css";

const App = () => {
  const [symbol, setSymbol] = useState("");
  const [type, setType] = useState("Stocks");
  const [submittedSymbol, setSubmittedSymbol] = useState("");
  const [submittedType, setSubmittedType] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent page reload
    setSubmittedSymbol(symbol); // Set symbol for API calls
    setSubmittedType(type); // Set type (Stocks/ETFs) for API calls
  };

  return (
    <div className="App">
      <h1>MarketMood</h1>
      <p>Track the pulse of stocks and ETFs over last 30 days</p>

      {/* Search Form */}
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          placeholder="Enter Symbol (e.g., TSLA)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="Stocks">STOCKS</option>
          <option value="ETF">ETF</option>
        </select>
        <button type="submit">Submit</button>
      </form>

      {/* Render Stock and News Components */}
      <div className="data-display">
        <div className="stock-section">
          <StockData symbol={submittedSymbol} assetType={submittedType} />
        </div>
        <div className="news-section">
          <NewsData symbol={submittedSymbol} />
        </div>
        {/* Charts Section */}
        <div className="charts-section">
          <SentimentChart symbol={submittedSymbol} />
        </div>
      </div>
    </div>
  );
};

export default App;
