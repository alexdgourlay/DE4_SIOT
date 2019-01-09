import requests
import pandas as pd
import json
import tweepy
import schedule
import time
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

with open('./credentials.json') as f:
    creds = json.load(f)

block_blob_service = BlockBlobService(account_name=creds['azure']['account_name'],
                                      account_key=creds['azure']['account_key'])


'''-------CoinMarketCap--------- '''
coin_data = requests.get(creds['cmc']['api']+creds['cmc']['key']).json()

coin_names = []

for coin in coin_data['data']:
    if len(coin_names) < 6:
        coin_names.append(coin['name'])
    else:
        break

columns = [x.lower().replace(" ", "") for x in coin_names]

coin_df = pd.DataFrame(columns=columns, index=pd.to_datetime([]))

'''------- Twitter ----------'''

auth = tweepy.OAuthHandler(
    creds['twitter']['key'], creds['twitter']['secret_key'])

auth.set_access_token(creds['twitter']['token'],
                      creds['twitter']['secret_token'])

twitter_df = pd.DataFrame(columns=columns, index=pd.to_datetime([]))

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True, compression=True)

count_dict = {}

def InitTweetCounts():
    for coin in columns:
        count_dict[coin] = 0

InitTweetCounts()

def CountTweets(tweet):
    for word in tweet.split():
        word.lower().replace(" ", "")
        if word.startswith('#'):
            word = word[1:]
        if (word in list(twitter_df.columns.values)):
            count_dict[word] += 1

class StreamListener(tweepy.StreamListener):

    def __init__(self):
        tweepy.StreamListener.__init__(self)
        self.connected = False

    def on_connect(self):
        print('Twitter Stream Connected')
        self.connected = True

    def on_disconnect(self):  
        print('Twitter Stream Disconnected')
        self.connected = False

    def on_status(self, status):
        CountTweets(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=columns, is_async=True)


'''--------RUN-----------'''

def run():
    print ("Running!")

    coin_data = requests.get(creds['cmc']['api']+creds['cmc']['key']).json()

    timestamp = pd.Timestamp('now')

    for coin in coin_data['data']:
        if coin['name'] in coin_names:
            coin_df.loc[timestamp, coin['name'].lower().replace(" ", "")] = coin['quote']['USD']['price']

    coin_df.to_csv('CMC_data.csv')

    block_blob_service.create_blob_from_path(
        creds['azure']['container'],
        'CMC_data.csv',
        'CMC_data.csv',
        content_settings=ContentSettings(content_type='application/CSV')
    )

    if not listener.connected:
        print('Twitter stream dropped... Trying to reconnect...')
        time.sleep(2)
        stream.filter(track=columns, is_async=True)

    for coin, count in count_dict.items():
            if coin in twitter_df.columns:
                twitter_df.loc[timestamp, coin] = count

    twitter_df.to_csv('Twitter_Data.csv')
        
    block_blob_service.create_blob_from_path(
        creds['azure']['container'],
        'Twitter_data.csv',
        'Twitter_data.csv',
        content_settings=ContentSettings(content_type='application/CSV')
    )

schedule.every(4.5).minutes.do(run)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except (KeyboardInterrupt):
    stream.disconnect()

