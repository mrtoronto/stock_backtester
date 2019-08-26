def add_indicators(df):
    df['day_difference'] = df['Close'].diff(1)
    df['day_diff_perc'] = (df['Close'].diff(1) / df['Close']) * 100

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()

    df['macd'] = macd
    df['macd_signal'] = exp3
    return df
