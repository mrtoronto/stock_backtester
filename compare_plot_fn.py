import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plot_fn(df, names, cash, test_symbol, save_image=''):

    fig, ax1 = plt.subplots(figsize = (12,8))
    fig.subplots_adjust(left=.3)
    plt.xlabel("Date", labelpad=15)
    plt.title("S&P500 Buy and Hold vs Trading Strategy(s)", pad=15, fontsize=18, weight='bold')
    plt.ylabel("Value of account ($)")
    plt.grid(True, which='both', axis='both', alpha=.5)
    fig.autofmt_xdate()
    ax1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

    ylim_max_list = []
    ylim_min_list = []
    ax_list = []
    ### Fill out ax_list, max_list and min_list with values
    for name in names:
        ax_list.append(ax1.twinx())

        ylim_max_list.append(df["{}_net_worth".format(name)].max())
        ylim_min_list.append(df["{}_net_worth".format(name)].min())

    ylim_max_val = np.max(ylim_max_list)
    ylim_min_val = np.min(ylim_min_list)

    ### First color is grey but others can be changed
    ### https://medialab.github.io/iwanthue/
    colors = ['#929591', '#b6739d', '#72a555', '#638ccc', '#ad963d'][:len(names)]
    for ax, name, color in zip(ax_list, names, colors):
        if 'sp' in name:
            alpha = .5
            linewidth=2
        else:
            alpha = 1
            linewidth=4
        ax.plot_date(x=df["Date"], y=df["{}_net_worth".format(name)],
                    linestyle='-', linewidth=linewidth, markersize=0, alpha=alpha, color=color,
                    label="'{}' Net Worth".format(name))

    for ax, name in zip(ax_list, names):
        ax.set_ylim([ylim_min_val * .8, ylim_max_val * 1.1])
    ax1.set_ylim([ylim_min_val * .8, ylim_max_val * 1.1])
    
    fig.legend(loc='upper left', fontsize = 'medium')

    length_days = df.shape[0]
    length_years = round(length_days / 253, 3) # 253 trading days in a year according to Google
    caption_str = """{length} days - {length_year} years\nStarting Cash: ${cash}\n${symbol} Stock\n""".format(length = length_days, length_year = length_years, cash=cash, symbol = test_symbol)
    for name in names:
        final_net = round(df.loc[df.index[-1], "{}_net_worth".format(name)], 2)
        dollar_gain = round(final_net - cash, 2)
        perc_gain = round(100*(dollar_gain / cash), 3)

        caption_str += '\n' + '{name}'.format(name=name)
        caption_str += '\n    Final Net: ${net_worth}'.format(net_worth = final_net)
        caption_str += '\n    Profit:    ${gain_dol} ({gain_perc}%)\n'.format(gain_dol=dollar_gain, gain_perc = perc_gain)

    print(caption_str)
    fig.text(0.02, .5, caption_str,va='center', ha='left', fontsize=9)

    if save_image != '':
        if not os.path.exists("output_files"):
            os.mkdir('output_files')
        plt.savefig('output_files/' + save_image)

    plt.show()
