from eca import *
from eca.generators import start_offline_tweets
from eca.http import GenerateEvent
import datetime
import textwrap
import random

def add_request_handlers(httpd):
   httpd.add_route('/', GenerateEvent('search'), methods=['POST'])

   httpd.add_content('/lib/', 'twitter_static/lib')
   httpd.add_content('/style/', 'twitter_static/style')

@event('init')
def setup(ctx, e):
   start_offline_tweets('tweets.txt', time_factor=1, event_name='chirp')
#    start_offline_tweets('test.txt', time_factor=1, event_name='chirp')
   ctx.count = 0.0001
   ctx.interval = datetime.datetime.now()
   ctx.keyword = None
   ctx.intervalgraph = 3
   start_offline_tweets('tweets.txt', time_factor=1, event_name='tweetgraph')

@event('chirp')
def tweet(ctx, e):
   # we receive a tweet
   tweet = e.data
   if not ctx.keyword or ctx.keyword.lower() in tweet['text'].lower() or ctx.keyword.lower() in tweet['user']['screen_name'].lower() or ctx.keyword.lower() in tweet['user']['name'].lower():
      # parse date
      time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

      # nicify text
      text = textwrap.fill(tweet['text'],initial_indent='    ', subsequent_indent='    ')

      # generate output
      output = "[{}] {} (@{}):\n{}".format(time, tweet['user']['name'], tweet['user']['screen_name'], text)
   #    emit('tweet', output)
      emit('tweet', tweet)

@event('tweetgraph')
def generate_graph(ctx, e):
   delta = datetime.datetime.now() - ctx.interval
   if delta.total_seconds() < ctx.intervalgraph:
      tweet = e.data
      if not ctx.keyword or ctx.keyword.lower() in tweet['text'].lower():
         ctx.count += 1
   else:   
      emit('tweetgraph',{
         'action': 'add',
         'value': ctx.count
      })
      ctx.interval = datetime.datetime.now()
      ctx.count = 0.0001

@event('search')
def on_search(ctx, e):
   ctx.keyword = e.data['search']


@event('intervalbtn')
def set_interval(ctx,e):
   print(e.data['intervalbtn'])
   ctx.intervalgraph = int(e.data['intervalbtn'])