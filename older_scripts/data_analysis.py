import os
import tweepy
import json
import re
from pprint import pprint

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


def _print_average_characters(average):
    """Function to print the average number of characters in a tweet"""
    print(f"The average number of characters per tweet is roughly {int(average)} characters.")


def longest_word_tweet(tweet):
    """Function to determine the longest word of a single tweet"""
    pattern = re.compile(r"\w+")
    single_words = []
    for match in re.finditer(pattern, tweet):
        single_words.append(match.group())
    longest = max(single_words, key=len)
    return longest

def _print_longest_word(longest):
    """Function to print the longest word in the tweet"""
    print(f"The longest word in this tweet is: {longest}.")


def follower_average(tweets):
    followers = 0
    for i in range(len(tweets)):
        follower_count = tweets[i]["user"]["followers_count"]
        followers += follower_count
    average = followers / len(tweets)
    return average

def _print_average_followers(average):
    """Function to print the average number of followers of posters"""
    print(f"The average number of followers per user is roughly {int(average)} followers.")


tweets = json_to_list("data.json")

# Average length of tweets in characters
average_length = calculate_average_tweet(tweets)
result1 = _print_average_characters(average_length)

# Longest word in a single tweet
longest_word = longest_word_tweet(tweets[6]["text"])
result2 = _print_longest_word(longest_word)

# The average number of followers that users have
average_followers = follower_average(tweets)
_print_average_characters(average_followers)

# Write results to file
results = {"average_length_cars": average_length, "longest_word": longest_word, "average_followers": average_followers}
with open("results_twitter_analysis.txt", "w") as f:
    json.dump(results,f)