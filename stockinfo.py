#!/usr/bin/env python3
import yfinance as yf
print("This is a downloaded file:")
data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
print(data)


print("\nThis is saving data to a variable:")
dow = yf.Ticker("DOW")
# get stock info
# print(dow.info)

# get historical market data, no need to display dividends and stock splits
# open, close, ask, bid, volume, PE Ratios, EPS, analyst recommendations
hist = dow.history(period="1mo")
print(hist)
print(dow.open)


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