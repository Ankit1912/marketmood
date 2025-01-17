import React, { useState, useEffect } from "react";
import axios from "axios";
import ClipLoader from "react-spinners/ClipLoader";

const StockData = ({ symbol, assetType }) => {
  const [stockData, setStockData] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (symbol && assetType) {
      console.log("Fetching data for:", symbol, assetType);
      setIsLoading(true);
      setError(null);
  
      axios
        .get(`http://127.0.0.1:5000/stocks?symbol=${symbol}&type=${assetType}`)
        .then((response) => {
          console.log("API Response:", response.data);
          if (response.data.body) {
            setStockData(response.data.body);
          } else {
            setError("No data available for this symbol.");
          }
        })
        .catch((err) => {
          console.error("Error fetching stock data:", err);
          setError("Failed to fetch data. Please try again later.");
        })
        .finally(() => setIsLoading(false));
    }
  }, [symbol, assetType]);
  

  return (
    <div>
      <h2>Data for {assetType.toUpperCase()}</h2>
      {isLoading ? (
        <ClipLoader color="#123abc" loading={isLoading} size={50} />
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <ul>
          <li><strong>Company Name:</strong> {stockData.companyName || "N/A"}</li>
          <li><strong>Exchange:</strong> {stockData.exchange || "N/A"}</li>
          <li><strong>Last Sale Price:</strong> {stockData.primaryData?.lastSalePrice || "N/A"}</li>
          <li><strong>Net Change:</strong> {stockData.primaryData?.netChange || "N/A"}</li>
          <li><strong>Percent Change:</strong> {stockData.primaryData?.percentageChange || "N/A"}</li>
        </ul>
      )}
    </div>
  );
};

export default StockData;
