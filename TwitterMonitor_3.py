#!/home/vcm/.pyenv/shims/python3.7
import tweepy
import pandas as pd
import numpy as np
import sys
from slacker import Slacker
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import timezone
import re

#Twitter App access keys
# Consume:
CONSUMER_KEY = 'VOuHwMgk0JWZEEpddjGl2OVsG'
CONSUMER_SECRET = 'oEsl4A2a2t5MnKd14q0KStLavPbU8WhNFTwrlFS042QhAmx3BF'

# Access:
ACCESS_TOKEN = '1066881360579698689-tBP2JjznBg7jNVAdCBU7YrjT1CRDXI'
ACCESS_SECRET = 'NWcqLuA8ULlIiCU7jk60bQ1ZdR992WQNX0rZnyMXedr9T'

slack = Slacker('xoxb-818172236657-827951422327-arzd2Oq5iDwyjiUuid1cwpQY')

import os
cd = os.getcwd()

dff = pd.read_csv(cd+"/TwitterA.csv")

def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

for index, row in dff.iterrows():

    twt = row['TwitterAccount']

    

    extractor = twitter_setup()

    

    # We create a tweet list as follows:

    tweets = extractor.user_timeline(screen_name=twt, count=200)

    data = pd.DataFrame(columns=['Account','Tweets','Date'])

    for tweet in tweets:

        t = {"Account":str(twt),"Tweets":str(tweet.text),"Date":tweet.created_at}

        data = data.append(t,ignore_index=True)

        

    created_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)

    data = data[(data['Date'] > created_time) & (data['Date'] < datetime.datetime.utcnow())]

    

    if(len(data) > 0):

        slack.chat.post_message(text='#ops-twitter-alerts' + data['Tweets'], channel="general")

        with open("update_monitor.csv", 'a',encoding="utf-8") as f:

            data.to_csv(f)

    else:

        print("There is no updated tweet for",twt)