from eca import *
from eca.generators import start_offline_tweets

import datetime
import textwrap

@event('init')
def setup(ctx, e):
    # start the offline tweet stream
    start_offline_tweets('Dashboard/tweets.txt', event_name='chirp', time_factor=10000)

@event('chirp')
def tweet(ctx, e):
    # we receive a tweet
    tweet = e.data


    # nicify text
    text = tweet['text']

    emit('tweet', text)