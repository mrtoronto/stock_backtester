import yfinance as yf
import numpy as np
import seaborn as sns
from readers.quandl_reader import quandl_reader
from readers.stooq_reader import stooq_reader

from indicators import add_indicators
from strategies.buyall_hold_strategy import buy_hold_strategy
from compare_plot_fn import plot_fn
from add_strategies import add_strategies

### Ticker for S&P500 buy and hold strategy
sp_symbol = 'SPY'
### Ticker to test strategies on
test_symbol = 'AAPL'

### Dates in 'YYYY-MM-DD' format
start_date = '2015-08-20'
end_date = '2019-08-20'
### Cash to start with
cash = 10000


"""
Grab historic stock data for test ticker and S&P500.

Source options: `stooq.com`, Yahoo! Finance, Quandl
    I found stooq first and it has up to date data but has a daily limit. The limit may be with `pandas_datareader` overall.
        history_test_df = stooq_reader(test_symbol, start_date, end_date)
    Quandl is slightly outdated and requires an API key. Also effected by daily limit.
        history_test_df = quandl_reader(test_symbol, start_date, end_date)
    Yahoo Finance is good and up to date.
        history_test_df = yf.download(test_symbol, start=start_date, end=end_date)
"""

history_test_df = yf.download(test_symbol, start=start_date, end=end_date)
### Grab S&P500 data for the same time range
history_sp_df = yf.download(sp_symbol, start=start_date, end=end_date)
### Add indicators to the test ticker's DataFrame
history_test_df = add_indicators(history_test_df)

### Add S&P500 close price to test DataFrame
history_test_df['sp_500_close'] = history_sp_df['Close']

### Adds columns for S&P500 buy-hold benchmark strategy
history_test_df = buy_hold_strategy(history_test_df, cash, SP_bool = True)

### Adds all other stratgies for run
history_test_df, strat_names = add_strategies(df=history_test_df, cash=cash)

### Reset index to make the Date column easier to plot
history_test_df = history_test_df.reset_index()

### Columns to print
print_cols = ['Date']
for col_name in strat_names:
    print_cols.append('{}_net_worth'.format(col_name))

print_df = history_test_df.loc[:, print_cols]
n=10
print("First {} days\n#####\n".format(n), print_df.head(n))
print("Last {} days\n".format(n), print_df.tail(n))

plot_fn(history_test_df, strat_names, cash, test_symbol, save_image='')
