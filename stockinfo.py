#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
# yf.download returns a DataFrame
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)
def GetStock(ticker):
    print("\nThis is saving data to a variable:")
    
    # get stock info
    ticker.info

    # get historical market data
    hist = ticker.history(period="1mo")

    # print("show analyst recommendations:")
    # print(dow.recommendations)
    analyst_recdf = pd.DataFrame(ticker.recommendations)

    df = pd.DataFrame(hist)
    # print(type(df)) - for debug
    column_headers = list(df.columns.values)
    # print("The Column Header :", column_headers) - for debug
    df2 = df[["Open","Volume","Close","Low"]]
    # print(df2)

    # appending analyst recommendations columns to selected historical columns
    df3 = pd.concat([df2, analyst_recdf])
    print(df3)

    print("two PE ratios are trailingPE and forwardPE: ", ticker.info["trailingPE"], ticker.info["forwardPE"])
    print("ask: ", ticker.info["ask"])
    print("bid: ", ticker.info["bid"])
    print("EPS: ", ticker.info["revenuePerShare"])


inp = input('Input a stock ticker: ')
stock = yf.Ticker(inp)
GetStock(stock)
