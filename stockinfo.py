#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
import requests
import json
# yf.download returns a DataFrame
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)

def PrintHistoricalAndRec(ticker):
        hist = ticker.history(period="1d")
        analyst_recdf = pd.DataFrame(ticker.recommendations)
        df = pd.DataFrame(hist)
        df2 = df[["Open","Volume","Close","Low"]]
        df3 = pd.concat([df2, analyst_recdf])
        print(df3)
        df3.to_csv("concat_data.csv")
        return df3

def PrintPERatios(ticker):
        print("two PE ratios are trailingPE and forwardPE: ", ticker["trailingPE"], ticker["forwardPE"])
        return ticker["trailingPE"], ticker["forwardPE"]

def PrintAsk(ticker):
        print("Ask: ", ticker["ask"])
        return ticker["ask"]

def PrintBid(ticker):
        print("Bid: ", ticker["bid"])
        return ticker["bid"]

def PrintEPS(ticker):
        print("EPS: ", ticker["revenuePerShare"])
        return ticker["revenuePerShare"]



if __name__ == '__main__':
        inp = input('Input a stock ticker: ')
        stock = yf.Ticker(inp)
        hist = stock.history(period="1d")
        df = pd.DataFrame(hist)
        df2 = df[["Open","Volume","Close","Low"]]
        df2.to_csv("history.csv")
        rec = stock.recommendations
        rec.to_csv("recommendations.csv")

        # TODO: pull quote data from Yahoo Finance API

        PrintHistoricalAndRec(stock)
        PrintPERatios(stock.info)
        PrintAsk(stock.info)
        PrintBid(stock.info)
        PrintEPS(stock.info)
