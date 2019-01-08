from RetrieveAzureData import retrieveAzureData
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import grangercausalitytests

retrieveAzureData()

def parseToPandasDF(csv_file):
    with open(csv_file) as file:
        df = pd.read_csv(file, index_col=0, parse_dates=True)
        pd.to_datetime(df.index)
        return df

twitter_df = parseToPandasDF("Twitter_data.csv") 
cmc_df = parseToPandasDF("CMC_data.csv") 

array = df[['bitcoin', 'bitcoincash']].values

grangercausalitytests(array, maxlag=30)

fig, ax = plt.subplots()

dayTicks = mdates.DayLocator(interval = 1)
hourTicks = mdates.HourLocator(interval = 4)

dayFmt = mdates.DateFormatter('%d/%m/%y')
hourFmt = mdates.DateFormatter('%H:%M')


# ax.plot(df.index, df['ethereum'], linewidth = 2)

diff = np.diff(df['bitcoin'])
ax.plot(df.index[1:], diff, linewidth=1)
ax.xaxis.set_major_locator(dayTicks)
ax.xaxis.set_minor_locator(hourTicks)
ax.xaxis.set_major_formatter(dayFmt)
ax.xaxis.set_minor_formatter(hourFmt)

fig.autofmt_xdate()

#test
try:
    plt.show()
except (KeyboardInterrupt):
    plt.close()


