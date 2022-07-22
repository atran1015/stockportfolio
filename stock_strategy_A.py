#!/usr/bin/env python3
import yfinance as yf
import pandas as pd


def moving_average_calc(df, days, col="Close"):
            if len(df) > days:
                close_col = df[[col]]
                close_last_100days = close_col.tail(100)

                # calculates moving average over last 100 days
                moving_average = int(close_last_100days.sum()) / days

            else:
                print("\nData is not sufficient to calculate")

            return buy_sell_recommendation(df,moving_average)


def buy_sell_recommendation(df, ma):
    curr_closing_price = df["Close"][-1]    # current closing price

    if curr_closing_price >= ma:
        print("\nCurrent price is over 100-day moving average -- Good time to buy shares!")
        stock_above_sma.append(ticker)
    else:
        print("\nCurrent price is under 100-day moving average -- You should sell some shares!")
        stock_below_sma.append(ticker)


stock_above_sma = []    # List of stocks above 100-day moving average
stock_below_sma = []    # List of stocks below 100-day moving average

# df = yf.download(ticker, period="1yr", interval="1d")
ticker = 'AAPL'
stock = yf.Ticker(ticker)
hist = stock.history(period="6mo")
df = pd.DataFrame(hist)

ma = moving_average_calc(df, days=100)
