import os
import re
import sqlalchemy
from database_queries import *

def update_words_occurrences_table(result_set_to_update, corpus_to_insert, table):
    """Function to update a dictionary starting from a result set from a db and a dictionary.
    DB must be update with values in the dictionary"""
    corpus = corpus_to_insert

    dictionary_to_update = {}
    for result in result_set_to_update:
        dictionary_to_update[result[0]] = result[1]

    for word, occurrence in corpus.items():
        if word not in dictionary_to_update.keys():
            data = {"word": word, "occurrences": occurrence}
            query_insert = sqlalchemy.insert(table)
            try:
                result_proxy = connection.execute(query_insert, data)
            except:
                continue

        else:
            if occurrence != dictionary_to_update.get(word):
                query_update = sqlalchemy.update(table).where(table.c.word == word).values(occurrences=occurrence)
                result_proxy = connection.execute(query_update)

    print("Update was completed.")


def update_symbols_occurrences_table(result_set_to_update, corpus_to_insert, table):
    """Function to update a dictionary starting from a result set from a db and a dictionary.
    DB must be update with values in the dictionary"""
    corpus = corpus_to_insert

    dictionary_to_update = {}
    for result in result_set_to_update:
        dictionary_to_update[result[0]] = result[1]

    for char, occurrence in corpus.items():
        if char not in dictionary_to_update.keys():
            data = {"symbol": char, "occurrences": occurrence}
            query_insert = sqlalchemy.insert(table)
            try:
                result_proxy = connection.execute(query_insert, data)
            except:
                continue

        else:
            if occurrence != dictionary_to_update.get(char):
                query_update = sqlalchemy.update(table).where(table.c.symbol == char).values(occurrences=occurrence)
                result_proxy = connection.execute(query_update)

    print("Update was completed.")

def average_length_word(dataset):
    """Function to calculate the average length of tweet in words"""

    # This is enough for a quantitive search
    pattern_word = re.compile(r"\b(?!http|\/\/|t\.co|co\/)\b\w+")
    pattern_all_rest = re.compile(r"@|#|http")

    sum_averages = 0

    for data in dataset:
        total_words = 0
        text = data[4]

        for match in re.finditer(pattern_word, text):
            total_words += 1

        # Don't count links, mentions, and hashtags as words
        for match in re.finditer(pattern_all_rest, text):
            total_words -= 1

        sum_averages += total_words

    average = sum_averages / len(dataset)

    return average


def average_length_char(dataset):
    """Function to calculate the average length of tweet in characters"""

    total_chars = 0

    for data in dataset:
        text = data[4]
        total_chars += len(text)

    average = total_chars / len(dataset)

    return average


def tweets_with(dataset, symbol):
    """Function to calculate the percentage of tweet containing a specific symbol"""

    tweets_with_symbol = 0

    for data in dataset:
        if symbol in data[4]:
            tweets_with_symbol += 1

    percentage = (tweets_with_symbol * 100) / len(dataset)

    return int(percentage)


def percentage_tweet_punctuation(dataset):
    """Function to calculate the percentage of tweets with punctuation"""

    pattern = re.compile(r"[!?.,;:_'\"\/\|\[\]{}()<>]")

    tweets_with_punctuation = 0

    for data in dataset:
        text = data[4]
        r = re.search(pattern, text)
        if r:
            tweets_with_punctuation += 1

    percentage = (tweets_with_punctuation * 100) / len(dataset)

    return round(percentage, 2)


def _words_without_hash_mentions(tweet):
    """Function to get list of words in tweet without hashtags and mentions"""

    # Regular words
    pattern = re.compile(r"\b\w+\b")
    # Words starting with @
    pattern2 = re.compile(r"[#|@]\w+")
    # URLs
    pattern3 = re.compile(r"https?:\/\/[-a-zA-Z0-9@:%._\+~#=]*\/?\w*")
    # Digits
    pattern4 = re.compile(r"\b\d+\b")
    # Punctuation
    pattern5 = re.compile(r"[!?.,;:_'\"\/\|\[\]{}()<>ﾟ]\w*")

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
    # Remove all symbols
    for match in re.finditer(pattern5, text):
        text = text.replace(match.group(), "")

    for match in re.finditer(pattern, text):
        # Attach all words except retweets
        if match.group() != "RT":
            word_list.append(match.group())
    return word_list


def find_longest_word_tweet(dataset):
    """Function to find the longest word in this dataset (hashtags and mentions excluded)"""

    longest_word = ""
    original_tweet = ""

    for data in dataset:
        word_list = _words_without_hash_mentions(data)

        # Only pure words, no hashtags or mentions
        for word in word_list:
            if len(word) > len(longest_word):
                longest_word = word
                original_tweet = data[4]

    return longest_word, original_tweet


def create_corpus_with_occurrences_words(dataset):
    """Function to create a dictionary of all the words and their occurrences"""
    count = {}

    for data in dataset:
        word_list = _words_without_hash_mentions(data)
        for word in word_list:
            word = word.lower()
            # Special cases that I don't how else to filter out
            if word != "s" and word != "t":
                count.setdefault(word, 0)
                count[word] += 1

    return count

def create_corpus_with_occurrences_characters(dataset):
    """Function to create a dictionary of all the characters and their occurrences"""
    pattern = re.compile(r"[^a-zA-Z0-9|\s|ㅤ|️]")
    count = {}

    for data in dataset:
        for character in data[4]:
            if re.fullmatch(pattern, character):
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


