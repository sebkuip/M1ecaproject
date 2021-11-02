from eca import *
import json

import random

## You might have to update the root path to point to the correct path
## (by default, it points to <rules>_static)
root_content_path = 'Dashboard'

# binds the 'setup' function as the action for the 'init' event
# the action will be called with the context and the event
@event('init')
def setup(ctx, e):
    with open("Dashboard/tweets.json", "r", encoding='utf8') as f:
        ctx.tweet_data = json.load(f)


# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))

@event('sample')
def generate_sample(ctx, e):
    ctx.count += 1
    if ctx.count % 50 == 0:
        emit('debug', {'text': 'Log message #'+str(ctx.count)+'!'})

    # base sample on previous one
    sample = clip(-100, e.data['previous'] + random.uniform(+5.0, -5.0), 100)

    # emit to outside world
    emit('sample',{
        'action': 'add',
        'value': sample
    })

    # chain event
    fire('sample', {'previous': sample}, delay=0.05)

