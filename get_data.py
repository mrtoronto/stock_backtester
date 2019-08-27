import dateparser
from indicators import add_indicators
import pandas as pd
import os
import yfinance as yf

"""

Gets data from Yahoo! Finance or from cache. If cache data partially exists, use Yahoo! Finance to fill it in and then update the cache.

"""

def _get_data(symbol, start, end, debug=False):
    cache_file_name = "cache/{sym}/{sym}_cache.csv".format(sym=symbol)
    cache_folder_name = "cache/{}".format(symbol)

    ### If the cache folder doesn't exist:
    if not os.path.exists("cache"):
        os.mkdir('cache')
        print("Cache folder didn't exist. Creating it now.")
        os.mkdir(cache_folder_name)
        print("Cache folder for ${} didn't exist. Creating it now.".format(symbol))
        ### Download data, remove index from 'Date'
        df = yf.download(symbol, start=start, end=end).reset_index()
        df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in df['Date'].astype(str)]
        ### Save cache file
        df.to_csv(cache_file_name, index=False)
        if debug == True:
            print(df.head(3))
            print(df.tail(3))
        return df

    ### If the ticker's cache folder doesn't exist:
    elif (not os.path.exists(cache_folder_name)):
        os.mkdir(cache_folder_name)
        print("Cache folder for ${} didn't exist. Creating it now.".format(symbol))
        ### Download data, remove index from 'Date'
        df = yf.download(symbol, start=start, end=end).reset_index()
        df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in df['Date'].astype(str)]
        ### Save cache file
        df.to_csv(cache_file_name, index=False)
        if debug == True:
            print(df.head(2))
            print(df.tail(2))
        return df

    ### If the ticker's cache file doesn't exist:
    elif not os.path.exists(cache_file_name):
        ### Download data, remove index from 'Date'
        df = yf.download(symbol, start=start, end=end).reset_index()
        df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in df['Date'].astype(str)]
        ### Save cache file
        df.to_csv(cache_file_name, index=False)
        print("Cache file for ${} didn't exist. Creating it now.".format(symbol))
        if debug == True:
            print(df.head(2))
            print(df.tail(2))
        return df

    ### If the ticker's cache file does exist:
    else:
        print("\n\nCache file for ${} exists. Reading it now.".format(symbol))
        ### Read cache file, don't read an index column
        cached_df = pd.read_csv(cache_file_name, header=0, index_col=False)
        ### Parse all the dates
        cached_df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in cached_df['Date'].astype(str)]
        start = dateparser.parse(start, date_formats=['%m/%d/%y'])
        end = dateparser.parse(end, date_formats=['%m/%d/%y'])

        ### Pull the first and last dates (Cache files should be sorted so this works)
        first_date_in_cache = cached_df['Date'].iloc[0]
        first_date_in_cache = dateparser.parse(str(first_date_in_cache), date_formats=['%m/%d/%y'])
        last_date_in_cache = cached_df['Date'].iloc[len(cached_df)-1]
        last_date_in_cache = dateparser.parse(str(last_date_in_cache), date_formats=['%m/%d/%y'])

        if debug == True:
            print("Start : ", start, " // first_date_in_cache : ", first_date_in_cache)
            print("End : ", end, " // last_date_in_cache : ", last_date_in_cache)

        ### If cached_df fully contains requested data
        if (first_date_in_cache <= start) and (last_date_in_cache >= end):
            ### Truncate cached_df with the date range
            cached_df = cached_df[(cached_df['Date'] >= start)]
            cached_df = cached_df[(cached_df['Date'] <= end)]
            print("${} cache had all necessary data, returning cached data.".format(symbol))
            if debug == True:
                print(cached_df.head(3))
                print(cached_df.tail(3))
            return cached_df

        ### If cached_df has earlier data but not later data
        elif first_date_in_cache <= start and last_date_in_cache <= end:
            ### Download the missing data using the last date in cache and the requested end date
            download_df = yf.download(symbol, last_date_in_cache, end).reset_index()
            ### Append the download_df to the cached_df
            cached_df = cached_df.append(download_df, ignore_index=True, sort=False)
            ### Sort and drop duplicates
            cached_df = cached_df.sort_values(by='Date')
            cached_df = cached_df.drop_duplicates()
            ### Remove the old cache file
            os.unlink(cache_file_name)
            ### Save the updated cache file
            cached_df.to_csv(cache_file_name, index=False)
            print("${} cache had earlier data but not through requested end, cache has been updated.".format(symbol))
            if debug == True:
                print(cached_df.head(3))
                print(cached_df.tail(3))
            return cached_df

        ### If cached_df has later data but not earlier data
        elif first_date_in_cache >= start and last_date_in_cache >= end:
            ### Download the missing data using the requested start date and first date in the cache as endpoints
            download_df = yf.download(symbol, start, first_date_in_cache).reset_index()
            ### Append the download_df to the cached_df
            cached_df = cached_df.append(download_df, ignore_index=True)
            ### Sort and drop duplicates
            cached_df = cached_df.sort_values(by='Date')
            cached_df = cached_df.drop_duplicates()
            ### Remove the old cache file
            os.unlink(cache_file_name)
            ### Save the updated cache file
            cached_df.to_csv(cache_file_name, index=False)
            print("${} cache had later data but not as early as requested, cache has been updated.".format(symbol))
            if debug == True:
                print(cached_df.head(3))
                print(cached_df.tail(3))
            return cached_df

        else:
            if debug == True:
                print("Please help me, I'm on fire.")
            return None


def get_dataframe(symbol, start, end, debug, cache=True):

    if cache == True:
        ### Get data from Yahoo! Finance or cache
        df = _get_data(symbol, start, end, debug)
        sp_df = _get_data('SPY', start, end, debug)
    elif cache == False:
        df = yf.download(symbol, start=start, end=end).reset_index()
        sp_df = yf.download('SPY', start=start, end=end).reset_index()
    ### Run function to add indicators
    df = add_indicators(df)

    ### Add S&P500 close price to test DataFrame
    df['sp_500_close'] = sp_df['Close']
    print('\n\n')
    return df
