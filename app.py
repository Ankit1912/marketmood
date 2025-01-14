from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, MarketMood!"

import requests

@app.route('/stocks', methods=['GET'])
def get_stocks():
    api_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": "TSLA",
        "interval": "1min",
        "apikey": "MGHF2GV6I7EP3JBB"
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return jsonify(data)

@app.route('/news', methods=['GET'])
def get_news():
    api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Tesla",
        "apiKey": "859fccdbd13149dfa82d5184254060f1"
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
