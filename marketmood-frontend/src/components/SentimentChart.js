import React, { useState, useEffect } from "react";
import { Line, Pie } from "react-chartjs-2";

const SentimentChart = ({ symbol }) => {
  const [sentiments, setSentiments] = useState({ positive: 0, negative: 0, neutral: 0 });

  useEffect(() => {
    if (symbol) {
      fetch(`http://127.0.0.1:5000/news?symbol=${symbol}`)
        .then((res) => res.json())
        .then((data) => {
          const articles = data.articles || [];
          const sentimentCount = { positive: 0, negative: 0, neutral: 0 };

          articles.forEach((article) => {
            sentimentCount[article.sentiment]++;
          });

          setSentiments(sentimentCount);
        })
        .catch((err) => console.error("Error fetching sentiment data:", err));
    }
  }, [symbol]);

  const data = {
    labels: ["Positive", "Negative", "Neutral"],
    datasets: [
      {
        label: "Sentiment Distribution",
        data: [sentiments.positive, sentiments.negative, sentiments.neutral],
        backgroundColor: ["#4caf50", "#f44336", "#9e9e9e"],
      },
    ],
  };

  return (
    <div>
      <h2>News Sentiment Analysis</h2>
      <Pie data={data} />
    </div>
  );
};

export default SentimentChart;
