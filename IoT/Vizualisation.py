from RetrieveAzureData import RetrieveAzureData
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.api import tsa

# RetrieveAzureData()

def parseToPandasDF(csv_file):
    with open(csv_file) as file:
        df = pd.read_csv(file, index_col=0, parse_dates=True)
        pd.to_datetime(df.index)
        return df


twitter_df = parseToPandasDF("Twitter_data.csv")
cmc_df = parseToPandasDF("CMC_data.csv")


def FormatTimeAxis(xaxis, hourInterval=12):
    dayTicks = mdates.DayLocator(interval=1)
    hourTicks = mdates.HourLocator(interval=hourInterval)
    dayFmt = mdates.DateFormatter('%d/%m/%y')
    hourFmt = mdates.DateFormatter('%H:%M')
    xaxis.set_major_locator(dayTicks)
    xaxis.set_major_formatter(dayFmt)
    xaxis.set_minor_locator(hourTicks)
    xaxis.set_minor_formatter(hourFmt)


def GenerateHistograms():
    fig, ax = plt.subplots(nrows=1, ncols=6)
    fig.set_size_inches(45, 6)
    idx = 0

    for coin in cmc_df.columns:
        series = np.diff(twitter_df[coin].values)
        series = np.diff(twitter_df[coin].values)
        ax[idx].hist(series, bins=20)
        ax[idx].set_title("{}".format(coin), fontsize=24)
        idx += 1

    plt.savefig('./Resources/tweet_histograms.png')


def raw_plot(coin):
    fig, ax = plt.subplots()
    ax.set_title("{}".format(coin), fontsize=24)
    fig.set_size_inches(10, 5)

    ax.set_xlabel('Time')

    ax.plot(twitter_df.index, twitter_df[coin], color='b', linewidth=2)
    ax.set_ylabel('Number of Tweets', color='b')
    ax.yaxis.label.set_fontsize(16)
    ax.tick_params('y', labelsize=10)

    ax2 = ax.twinx()
    ax2.plot(cmc_df.index, cmc_df[coin], color='g', linewidth=2)
    ax2.yaxis.label.set_fontsize(16)
    ax2.set_ylabel('Price (USD)', color='g')
    ax2.tick_params('y', labelsize=10)

    FormatTimeAxis(ax.xaxis, hourInterval=9)

    fig.autofmt_xdate()
    fig.savefig('./Resources/{}_raw_plot.png'.format(coin))


def norm_diff_plot(coin):

    diff = np.diff(twitter_df[coin])
    norm_tweets = (diff - np.mean(diff))/np.std(diff)

    norm_prices = (cmc_df[coin] - np.mean(cmc_df[coin]))/np.std(cmc_df[coin])
    fig, ax = plt.subplots()

    ax.set_title("{}".format(coin), fontsize=24)
    fig.set_size_inches(10, 5)

    ax.set_xlabel('Time')

    ax.plot(twitter_df.index[1:], norm_tweets, color='b', linewidth=0.2)
    ax.yaxis.label.set_fontsize(16)
    ax.tick_params('y', labelsize=10)
    ax.plot(cmc_df.index[1:], norm_prices[1:], color='g', linewidth=1)

    FormatTimeAxis(ax.xaxis, hourInterval=9)

    fig.autofmt_xdate()
    fig.savefig('./Resources/{}_norm_plot.png'.format(coin))

def seasonality(coin):
    tweets = np.diff(twitter_df[coin])
    # pd.DataFrame(data)
    freq = round(1*1440/4.5)
    decomposed = tsa.seasonal_decompose(tweets, freq=freq)
    decomposed.plot()

    plt.savefig('./Resources/{}_seasonal_plot.png'.format(coin))

def pearsonR(coin):
    print(coin)
    return (scipy.stats.pearsonr(np.diff(twitter_df[coin]), cmc_df[coin][1:]))


def crossPlot(coin):
    fig, ax = plt.subplots()

    fig.set_size_inches(10, 10)

    ax.set_xlabel("{} price".format(coin))
    ax.set_ylabel("Number of {} tweets".format(coin))

    ax.scatter(cmc_df[coin][1:],np.diff(twitter_df[coin]), color='b', linewidth=2)

def crossPlot_diff(coin):
    fig, ax = plt.subplots()

    fig.set_size_inches(10, 10)

    ax.set_xlabel("{} price".format(coin))
    ax.set_ylabel("Number of {} tweets".format(coin))

    ax.scatter(np.diff(cmc_df[coin]),np.diff(twitter_df[coin]), color='b', linewidth=2)



def auto():
    coin = 'bitcoin'
    fig = plt.figure()
    fig.add_subplot(121)
    plot_acf(np.diff(twitter_df[coin].values), lags=10)
    fig.add_subplot(122)
    plot_acf(np.diff(twitter_df[coin].values), lags=10)

# crossPlot_diff('xrp')
# Causality('bitcoin', 100)
# Causality2('bitcoin', 100)

plt.show()