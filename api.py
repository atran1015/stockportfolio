from distutils.log import error
from xmlrpc.client import ResponseError
from django import urls
from flask import Flask
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
    for url in urls: # combine all data into one chunk
        response = requests.get(url, headers=header).json()
        data.update(response)
    # pprint.pprint(data) 
    return data

@app.route('/smaStrategy/<stock>')
def smaStrategy(stock):
    header = {
        "authority": "finance.yahoo.com",
        "method": "GET",
        "scheme": "https",
        "accept": "application/json",
        "X-API-KEY": "ZIrcNpIx1u3Y5gbzw9OX85WY5b6OQ6Fj5kPHZrh7",
    }
    response = requests.get('https://yfapi.net/v8/finance/spark?interval=1d&range=6mo&symbols=' + stock, headers=header).json()
    days = 100
    currClosingPrice = response[stock]['close'][0]
    
    if len(response[stock]['close']) >= 100:
        closingDays = response[stock]['close'] 
        closeLast100Days = closingDays[0:100]
        movingAverage = sum(closeLast100Days) / days
    else:
        error = 'Insufficient data to calculate moving average...'
        print(error)
        return error

    if currClosingPrice > movingAverage:
        aboveMA = stock + ' current price is above the 100-day moving average -- Time to buy shares!'
        return aboveMA
    elif currClosingPrice < movingAverage:
        belowMA = stock + 'current price is below the 100-day moving average -- Time to sell shares!'
        return belowMA
    else:
        equalMA = stock + 'current price is equal to the 100-day moving average -- Lets wait!'
        return equalMA

if __name__ == "__main__":
    app.run(debug=True)
