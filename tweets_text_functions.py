import os
import re
from random import randint
import time


def average_length_word(dataset):
    """Function to determine the average length of tweet in words"""
    # This is enough for a quantitive search
    pattern_word = re.compile(r"\b(?!http|\/\/|t\.co|co\/)\b\w+")
    pattern_all_rest = re.compile(r"@|#|http")
    sum_averages = 0
    # For every tweet
    for data in dataset:
        total_words = 0
        text = data[4]
        for match in re.finditer(pattern_word, text):
            total_words += 1
        for match in re.finditer(pattern_all_rest, text):
            total_words -= 1
        sum_averages += total_words
    average = sum_averages / len(dataset)
    return average


def average_length_char(dataset):
    """Function to determine the average length of tweet in characters"""
    total_chars = 0
    for data in dataset:
        text = data[4]
        total_chars += len(text)
    average = total_chars / len(dataset)
    return average


def tweets_with(dataset, symbol):
    """Function to determine the percentage of tweeet containing a specific symbol"""
    tweets_with_symbol = 0
    for data in dataset:
        if symbol in data[4]:
            tweets_with_symbol += 1

    percentage = (tweets_with_symbol * 100) / len(dataset)
    return int(percentage)


def percentage_tweet_punctuation(dataset):
    """Function to determine the percentage of tweets with punctuation"""
    pattern = re.compile(r"[!?.,;:_'\"\/\|\[\]{}()<>]")
    tweets_with_punctuation = 0

    for data in dataset:
        text = data[4]
        r = re.search(pattern, text)
        if r:
            tweets_with_punctuation += 1
    percentage = (tweets_with_punctuation * 100) / len(dataset)
    return round(percentage, 2)


def find_longest_word_tweet(dataset):
    """Function to find the five longest words in this dataset(hashtags and mentions excluded)"""
    longest_word = ""
    original_tweet = ""
    for data in dataset:
        word_list = _words_without_hash_mentions(data)
        for word in word_list:
            if len(word) > len(longest_word):
                longest_word = word
                original_tweet = data[4]

    return longest_word, original_tweet


def _words_without_hash_mentions(tweet):
    """Function to get list of words in tweet without hashtags and mentions"""
    pattern = re.compile(r"\b\w+\b")
    pattern2 = re.compile(r"[#|@]\w+")
    pattern3 = re.compile(r"https?:\/\/[-a-zA-Z0-9@:%._\+~#=]*\/?\w*")
    pattern4 = re.compile(r"\b\d+\b")
    word_list = []
    text = tweet[4]
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


def create_corpus_with_occurrences_words(dataset):
    """Function to create a dictionary of all the words and their occurrences"""
    count = {}

    for data in dataset:
        word_list = _words_without_hash_mentions(data)
        for word in word_list:
            # Special case that I don't how else to filter out
            if word != "s":
                count.setdefault(word, 0)
                count[word] += 1

    return count

def create_corpus_with_occurrences_characters(dataset):
    """Function to create a dictionary of all the characters and their occurrences"""
    count = {}

    for data in dataset:
        for character in data[4]:
            count.setdefault(character, 0)
            count[character] += 1

    return count

def find_most_frequent_occurrences_words(corpus, limit=10):
    """Function to find the highest occurrences of the previously made corpus"""
    list_words_occurrences = list(corpus.items())
    list_words_occurrences.sort(key=lambda x:x[1], reverse = True)
    highest_occurrences = list_words_occurrences[:limit]

    highest_occurrences_formatted = [f"\t{occurrence[0]} ({occurrence[1]})" for occurrence in highest_occurrences]

    return highest_occurrences_formatted, limit


def find_most_frequent_occurrences_symbols(corpus, limit=10):
    """Function to find the highest occurrences of the previously made corpus"""
    pattern = re.compile(r"[^a-zA-Z0-9|\s|ㅤ|️]")
    list_symbols_occurrences = [(value, key) for key, value in corpus.items() if re.fullmatch(pattern, key)]
    list_symbols_occurrences.sort(reverse=True)

    highest_occurrences = list_symbols_occurrences[:limit]

    highest_occurrences_formatted = [f"\t{occurrence[1]} ({occurrence[0]})" for occurrence in highest_occurrences]

    return highest_occurrences_formatted, limit


def find_num_tweets_containing_keyword(dataset, keyword):
    """Function that returns the number of tweets containing the given keyword"""
    word_count = 0
    for data in dataset:
        word_list = _words_without_hash_mentions(data)
        for word in word_list:
            if word.lower() == keyword.lower():
                word_count += 1

    return word_count, keyword


def create_list_times(dataset):
    """Function that returns a list of time objects and relative tweet ID"""
    time_objects = []
    for data in dataset:
        time = data[3]
        tweet_id = data[0]

        time_objects.append((time, tweet_id))
        time_objects.sort()

    return time_objects

def dict_occurrences_hours(time_objects):
    """Function returns the occurrence of every time object (only hour, not date)"""

    all_hours = [time[0].strftime("%H") for time in time_objects]
    hours_occurrences = {}

    for hour in all_hours:
        hours_occurrences.setdefault(hour, 0)
        hours_occurrences[hour] += 1

    return hours_occurrences


def find_most_popular_times(time_objects, limit=3):
    """Returns limit number of most popular hours"""
    hours_dict = dict_occurrences_hours(time_objects)
    hours_list = [(value, key) for key, value in hours_dict.items()]
    hours_list.sort()
    most_popular_hours = hours_list[-limit:]

    result = [f"{hour[1]} ({hour[0]})" for hour in most_popular_hours]

    return result, limit
