#import pandas_datareader.stooq as web
from pandas_datareader import data as web

### https://stooq.com/

def stooq_reader(symbol, start_date, end_date):

    reader = web.StooqDailyReader(symbols = symbol,
                                start = start_date,
                                end = end_date)

    df = reader.read().reset_index()
    df = df.sort_values(by='Date').set_index('Date')
    reader.close()
    """
    df columns
     Open     High      Low    Close     Volume
    """
    return df
