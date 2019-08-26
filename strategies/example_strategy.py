def example_strategy(df, cash, name='example'):

    ### Parameters
    stock_held = 0  ### Number of stock held each day
    stock_held_column = []  ### List of stock held on each day
    cash_column = []        ### List of cash on each day
    total_value_column = [] ### List of networth on each day

    ### Loop through days in df
    ### This strategy requires Closing price and daily price difference but zip as many columns as necessary
    for close, diff in zip(df['Close'], df['day_difference']):
        ### If daily price difference is > 2, buy a stock
        if diff > 2:
            stock_held += 1
            cash -= close

        elif (diff < -2) and (stock_held > 0):
            stock_held -= 1
            cash += close

        else:
            pass

        ### Append daily data to lists that will become columns
        stock_held_column.append(stock_held)
        cash_column.append(cash)
        total_value_column.append(close * stock_held + cash)

    df['{}_stocks'.format(name)] = stock_held_column
    df['{}_cash'.format(name)] = cash_column
    df['{}_net_worth'.format(name)] = total_value_column

    return df
