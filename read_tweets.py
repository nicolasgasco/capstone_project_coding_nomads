import os
import tweepy
from pprint import pprint
import json
import re
from random import randint

# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']


# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create the connection
limit_search = 10
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="python",
lang="en",
since=2020-12-3).items(limit_search)


def generate_dict(dataset, number):
    """Function to generate a list of tweets in form of dictionaries"""
    data_list = []
    for data in dataset:
        data_dict = {}
        data_dict["id"] = data.id
        data_dict["text"] = data.text
        data_dict["followers_count"] = data.user.followers_count
        status = api.get_status(data_dict["id"], tweet_mode="extended")
        data_dict["full_text"] = status.full_text
        data_dict["friends_count"] = data.user.friends_count
        data_dict["screen_name"] = data.user.screen_name
        data_dict["statuses_count"] = data.user.statuses_count
        data_list.append(data_dict)
    return data_list


def average_followers(dataset, number):
    """Function to calculate the average number of followers"""
    total_followers = 0
    for data in dataset:
        followers = data["followers_count"]
        average = followers / number
    return average


def average_length_word(dataset, number):
    """Function to determine the average length of tweet in words"""
    pattern = re.compile(r"\w+")
    total_words = 0
    for data in dataset:
        text = data["full_text"]
        for match in re.finditer(pattern, text):
            total_words += 1
    average = total_words / number
    return average


def average_length_char(dataset, number):
    """Function to determine the average length of tweet in characters"""
    total_chars = 0
    for data in dataset:
        text = data["full_text"]
        total_chars += len(text)
    average = total_chars / number
    return average


def tweets_with(dataset, number, symbol):
    """Function to determine the percentage of tweeet containing a specific symbol"""
    tweets_with_hashtag = 0
    for data in dataset:
        if symbol in data["full_text"]:
            tweets_with_hashtag += 1
    percentage = (tweets_with_hashtag * 100) / number
    return percentage


def percentage_tweet_punctuation(dataset, number):
    """Function to determine the percentage of tweets with punctuation"""
    pattern = re.compile(r"[!?.,;'\"\/\|\[\]{}()]")
    tweets_with_punctuation = 0
    for data in dataset:
        text = data["full_text"]
        r = re.search(pattern, text)
        if r:
            tweets_with_punctuation += 1
    percentage = (tweets_with_punctuation * 100) / number
    return percentage

def _words_without_hash_mentions(tweet):
    """Function to get list of words in tweet without hashtags and mentions"""
    pattern = re.compile(r"\b\w+\b")
    pattern2 = re.compile(r"[#|@]\w+")
    pattern3 = re.compile(r"https?:\/\/[-a-zA-Z0-9@:%._\+~#=]*\/?\w*")
    pattern4 = re.compile(r"\b\d+\b")
    word_list = []
    text = tweet["full_text"]
    # Remove all links from tweets
    for match in re.finditer(pattern3, text):
        text = text.replace(match.group(), "")
    # Remove all mentions and hashtags
    for match in re.finditer(pattern2, text):
        text = text.replace(match.group(), "")
    # Remove all singles numbers
    for match in re.finditer(pattern4, text):
        text = text.replace(match.group(), "")
    for match in re.finditer(pattern, text):
    # Attach all words except "RT" from "retweet"
        if match.group() != "RT":
            word_list.append(match.group())
    return word_list

def longest_word_tweet(tweet):
    """Function to find the longest word in a tweet (hashtags and mentions excluded)"""
    longest_word = ""
    word_list = _words_without_hash_mentions(tweet)
    for word in word_list:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word


def shortest_word_tweet(tweet):
    """Function to find the short word in a tweet (hashtags and mentions excluded)"""
    word_list = _words_without_hash_mentions(tweet)
    shortest_word = word_list[0]
    for word in word_list:
        if len(word) < len(shortest_word):
            shortest_word = word
    return shortest_word

def find_most_statuses(dataset):
    """Functions to find user with most tweets"""
    highest_statuses = 0
    for data in dataset:
        if data["statuses_count"] > highest_statuses:
            highest_statuses = data["statuses_count"]
    return highest_statuses


def find_user_statuses(dataset, statuses):
    """Function to find the username of a certain status count"""
    username = ""
    for data in dataset:
        if data["statuses_count"] == statuses:
            username += data["screen_name"]
    return username

tweets = generate_dict(tweets, limit_search)

# The average number of followers.
print(f"The average number of followers is {average_followers(tweets, limit_search)}.")

# The average length of tweets (counting words).
print(f"The average number of words per tweet is {average_length_word(tweets, limit_search)}.")

# The average length of tweets (counting characters).
print(f"The average number of characters per tweet is {average_length_char(tweets, limit_search)}.")

# The percentage of tweets that have a hashtag (#).
print(f"The percentage of tweets with hashtags is {tweets_with(tweets, limit_search, '#')}%.")

# The percentage of tweets that have a mention (@).
print(f"The percentage of tweets with a mention (@) is {tweets_with(tweets, limit_search, '@')}%.")

# The 100 most common words.

# The 100 most common symbols.

# Percentage of tweets that use punctuation.
print(f"The percentage of tweets containing punctuation is {percentage_tweet_punctuation(tweets, limit_search)}%.")

# The longest word in a tweet.
random_tweet = tweets[randint(0, limit_search -1)]
longest_word = longest_word_tweet(random_tweet)
print(f"The longest word of this random tweet is: {longest_word}.")

# Shortest word in a tweet.
shortest_word = shortest_word_tweet(random_tweet)
print(f"The shortest word of this random tweet is: {shortest_word}.")

# What user has the most tweets in the dataset?
highest_status = find_most_statuses(tweets)
highest_status_user = find_user_statuses(tweets, highest_status)
print(f"The user with the highest status count is: {highest_status_user} with {highest_status} statuses.")

# The average number of tweets from an individual user.
# The hour with the greatest number of tweets.