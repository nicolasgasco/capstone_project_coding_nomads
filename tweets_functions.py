import os
import re
from random import randint




def average_followers(dataset):
    """Function to calculate the average number of followers"""
    user_count = len(dataset)
    followers_count = 0
    for data in dataset:
        followers_count += data[3]
    average = followers_count / user_count
    return average


def average_followed(dataset):
    """Function to calculate the average number of friends (followed)"""
    user_count = len(dataset)
    followed_count = 0
    for data in dataset:
        followed_count += data[4]
    average = followed_count / user_count
    return average


def average_status_count(dataset):
    """Function to find the average number of statuses"""
    user_count = len(dataset)
    statuses_count = 0
    for data in dataset:
        statuses_count += data[2]
    average = statuses_count / user_count
    return average


def find_most_statuses(dataset):
    """Functions to find user with most tweets"""
    highest_statuses = 0
    user_name = ""
    for data in dataset:
        if data[2] > highest_statuses:
            highest_statuses = data[2]
            user_name = data[1]
    return highest_statuses, user_name


def find_least_statuses(dataset):
    """Functions to find user with least tweets"""
    least_statuses = dataset[0][2]
    user_name = ""
    for data in dataset:
        if data[2] < least_statuses:
            least_statuses = data[2]
            user_name = data[1]
    return least_statuses, user_name


def find_highest_followers(dataset):
    """Functions to find user with most followers"""
    highest_followers = 0
    user_name = ""
    for data in dataset:
        if data[3] > highest_followers:
            highest_followers = data[3]
            user_name = data[1]
    return highest_followers, user_name


def find_highest_friends(dataset):
    """Functions to find user with most friends"""
    highest_friends = 0
    user_name = ""
    for data in dataset:
        if data[4] > highest_friends:
            highest_friends = data[4]
            user_name = data[1]
    return highest_friends, user_name


def find_users_without_followers(dataset, limit=5):
    """Functions to find users without followers"""
    users_without_followers = []
    for data in dataset:
        if data[3] == 0:
            users_without_followers.append(data[1])

    # If a huge or too small number is passed as an argument
    if limit > 5 or limit <= 2:
        limit = 5

    # If numbers of elements found smaller than limit
    length_list_result = len(users_without_followers)
    if length_list_result < limit:
        limit = length_list_result

    return users_without_followers, limit


def find_users_most_followers(dataset, limit=5):
    """Functions to find users with the biggest number of followers"""
    users_with_followers = []
    for data in dataset:
        user_with_count = (data[3], data[1])
        users_with_followers.append(user_with_count)

    users_with_followers.sort()

    if limit > len(users_with_followers):
        limit = len(users_with_followers)

    users_with_followers = users_with_followers[-limit:]
    result_list = []
    for user in users_with_followers:
        result_list.append(f"{user[1]} ({user[0]})")

    return result_list, limit


def find_smallest_highest_id(dataset):
    """Function to find the smallest and highest ID"""
    smallest_id = [dataset[0][1], int(dataset[0][0])]
    biggest_id = [dataset[0][1], 0]
    for data in dataset:
        if int(data[0]) < smallest_id[1]:
            smallest_id[0] = data[1]
            smallest_id[1] = int(data[0])

        elif int(data[0]) > biggest_id[1]:
            biggest_id[0] = data[1]
            biggest_id[1] = int(data[0])

    return smallest_id, biggest_id

def find_users_without_followers_but_statuses(dataset, limit_followers=50, limit_statuses=500):
    """Functions to find users without followers"""
    users_without_followers = []
    for data in dataset:
        if data[3] <= limit_followers and data[2] >= limit_statuses:
            users_without_followers.append(data[1])

    return len(users_without_followers), limit_statuses, limit_followers


def percentage_user_with_less_x_followers(dataset, limit=100):
    """Function to find the percentage of users with less than x followers"""
    users_with_less = 0
    for data in dataset:
        if data[3] <= limit:
            users_with_less += 1

    percentage = (users_with_less * 100)/len(dataset)
    return percentage, limit


def average_followers_users_no_friends(dataset, limit=5):
    """Function to determine the average of followers of users with less than limit friends"""
    followers_users_no_friends = []
    for data in dataset:
        if data[4] <= limit:
            followers_users_no_friends.append(data[3])

    average = sum(followers_users_no_friends) / len(followers_users_no_friends)
    return average, limit


def average_length_word(dataset):
    """Function to determine the average length of tweet in words"""
    # This is enough for a quantitive search
    pattern = re.compile(r"\w+")
    sum_averages = 0
    # For every tweet
    for data in dataset:
        total_words = 0
        text = data[4]
        for match in re.finditer(pattern, text):
            total_words += 1
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


# This one too is old and not actually need
def find_user_statuses(dataset, statuses):
    """Function to find the username of a certain status count"""
    username = ""
    for data in dataset:
        if data["statuses_count"] == statuses:
            username += data["screen_name"]
    return username


# This is an old function and not actually required anymore
def generate_dict(dataset, number):
    """Function to generate a dictionary of tweets starting from a tweepy object"""
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
