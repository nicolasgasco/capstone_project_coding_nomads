import os
import tweepy
from pprint import pprint
import json
import re

# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']


# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create the connection
limit_search = 5
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)

# for tweet in tweets:
#     print(tweet)
#     print(tweet.user.screen_name, f"(user ID: {tweet.user.id}) wrote:")
#     print(tweet.text)
#     print(f"Date: {tweet.created_at}\n")



def average_followers(dataset, number):
    """Function to calculate the average number of followers"""
    total_followers = 0
    for data in dataset:
        followers = data.user.followers_count
        total_followers += followers
    average = total_followers / number
    return average


def average_length_word(dataset, number):
    """Function to determine the average length of tweet in words"""
    pattern = re.compile(r"\w+")
    total_words = 0
    for data in dataset:
        text = data.text
        for match in re.finditer(pattern, text):
            total_words += 1
    average = total_words / number
    return average


def average_length_char(dataset, number):
    """Function to determine the average length of tweet in characters"""
    total_chars = 0
    for data in dataset:
        text = data.text
        total_chars += len(text)
    average = total_chars / number
    return average


def tweets_with(dataset, number, symbol):
    """Function to determine the percentage of tweeet containing a specific symbol"""
    tweets_with_hashtag = 0
    for data in dataset:
        if symbol in data.text:
            tweets_with_hashtag += 1
    percentage = (tweets_with_hashtag * 100) / number
    return percentage


# The average number of followers.
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)
print(f"The average number of followers is {average_followers(tweets, limit_search)}.")

# The average length of tweets (counting words).
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)
print(f"The average number of words per tweet is {average_length_word(tweets, limit_search)}.")



# The average length of tweets (counting characters).
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)
print(f"The average number of characters per tweet is {average_length_char(tweets, limit_search)}.")

# The percentage of tweets that have a hashtag (#).
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)

print(f"The percentage of tweets with hashtags is {tweets_with(tweets, limit_search, '#')}%.")

# The percentage of tweets that have a mention (@).
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)

print(f"The percentage of tweets with a mention (@) is {tweets_with(tweets, limit_search, '@')}%.")


# The 100 most common words.
# The 100 most common symbols.
# Percentage of tweets that use punctuation.
# The longest word in a tweet.
# Shortest word in a tweet.
# What user has the most tweets in the dataset?
# The average number of tweets from an individual user.
# The hour with the greatest number of tweets.