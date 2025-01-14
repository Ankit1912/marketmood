from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, MarketMood!"

import requests

# Fetch stock prices from Alpha Vantage API
@app.route('/stocks', methods=['GET'])
def get_stocks():
    try:
        api_url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": "TSLA",
            "interval": "5min",
            "apikey": "MGHF2GV6I7EP3JBB"
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch stock data", "details": str(e)}), 500


@app.route('/news', methods=['GET'])
def get_news():
    try:
        api_url = "https://newsapi.org/v2/everything"
        params = {
            "q": "Tesla",
            "apiKey": "859fccdbd13149dfa82d5184254060f1"
        }
        response = requests.get(api_url, params=params)
        data = response.json()
        return jsonify(data)
    except resuts.exceptions.RequestException as e:
        return jsonify({"error": "Failed to getch news data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
