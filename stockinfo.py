#!/usr/bin/env python3
import yfinance as yf
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)


print("\nThis is saving data to a variable:")
dow = yf.Ticker("DOW")
# get stock info
dow.info

# get historical market data
# no need to display dividends, stock splits, and high

hist = dow.history(period="1mo")
print(hist)


# TODO: display ask, bid, PE Ratios, EPS, analyst recommendations
# comment: i'm not sure if he wants us to print data over a certain period
# the print statements below only print the current data
print("two PE ratios are trailingPE and forwardPE:")
print(dow.info["trailingPE"])
print(dow.info["forwardPE"])
print("ask:")
print(dow.info["ask"])
print("bid:")
print(dow.info["bid"])
print("earnings/revenue per share (EPS?):")
print(dow.info["revenuePerShare"])
print("analyst recommendations? 'numberOfAnalystOpinions'")
print(dow.info["numberOfAnalystOpinions"])
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