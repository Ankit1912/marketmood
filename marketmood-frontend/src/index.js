// Import React and other required modules
import React from "react";
import ReactDOM from "react-dom/client";

// Import CSS and app components
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

// Import and register Chart.js components
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register the required Chart.js components globally
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Create the React root and render the App
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Measure app performance (optional, can be customized)
reportWebVitals();
