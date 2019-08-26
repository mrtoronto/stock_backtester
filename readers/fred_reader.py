import pandas_datareader.nasdaq_trader as web

df = web.get_nasdaq_symbols()

print(df.columns)
