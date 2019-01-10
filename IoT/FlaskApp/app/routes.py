from flask import render_template, request
from app import app

import pandas as pd
from azure.storage.blob import BlockBlobService, ContentSettings
import json

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
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

def create_figure(df, coin):
    source = ColumnDataSource(df)
    p = figure(x_axis_type="datetime", plot_width=800, plot_height=400)
    p.line('Date', coin, source=source)

    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Price (USD)'

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

    script, div = components(create_figure(cmc_df, current_coin))

    return render_template('bokeh.html',script=script, div=div, coin_names=coin_names, current_coin=current_coin)
