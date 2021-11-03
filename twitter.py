from eca import *

from eca.generators import start_offline_tweets
import datetime
import textwrap
import random


@event('init')
def setup(ctx, e):
   start_offline_tweets('tweets.txt', time_factor=1, event_name='chirp')
#    start_offline_tweets('test.txt', time_factor=1, event_name='chirp')
   ctx.count = 0
   ctx.interval = datetime.datetime.now()
   start_offline_tweets('tweets.txt', time_factor=1, event_name='tweetgraph')

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
#    emit('tweet', output)
   emit('tweet', tweet)

@event('tweetgraph')
def generate_sample(ctx, e):
   delta = datetime.datetime.now() - ctx.interval
   if delta.total_seconds() < 3:
      ctx.count += 1
   else:   
      emit('tweetgraph',{
         'action': 'add',
         'value': ctx.count
      })
      ctx.interval = datetime.datetime.now()
      ctx.count = 0