def scaled_macd_strategy(df, cash, name='scaled_macd', scale_factor=3):

    ### Parameters
    stock_held = 0  ### Number of stock held each day
    stock_held_column = []  ### List of stock held on each day
    cash_column = []        ### List of cash on each day
    total_value_column = [] ### List of networth on each day

    ### Loop through days in df
    ### This strategy requires Closing price and daily price difference but zip as many columns as necessary
    for macd, signal, close in zip(df['macd'], df['macd_signal'], df['Close']):
        ### If daily macd is > signal value, buy stock
        if macd > signal and (cash > close):
            stock_held += scale_factor
            cash -= scale_factor * close

        elif (macd < signal) and (stock_held >= scale_factor):
            stock_held -= scale_factor
            cash += scale_factor * close

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
