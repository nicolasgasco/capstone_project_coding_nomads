import os
import tweepy
import json
import re
from pprint import pprint

# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']


# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
handle = 'NekoJitaBlog'  # for example purposes; prop any handle you want!
user = api.get_user(handle)

def print_account_info(user):
    """Function to print the user's name, number of followed, and number of followers"""
    num_friends = user.friends_count
    screen_name = user.screen_name
    followers_count = user.followers_count
    print(f"The user @{screen_name} is following {num_friends} accounts and has {followers_count} followers")
