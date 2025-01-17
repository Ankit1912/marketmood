import React, { useState, useEffect } from "react";
import axios from "axios";
import ClipLoader from "react-spinners/ClipLoader";

const NewsData = ({ symbol }) => {
  const [newsData, setNewsData] = useState([]); // For storing articles
  const [isLoading, setIsLoading] = useState(false); // For loading state
  const [error, setError] = useState(null); // For error messages

  useEffect(() => {
    if (symbol) {
      // Only make API call if symbol is valid
      setIsLoading(true);
      setError(null);

      console.log(`Fetching news for: ${symbol}`);

      axios
        .get(`http://127.0.0.1:5000/news?symbol=${symbol}`) // Match Flask route
        .then((response) => {
          console.log("API Response:", response.data);

          // Handle response - match the `articles` key from Flask
          if (response.data.articles && response.data.articles.length > 0) {
            setNewsData(response.data.articles); // Update state with articles
          } else {
            setNewsData([]);
            setError("No news articles available for this symbol.");
          }
        })
        .catch((err) => {
          console.error("Error fetching news data:", err);
          setError(
            err.response?.data?.error || "Failed to fetch news data. Please try again later."
          );
        })
        .finally(() => {
          setIsLoading(false); // Stop loading spinner
        });
    }
  }, [symbol]); // Re-run API call when `symbol` changes

  return (
    <div className="news-container">
      <h2>News Articles</h2>

      {isLoading ? (
        // Display loading spinner while fetching data
        <ClipLoader color="#123abc" loading={isLoading} size={50} />
      ) : error ? (
        // Display error message if an error occurs
        <p style={{ color: "red" }}>{error}</p>
      ) : newsData && newsData.length > 0 ? (
        // Render the list of news articles
        <ul>
          {newsData.map((article, index) => (
            <li key={index} className="news-item">
              <strong>{article.title}</strong> - Sentiment:{" "}
              <span
                style={{
                  color:
                    article.sentiment === "positive"
                      ? "green"
                      : article.sentiment === "negative"
                      ? "red"
                      : "gray", // Neutral sentiment
                }}
              >
                {article.sentiment || "Neutral"}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        // No articles to show
        <p>No news articles available for this symbol.</p>
      )}
    </div>
  );
};

export default NewsData;
