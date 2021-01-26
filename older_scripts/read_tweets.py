import os
import tweepy
import json
from pprint import pprint


# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create the connection
api = tweepy.API(auth)

# define a handle to inspect for quicker reference
handle = 'codingnomads' # for example purposes; prop any handle you want!
tweets = api.user_timeline(handle)

# write tweet data to a JSON file
tweet_list = []
for tweet in tweets:
    # pprint(tweet._json)  # uncomment to see the tweet data
    tweet_list.append(tweet._json)

with open('data.json', 'w') as f:
    json.dump(tweet_list, f)
