from flask import Flask, jsonify, request
from transformers import pipeline

import requests  # For making API calls

# Initialize Flask app
app = Flask(__name__)

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiments_batch(texts):
    """Analyze sentiment of a batch of texts."""
    results = sentiment_analyzer(texts)  # Process in batch
    return [result['label'].lower() for result in results]  # Convert to lowercase

def analyze_sentiment(text):
    """Analyze sentiment of a given text."""
    result = sentiment_analyzer(text)[0]  # Get first result
    sentiment = result['label']
    # Convert Hugging Face labels to simplified ones
    if sentiment == "POSITIVE":
        return "positive"
    elif sentiment == "NEGATIVE":
        return "negative"
    else:
        return "neutral"


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
    # Get the stock symbol from the query parameter
    symbol = request.args.get('symbol', 'TSLA')

    api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "apiKey": "859fccdbd13149dfa82d5184254060f1" 
    }

    try:
        # Fetch news data
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract article titles for sentiment analysis
        articles = data.get("articles", [])
        article_titles = [article.get("title", "") for article in articles]

        # Analyze sentiments in batch
        sentiments = analyze_sentiments_batch(article_titles)

        # Add sentiments back to articles
        simplified_articles = [
            {"title": title, "sentiment": sentiment}
            for title, sentiment in zip(article_titles, sentiments)
        ]

        return jsonify({"stock": symbol, "articles": simplified_articles})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch news data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
