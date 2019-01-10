from flask import render_template, request
from app import app

import pandas as pd
import numpy as np
from azure.storage.blob import BlockBlobService, ContentSettings
import json

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Range1d
from bokeh.embed import components

def RetrieveAzureData():
    with open('./credentials.json') as f:
        creds = json.load(f)

    block_blob_service = BlockBlobService(account_name=creds['azure']['account_name'],
                                        account_key=creds['azure']['account_key'])

    block_blob_service.get_blob_to_path(
        creds['azure']['container'], 'Twitter_data.csv', 'Twitter_data.csv')
    block_blob_service.get_blob_to_path(
        creds['azure']['container'], 'CMC_data.csv', 'CMC_data.csv')

    print("Twitter_data.csv and CMC_data.csv successfully retrieved from Azure blob storage")

def parseToPandasDF(csv_file):
    with open(csv_file) as file:
        df = pd.read_csv(file, index_col=0, parse_dates=True)
        pd.to_datetime(df.index)
        df.index.name = 'Date'
        return df

def create_figure(coin, df1, df2):
    price = ColumnDataSource(df1)

    diff = np.diff(df2[coin])
    tweet_df = pd.DataFrame({coin:diff}, index=df1.index.values[1:])
    tweet_df.index.name = 'Date'
    tweets = ColumnDataSource(tweet_df)

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=400)
    
    p.extra_y_ranges = {'Tweets' : Range1d(start=min(diff), end=2*max(diff))}
    p.add_layout(LinearAxis(y_range_name='Tweets', axis_label='Volume of Tweets'), 'right')


    p.line('Date', coin, source=price, line_color="#f46d43")
    p.line('Date', coin, source=tweets, y_range_name='Tweets' )

    p.xaxis.axis_label = 'Time'


    return p

@app.route('/')
def index():
    RetrieveAzureData()

    twitter_df = parseToPandasDF("Twitter_data.csv")
    cmc_df = parseToPandasDF("CMC_data.csv")

    coin_names = cmc_df.columns

    current_coin = request.args.get("current_coin")
    if current_coin == None:
        current_coin = 'bitcoin'

    script, div = components(create_figure(current_coin, cmc_df, twitter_df))

    return render_template('bokeh.html',script=script, div=div, coin_names=coin_names, current_coin=current_coin)
