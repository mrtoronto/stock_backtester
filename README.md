# stock_backtester

## General

Running `backtest.py` will perform a run of the script. The output will be a plot of the back-test.

Each run of the back-tester will use specified trading strategies to maintain a portfolio of stock over the specified timeframe. The results of all the strategies are plotted to be compared to each other and to the results of a "buy and hold" strategy on the S&P500 using the same amount of money.

![](https://i.imgur.com/pw9iIWU.png)

## Run description

1. Pull test ticker and S&P500 data from Yahoo! Finance or cache file created by process.
    - Changing the `cache` boolean to `False` will make the process pull fresh every run.
    - Cache folder and subfolders for each ticker will be created if necessary.
    - Partially complete cache data will be filled in from Yahoo! Finance.
        - If cache had data from '2017-01-01'-'2018-01-01' for a ticker and user requested data from '2017-01-01'-'2018-06-01' for the same ticker, process will pull data for '2018-01-01'-'2018-06-01' from Yahoo! Finance and update the stored cache file.

2. Derive indicators from the raw data.
    - Done in the `indicators.py` script.
    - Currently implemented indicators:
        - Daily price difference ($)
        - Daily price difference (%)
        - MACD and signal line
3. Run a "buy and hold" strategy on the S&P500 data
    - Buy and hold strategy buys all possible stock on the first day of run and holds through the run

4. Run the `add_strategies` function on the DataFrame to add data for any specified custom strategies.
    - Each 'strategy' lives in its own python script in the strategies folder.
    - A strategy follows the format below:
        - Iterate through a zip of any columns that'll be required for the strategy. For example:
            - `MACD` strategy iterates through `zip(df['macd'], df['macd_signal'], df['Close'])` as the strategy uses the MACD, the MACD's signal line and the day's Close price for each update.
    - Currently included strategies:
        - Buy and Hold strategy - Buys as much stock as possible immediately, holds for rest of run.
        - MACD Crossover Strategy
            - Relevant indicators:
                - MACD line == (12-day EMA - 26-day EMA)
                - Signal line == (9-day EMA of MACD)
            - When the MACD crosses above the signal line, its considered a bullish crossover.
            - When the MACD crosses below the signal line, its considered a bearish crossover.
            - In this strategy, the bot will buy and sell depending on whether a day is part of a bullish or bearish crossover at Close.
        - Scaled MACD Crossover Strategy
            - This strategy is the same as the MACD Crossover strategy except it buys/sells a set number of stock each day instead of 1.
        - Faded Scaled MACD Crossover Strategy
            - It doesn't appear this strategy preforms as well as normal scaled_MACD but feel free to try it.
            - This strategy is the same as the Scaled MACD crossover except instead of buying a set number per day, it has a constantly incremented `current_scale` factor.
                - This number is increased on bullish days and decreased on bearish days.
                - It is also used as the number of stock to buy on any given day.
5. Print net_worth columns to the console.

6. Run the plotting function (`compare_plot_fn.py`)
    - Relevant arguments are listed below:
        - `save_image`
            - By default this is blank and no image is saved
            - If its anything other than blank, the string will be used as the file name for an image of the plot.
        - `names`
            - List of strategy names from the `add_strategies()` function
    - The plotting function uses the `names` list to generate a twinx axis for each strategy.
    - Plots the net_worth of each strategy as time goes on.
        - Plots the S&P500 one a bit differently so its more of a benchmark.
    - Dynamically scales the Y axis based on the max and min values that appear in the run.
    - Adds an annotation with info on each strategy to the left side.

## To do

- Add more strategies.
