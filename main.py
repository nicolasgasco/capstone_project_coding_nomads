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


def json_to_list(filename):
    """Function to import data set from a JSON file"""
    with open(filename) as f:
        tweets = json.load(f)
    return tweets


def calculate_average_tweet(dataset):
    """Function to calculate the average length of tweets in data set"""
    dataset_length = 0
    for data in dataset:
        dataset_length += len(data["text"])
    average = dataset_length / len(dataset)
    return average

def _print_average(average):
    """Function to print the average number of characters in a tweet"""
    print(f"The average number of characters per tweet is roughly {int(average)} characters.")

def longest_word_tweet(tweet):
    """Function to determine the longest word of a single tweet"""
    pattern = re.compile(r"\w+")
    single_words = []
    for match in re.finditer(pattern, tweet):
        single_words.append(match.group())
    longest = max(single_words, key=len)

    print(f"The longest word in this tweet is: {longest}")



tweets = json_to_list("data.json")

# Average length of tweets in characters
average_length = calculate_average_tweet(tweets)
_print_average(average_length)

# Longest word in a single tweet
longest_word_tweet(tweets[6]["text"])


# The average number of followers that users have