from django import urls
from flask import Flask, jsonify
import requests
import pprint
import time
import json
import math


app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"


@app.route('/getStock/<stock>')
def getStockData(stock):
    header = {
        "authority": "finance.yahoo.com",
        "method": "GET",
        "scheme": "https",
        "accept": "application/json",
        "X-API-KEY": "ZIrcNpIx1u3Y5gbzw9OX85WY5b6OQ6Fj5kPHZrh7",
    }
    urls = [
        'https://yfapi.net/v7/finance/options/' + stock + '?date=' + str(math.floor(time.time())), #contains open, close, ask, bid, volume, eps
        'https://yfapi.net/v6/finance/recommendationsbysymbol/' + stock, #contains the anaylst recomendations
        'https://yfapi.net/v6/finance/quote?region=US&lang=en&symbols=' + stock #contains the trailing ratio
    ]
    data = {}
    for url in urls:
        response = requests.get(url, headers=header).json()
        data.update(response)
    # pprint.pprint(data) 
    return data
    
if __name__ == "__main__":
    app.run(debug=True)
