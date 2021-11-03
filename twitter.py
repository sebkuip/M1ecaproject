from eca import *

from eca.generators import start_offline_tweets
import datetime
import textwrap

@event('init')
def setup(ctx, e):
   start_offline_tweets('sports_tweets.txt', time_factor=100000, event_name='chirp')
#    start_offline_tweets('test.txt', time_factor=100000, event_name='chirp')

@event('chirp')
def tweet(ctx, e):
   # we receive a tweet
   tweet = e.data

   # parse date
   time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

   # nicify text
   text = textwrap.fill(tweet['text'],initial_indent='    ', subsequent_indent='    ')

   # generate output
   output = "[{}] {} (@{}):\n{}".format(time, tweet['user']['name'], tweet['user']['screen_name'], text)
   print("tweet", output)
#    emit('tweet', output)
   emit('tweet', tweet)