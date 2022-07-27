from flask import Flask
import requests
import pprint
import time
import json
import math
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Homepage'

@app.route('/getStock/<stock>')
def getStockData(stock):
    header = {
        'authority': 'finance.yahoo.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'application/json',
        'X-API-KEY': os.environ.get('APIKEY'),
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
        'authority': 'finance.yahoo.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'application/json',
        'X-API-KEY': os.environ.get('APIKEY'),
    }
    response = requests.get('https://yfapi.net/v8/finance/spark?interval=1d&range=6mo&symbols=' + stock, headers=header).json()
    days = 100
    currClosingPrice = response[stock]['close'][-1]
    
    if len(response[stock]['close']) >= 100:
        closingDays = response[stock]['close'] 
        closeLast100Days = closingDays[len(response[stock]['close'])-101:len(response[stock]['close'])-1]
        movingAverage = sum(closeLast100Days) / days
    else:
        error = 'Insufficient data to calculate moving average...'
        print(error)
        return error

    if currClosingPrice > movingAverage:
        aboveMA = stock + ' current price is above the 100-day moving average -- Time to buy shares! (Stock Price = ' + str(currClosingPrice) +  ' | MA = ' + str(movingAverage) + ')'
        return aboveMA
    elif currClosingPrice < movingAverage:
        belowMA = stock + ' current price is below the 100-day moving average -- Time to sell shares! (Stock Price = ' + str(currClosingPrice) +  ' | MA = ' + str(movingAverage) + ')'
        return belowMA
    else:
        equalMA = stock + 'current price is equal to the 100-day moving average -- Lets wait!' + str(currClosingPrice) +  ' | MA = ' + str(movingAverage) + ')'
        return equalMA


@app.route('/meanReversion/<stock>')
def meanReversionStrategy(stock):
    header = {
        'authority': 'finance.yahoo.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'application/json',
        'X-API-KEY': os.environ.get('APIKEY'),
    }
    response = requests.get('https://yfapi.net/v8/finance/spark?interval=1d&range=72mo&symbols=' + stock, headers=header).json()
    return response


if __name__ == '__main__':
    app.run(debug=True)
