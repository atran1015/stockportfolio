#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
# yf.download returns a DataFrame
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)
def GetStock(dow):
    print("\nThis is saving data to a variable:")
    
    # get stock info
    dow.info

    # get historical market data
    hist = dow.history(period="1mo")

    # print("show analyst recommendations:")
    # print(dow.recommendations)
    analyst_recdf = pd.DataFrame(dow.recommendations)

    df = pd.DataFrame(hist)
    # print(type(df)) - for debug
    column_headers = list(df.columns.values)
    # print("The Column Header :", column_headers) - for debug
    df2 = df[["Open","Volume","Close","Low"]]
    # print(df2)

    # appending analyst recommendations columns to selected historical columns
    df3 = pd.concat([df2, analyst_recdf])
    print(df3)


    # TODO: display ask, bid, PE Ratios, EPS, analyst recommendations
    # comment: i'm not sure if we need to print data over a certain period
    # the print statements below only print the current data
    print("two PE ratios are trailingPE and forwardPE: ", dow.info["trailingPE"], dow.info["forwardPE"])
    print("ask: ", dow.info["ask"])
    print("bid: ", dow.info["bid"])
    print("earnings/revenue per share (EPS?): ", dow.info["revenuePerShare"])


dow = yf.Ticker("DOW")
GetStock(dow)
