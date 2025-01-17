from flask import Flask, jsonify, request
from transformers import pipeline
from flask_cors import CORS
import requests  # For making API calls

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Analyze sentiment of a given text."""
    try:
        result = sentiment_analyzer(text)[0]  # Analyze the sentiment
        sentiment = result['label']
        # Convert Hugging Face labels to simplified ones
        if sentiment == "POSITIVE":
            return "positive"
        elif sentiment == "NEGATIVE":
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "neutral"  # Default to neutral if an error occurs


@app.route('/')
def home():
    return "Hello, MarketMood!"


@app.route('/stocks', methods=['GET'])
def get_stocks():
    """Fetch stock prices from Yahoo Finance API."""
    symbol = request.args.get('symbol', 'TSLA').upper()
    asset_type = request.args.get('type', 'STOCKS')  # STOCKS, CRYPTO, or ETFs
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/quote"
    #url = f"https://yahoo-finance15.p.rapidapi.com/api/v1/markets/historical/{symbol}?interval=1d&range=1mo"
    headers = {
        "X-RapidAPI-Key": "b98987f14amsh6fbad8b8bbdbf98p1f6b0djsn177e0b5f9f21",
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }
    params = {
        "ticker": symbol,
        "type": asset_type.upper()
    }

    print(f"Stock API Request: {url} with Params: {params}")

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return jsonify({"error": "Failed to fetch stock data", "details": str(e)}), 500


@app.route('/news', methods=['GET'])
def get_news():
    """Fetch news and analyze sentiment."""
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({"error": "Please provide a stock symbol"}), 400

    #url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey=859fccdbd13149dfa82d5184254060f1"
    url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&apiKey=859fccdbd13149dfa82d5184254060f1"

    print(f"News API Request: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
  
        # Simplify the articles and add sentiment analysis
        articles = response_data.get('articles', [])
        simplified_articles = []
        
        for article in articles:
            description = article.get('description', '')
            if description:  # Only process if the description exists
                sentiment = analyze_sentiment(description)
            else:
                sentiment = "neutral"  # Default sentiment for missing descriptions

            simplified_articles.append({
                "title": article.get('title', 'No Title'),
                "description": description or 'No Description',
                "sentiment": sentiment
            })
        
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for article in simplified_articles:
            sentiment_counts[article["sentiment"]] += 1

        return jsonify({"stock": symbol, "articles": simplified_articles, "sentiment_counts": sentiment_counts})
        #return jsonify({"stock": symbol, "articles": simplified_articles})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return jsonify({"error": "Failed to fetch news data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
