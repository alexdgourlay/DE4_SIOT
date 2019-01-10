from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.api import tsa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Vizualisation import parseToPandasDF

twitter_df = parseToPandasDF("Twitter_data.csv")
cmc_df = parseToPandasDF("CMC_data.csv")

def isStationary(df, coin, sigLevel=.05):
    adftest =  tsa.stattools.adfuller(df[coin], autolag='AIC')

    if (adftest[1] < sigLevel):
        return {"p Value" : round(adftest[1],3),  "Stationary" : True}
    else:
        return {"p Value" : round(adftest[1],3),  "Stationary" : False}
   
def checkStationarity(df):
    d = {}
    for coin in df:
        d[coin] = isStationary(df,coin)
    return d

# print(checkStationarity(twitter_df))
# print(checkStationarity(cmc_df))


def Causality(coin, lag):
    fig, ax = plt.subplots()

    array = [cmc_df[coin].values[1:], np.diff(twitter_df[coin].values)]
    array = np.asarray(array).transpose()

    gc_test = grangercausalitytests(array, maxlag=lag, verbose=False)
    pvals = [gc_test.get(i+1)[0].get('ssr_ftest')[1]
                for i in range(0, lag)]

    ax.set_xlabel("Number of Lags")
    ax.set_ylabel("Granger Causality p Value")
    
    ax.set_title("{}".format(coin), fontsize=24)
    
    minPoint =[pvals.index(min(pvals[5:])), min(pvals[5:])]
    ax.scatter(minPoint[0], minPoint[1], 200, color='r')
    ax.annotate('(%s, %.3f)' % (minPoint[0], minPoint[1]), xy=minPoint, textcoords='data')
    ax.plot(pvals)
    fig.autofmt_xdate()
    plt.savefig('./Resources/{}_granger_plot.png'.format(coin))

    return minPoint

