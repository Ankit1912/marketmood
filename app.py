from flask import Flask, jsonify, request
from transformers import pipeline
from flask_cors import CORS

import requests  # For making API calls

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Add this line

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
    symbol = request.args.get('symbol', 'TSLA').upper()  # Ensure ticker is uppercase
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/quote"
    headers = {
        "X-RapidAPI-Key": "b98987f14amsh6fbad8b8bbdbf98p1f6b0djsn177e0b5f9f21",  # Replace with your RapidAPI key
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }
    params = {
        "ticker": symbol,   # Stock ticker
        "type": "STOCKS"    # Asset type
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
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
