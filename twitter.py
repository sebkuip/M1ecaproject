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
   fire('sample', {'previous': 0.0}) 

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

@event('sample')
def generate_sample(ctx, e):
    ctx.count += 1
    if ctx.count % 50 == 0:
        emit('debug', {'text': 'Log message #'+str(ctx.count)+'!'})

    # base sample on previous one
    sample = clip(0.1, e.data['previous'] + random.uniform(+1.0, -1.0), 9.9)

    # emit to outside world
    emit('sample',{
        'action': 'add',
        'value': sample
    })

    # chain event
    fire('sample', {'previous': sample}, delay=0.05)