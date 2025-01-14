from flask import Flask, jsonify, request
import requests  # For making API calls

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, MarketMood!"

# Fetch stock prices from Alpha Vantage API
@app.route('/stocks', methods=['GET'])
def get_stocks():
    import requests
    # Get the stock symbol from the query parameter, default to Tesla if not provided
    symbol = request.args.get('symbol', 'TSLA')

    # Alpha Vantage API URL and parameters
    api_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": "MGHF2GV6I7EP3JBB"  # Replace with your actual API key
    }

    try:
        # Fetch stock data
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        # Check if the API returns an error
        if "Error Message" in data:
            return jsonify({"error": f"Invalid stock symbol: {symbol}"}), 400

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch stock data", "details": str(e)}), 500


@app.route('/news', methods=['GET'])
def get_news():
    import requests
    # Get the stock symbol from the query parameter, default to Tesla if not provided
    symbol = request.args.get('symbol', 'TSLA')

    # NewsAPI URL and parameters
    api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,  # Search for news related to the stock symbol
        "apiKey": "859fccdbd13149dfa82d5184254060f1"  # Replace with your actual API key
    }

    try:
        # Fetch news data
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        # Check for empty results
        if not data.get("articles"):
            return jsonify({"message": f"No news found for stock: {symbol}"}), 404

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch news data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
