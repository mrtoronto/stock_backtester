import pandas_datareader.quandl as web

def quandl_reader(symbol, start_date, end_date):

    ### Read API key from file
    with open("quandl_api_key.txt","r") as f:
        api_key = f.read().strip()

    reader = web.QuandlReader(symbols = symbol,
                                start = start_date,
                                end=end_date,
                                api_key=api_key)
    df = reader.read()
    df = df.sort_values(by='Date')

    """
    history_df is ordered with ascending dates and has the following columns :
    'Open', 'High', 'Low', 'Close', 'Volume', 'ExDividend', 'SplitRatio',
    'AdjOpen', 'AdjHigh', 'AdjLow', 'AdjClose', 'AdjVolume'
    """
    return df
