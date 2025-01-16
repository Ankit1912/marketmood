import React, { useState, useEffect } from "react";
import axios from "axios";
import ClipLoader from "react-spinners/ClipLoader";

const NewsData = () => {
  const [newsData, setNewsData] = useState([]);
  const [symbol, setSymbol] = useState("TSLA");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (symbol) {
      setIsLoading(true); // Start loading spinner
      axios
        .get(`http://127.0.0.1:5000/news?symbol=${symbol}`)
        .then((response) => {
          console.log("News Data:", response.data); // Debugging log
          setNewsData(response.data.articles || []);
          setIsLoading(false); // Stop loading spinner
        })
        .catch((error) => {
          console.error("Error fetching news data:", error);
          setIsLoading(false); // Stop loading spinner on error
        });
    }
  }, [symbol]);

  return (
    <div>
      <h2>News Articles</h2>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        placeholder="Enter stock symbol (e.g., TSLA)"
      />
      {isLoading ? (
        <ClipLoader color="#123abc" loading={isLoading} size={50} />
      ) : newsData.length ? (
        <ul>
          {newsData.map((article, index) => (
            <li key={index} style={{ marginBottom: "10px" }}>
              <strong>{article.title}</strong> - Sentiment:{" "}
              <span
                style={{
                  color:
                    article.sentiment === "positive"
                      ? "green"
                      : article.sentiment === "negative"
                      ? "red"
                      : "gray",
                }}
              >
                {article.sentiment}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No news articles found for this stock symbol.</p>
      )}
    </div>
  );
};

export default NewsData;
