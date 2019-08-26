def fade_scaled_macd_strategy(df, cash, name='fade_macd', max_scale_factor=3):

    ### Parameters
    stock_held = 0  ### Number of stock held each day
    stock_held_column = []  ### List of stock held on each day
    cash_column = []        ### List of cash on each day
    total_value_column = [] ### List of networth on each day

    ### Loop through days in df
    ### This strategy requires Closing price and daily price difference but zip as many columns as necessary
    current_scale = 1
    for macd, signal, close in zip(df['macd'], df['macd_signal'], df['Close']):
        ### If daily macd is > signal value, buy stock
        if macd > signal and (cash > close):
            stock_held += current_scale
            cash -= current_scale * close
            if current_scale < max_scale_factor:
                current_scale += 1

        elif (macd < signal) and (stock_held >= current_scale):
            stock_held -= current_scale
            cash += current_scale * close
            if current_scale > 0:
                current_scale -= 1

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
