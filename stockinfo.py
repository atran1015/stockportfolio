#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
# yf.download returns a DataFrame
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)

print("\nThis is saving data to a variable:")
dow = yf.Ticker("DOW")
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
# the print statements below only print the current data
print("two PE ratios are trailingPE and forwardPE: ", dow.info["trailingPE"], dow.info["forwardPE"])
print("ask: ", dow.info["ask"])
print("bid: ", dow.info["bid"])
print("earnings/revenue per share (EPS?): ", dow.info["revenuePerShare"])


# if dow:
#     print("not empty")





















# # show actions (dividends, splits)
# msft.actions

# # show dividends
# msft.dividends

# # show splits
# msft.splits

# # show financials
# msft.financials
# msft.quarterly_financials

# # show major holders
# msft.major_holders

# # show institutional holders
# msft.institutional_holders

# # show balance sheet
# msft.balance_sheet
# msft.quarterly_balance_sheet

# # show cashflow
# msft.cashflow
# msft.quarterly_cashflow

# # show earnings
# msft.earnings
# msft.quarterly_earnings

# # show sustainability
# msft.sustainability

# # show analysts recommendations
# msft.recommendations

# # show next event (earnings, etc)
# msft.calendar

# # show all earnings dates
# msft.earnings_dates

# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# msft.isin

# # show options expirations
# msft.options

# # show news
# msft.news

# # get option chain for specific expiration
# opt = msft.option_chain('2022-07-15')
# # data available via: opt.calls, opt.puts
#print("this works")