import React, { useState, useEffect } from "react";
import axios from "axios";
import ClipLoader from "react-spinners/ClipLoader";

const StockData = () => {
  const [stockData, setStockData] = useState({});
  const [symbol, setSymbol] = useState("TSLA");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (symbol) {
      setIsLoading(true); // Start loading spinner
      axios
        .get(`http://127.0.0.1:5000/stocks?symbol=${symbol}`)
        .then((response) => {
          console.log("Stock Data:", response.data); // Debugging log
          setStockData(response.data);
          setIsLoading(false); // Stop loading spinner
        })
        .catch((error) => {
          console.error("Error fetching stock data:", error);
          setIsLoading(false); // Stop loading spinner on error
        });
    }
  }, [symbol]);

  return (
    <div>
      <h2>Stock Data</h2>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        placeholder="Enter stock symbol (e.g., TSLA)"
      />
      {isLoading ? (
        <ClipLoader color="#123abc" loading={isLoading} size={50} />
      ) : stockData.body ? (
        <ul>
          <li><strong>Company Name:</strong> {stockData.body?.companyName || "N/A"}</li>
          <li><strong>Exchange:</strong> {stockData.body?.exchange || "N/A"}</li>
          <li><strong>Last Sale Price:</strong> {stockData.body?.primaryData?.lastSalePrice || "N/A"}</li>
          <li><strong>Net Change:</strong> {stockData.body?.primaryData?.netChange || "N/A"}</li>
          <li><strong>Percent Change:</strong> {stockData.body?.primaryData?.percentageChange || "N/A"}</li>
        </ul>
      ) : (
        <p>No stock data available for this symbol.</p>
      )}
    </div>
  );
};

export default StockData;
