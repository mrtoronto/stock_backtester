"""
Function will take in a DataFrame, list of strategy names, amount of starting cash, ticker that's being tested and the image save location.


"""


import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plot_fn(df, names, cash, test_symbol, save_image=''):
    
    fig, ax1 = plt.subplots(figsize = (12,8))
    ### Push left boarder 30% to the right to make room for the large annotation
    fig.subplots_adjust(left=.3)
    ### Labels
    plt.xlabel("Date", labelpad=15)
    plt.ylabel("Value of account ($)")
    plt.title("S&P500 Buy and Hold vs Trading Strategy(s)", pad=15, fontsize=18, weight='bold')
    ### Grid
    plt.grid(True, which='both', axis='both', alpha=.5)
    ### Format dates on the x-axis
    fig.autofmt_xdate()
    ax1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    ### Lists that'll eventually have the max and mins of each *_net_worth column
    ylim_max_list = []
    ylim_min_list = []
    ### List of axes of the plot
    ax_list = []
    ### Fill out ax_list, max_list and min_list with appropriate values for each strategy
    for name in names:
        ### Clone the original axis, keeping the X values
        ax_list.append(ax1.twinx())
        ### Append the max and min of the *_net_worth column, for scaling later
        ylim_max_list.append(df["{}_net_worth".format(name)].max())
        ylim_min_list.append(df["{}_net_worth".format(name)].min())
    
    ### Take the max of the max list and the min of the min list
    ylim_max_val = np.max(ylim_max_list)
    ylim_min_val = np.min(ylim_min_list)

    ### List of colors to use for lines in plot
    ### I'd recommend using the below link to get groups of optimally different colors
    ### https://medialab.github.io/iwanthue/
    ### The first color should stay grey-ish as that's the S&P500 benchmark line
    colors = ['#929591', '#b6739d', '#72a555', '#638ccc', '#ad963d'][:len(names)]
    
    ### Iterate through a zip of the axes, names and colors and plot
    for ax, name, color in zip(ax_list, names, colors):
        ### Do some special formatting for the S&P500 benchmark line
        if 'sp' in name:
            alpha = .5
            linewidth=2
        else:
            alpha = 1
            linewidth=4
        ax.plot_date(x=df["Date"], y=df["{}_net_worth".format(name)],
                    linestyle='-', linewidth=linewidth, markersize=0, alpha=alpha, color=color,
                    label="'{}' Net Worth".format(name))
    ### Set all the axes y-limit
    for ax, name in zip(ax_list, names):
        ax.set_ylim([ylim_min_val * .8, ylim_max_val * 1.1])
    ax1.set_ylim([ylim_min_val * .8, ylim_max_val * 1.1])
    
    fig.legend(loc='upper left', fontsize = 'medium')

    
    ### Create the annotation with the run data
    length_days = df.shape[0]
    length_years = round(length_days / 253, 3) # 253 trading days in a year according to Google
    caption_str = """{length} days - {length_year} years\nStarting Cash: ${cash}\n${symbol} Stock\n""".format(length = length_days, length_year = length_years, cash=cash, symbol = test_symbol)
    for name in names:
        ### Take the last value from the *_net_worth column as the Final Net Worth, round it to 2 decimals
        final_net = round(df.loc[df.index[-1], "{}_net_worth".format(name)], 2)
        ### Subtract final from starting to get profit
        dollar_gain = round(final_net - cash, 2)
        ### Divide profit by start cash to get percent gain
        perc_gain = round(100*(dollar_gain / cash), 3)
        ### Put it all together
        caption_str += '\n' + '{name}'.format(name=name)
        caption_str += '\n    Final Net: ${net_worth}'.format(net_worth = final_net)
        caption_str += '\n    Profit:    ${gain_dol} ({gain_perc}%)\n'.format(gain_dol=dollar_gain, gain_perc = perc_gain)
    
    print(caption_str)
    fig.text(0.02, .5, caption_str,va='center', ha='left', fontsize=9)
    ### If `save_image` is not blank, save an image of the plot to that location
    if save_image != '':
        if '.png' not in save_image:
            save_image += '.png'
        ### Check if "output_files" directory exists
        if not os.path.exists("output_files"):
            os.mkdir('output_files')
        plt.savefig('output_files/' + save_image)

    plt.show()
