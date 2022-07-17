#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
# yf.download returns a DataFrame
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)

def PrintHistoricalAndRec(ticker):
        hist = ticker.history(period="1mo")
        analyst_recdf = pd.DataFrame(ticker.recommendations)
        df = pd.DataFrame(hist)
        df2 = df[["Open","Volume","Close","Low"]]
        df3 = pd.concat([df2, analyst_recdf])
        print(df3)

def PrintPERatios(ticker):
        print("two PE ratios are trailingPE and forwardPE: ", ticker.info["trailingPE"], ticker.info["forwardPE"])

def PrintAsk(ticker):
        print("ask: ", ticker.info["ask"])

def PrintBid(ticker):
        print("bid: ", ticker.info["bid"])

def PrintEPS(ticker):
        print("EPS: ", ticker.info["revenuePerShare"])

inp = input('Input a stock ticker: ')
stock = yf.Ticker(inp)


PrintHistoricalAndRec(stock)
PrintPERatios(stock)
PrintAsk(stock)
PrintBid(stock)
PrintEPS(stock)
