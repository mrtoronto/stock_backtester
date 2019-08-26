### Name doesn't matter if `SP_bool` == True
### Buys all the stock possible on the first day, holds until last day

def buy_hold_strategy(df, cash, name='buyhold', SP_bool = True):

    ### Parameters
    if SP_bool == True:
        first_day_close = df['sp_500_close'][0]
        print()
    else:
        first_day_close = df['Close'][0]
    stock_held = cash // first_day_close   ### Number of stock held each day
    cash -= stock_held * first_day_close
    print(stock_held)
    stock_held_column = []  ### List of stock held on each day
    cash_column = []        ### List of cash on each day
    total_value_column = [] ### List of networth on each day

    ### Loop through days in df
    ### This strategy requires Closing price and daily price difference but zip as many columns as necessary
    if SP_bool == True:
        for close in df['sp_500_close']:
            ### Append daily data to lists that will become columns
            stock_held_column.append(stock_held)
            cash_column.append(cash)
            total_value_column.append(stock_held * close + cash)


        df['sp_buyhold_stocks'] = stock_held_column
        df['sp_buyhold_cash'] = cash_column
        df['sp_buyhold_net_worth'] = total_value_column
    else:
        df['{}_stocks'.format(name)] = stock_held_column
        df['{}_cash'.format(name)] = cash_column
        df['{}_net_worth'.format(name)] = total_value_column
    return df
