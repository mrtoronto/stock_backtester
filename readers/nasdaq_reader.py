import pandas_datareader.nasdaq_trader as web

df = web.get_nasdaq_symbols()

"""
df columns :
['Nasdaq Traded', 'Security Name', 'Listing Exchange', 'Market Category',
       'ETF', 'Round Lot Size', 'Test Issue', 'Financial Status', 'CQS Symbol',
       'NASDAQ Symbol', 'NextShares']

"""

print(df.columns)
