import numpy as np
import seaborn as sns
from readers.quandl_reader import quandl_reader
from readers.stooq_reader import stooq_reader
from get_data import get_dataframe


from strategies.buyall_hold_strategy import buy_hold_strategy
from compare_plot_fn import plot_fn
from add_strategies import add_strategies

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

### Ticker to test strategies on
test_symbol = 'GE'

### Debug option
debug = False
### Flag to use cache or pull fresh every run
cache = True

### Dates in 'YYYY-MM-DD' format
start_date = '2015-01-20'
end_date = '2017-06-20' # Excludes this day
### Cash to start with
cash = 10000

history_test_df = get_dataframe(symbol=test_symbol, start=start_date, end=end_date, debug=debug, cache=cache)


### Adds columns for S&P500 buy-hold benchmark strategy
history_test_df = buy_hold_strategy(history_test_df, cash, SP_bool = True)

### Adds all other stratgies for run
history_test_df, strat_names = add_strategies(df=history_test_df, cash=cash)

### Reset index to make the Date column easier to plot
history_test_df = history_test_df.reset_index()


if debug == True:
    ### Columns to print
    print_cols = ['Date']
    for col_name in strat_names:
        print_cols.append('{}_net_worth'.format(col_name))

    print_df = history_test_df.loc[:, print_cols]
    n=10
    print("#####\nFirst {} days\n".format(n), print_df.head(n))
    print("Last {} days\n".format(n), print_df.tail(n))

plot_fn(history_test_df, strat_names, cash, test_symbol, save_image='')
