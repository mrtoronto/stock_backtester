"""
Import strategies from the strategies folder and use the functions to calculate returns on the provided DataFrame.

Make sure to name each strategy uniquely so the resulting DataFrame/plot doesn't have repeated columns.

Return the updated DataFrame and the list of strategy names.
"""

from strategies.example_strategy import example_strategy
from strategies.macd_crossover_strategy import macd_strategy
from strategies.scaled_macd_crossover_strategy import scaled_macd_strategy
from strategies.fade_scaled_macd_crossover_strategy import fade_scaled_macd_strategy

def add_strategies(df, cash):

    ### Strategy functions add 3 columns for that strategy: stock_held, cash, net_worth
    ### Name strategy for plotting and column names
    strat_1_name = '1 Scaled MACD'
    df = scaled_macd_strategy(df=df, cash=cash, name=strat_1_name, scale_factor = 1)

    strat_3_name = '2 Scaled MACD'
    df = scaled_macd_strategy(df=df, cash=cash, name=strat_3_name, scale_factor = 2)
    strat_4_name = '3 Scaled MACD'
    df = scaled_macd_strategy(df=df, cash=cash, name=strat_4_name, scale_factor=3)

    strat_names = ['sp_buyhold', strat_1_name, strat_3_name, strat_4_name]

    return df, strat_names
