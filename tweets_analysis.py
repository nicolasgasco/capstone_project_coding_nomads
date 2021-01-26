import os
import sqlalchemy
from tweets_functions import *
import re
from random import randint

# This is where the actual data analysis will take place, using the data in the database

# Password stored in another file
file = r"C:\Users\nicol\Dropbox\Coding\password_SQL.txt"
with open(file) as f:
    password = f.read()
    password = password.replace("\"", "").strip()


# Connecting to database
engine = sqlalchemy.create_engine(f"mysql+pymysql://root:{password}@localhost/tweetsdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()


# Using both tweets and users tables
table_users = sqlalchemy.Table("users", metadata, autoload=True, autoload_with=engine)
table_tweets = sqlalchemy.Table("tweets", metadata, autoload=True, autoload_with=engine)


# Fetch from user_id column in users table
query_users = sqlalchemy.select([table_users])
# query_users_columns = sqlalchemy.select([table_users.columns()])

query_tweets = sqlalchemy.select([table_tweets])
# query_tweets_columns = sqlalchemy.select([table_tweets.columns])


result_proxy_users = connection.execute(query_users)
# result_proxy_users_columns = connection.execute(query_users_columns)


result_proxy_tweets = connection.execute(query_tweets)
# result_proxy_tweets_columns = connection.execute(query_tweets_columns)


result_set_users = result_proxy_users.fetchall()
# result_set_users_columns = result_proxy_users_columns.fetchall()

result_set_tweets = result_proxy_tweets.fetchall()
# result_set_tweets_columns = result_proxy_tweets_columns.fetchall()

print(result_set_users[0])
print(result_set_tweets[0])


print(f"The following stats were obtained by analyzing {len(result_set_tweets)} tweets from {len(result_set_users)} users.\n")

print("User-related stats:")
# The average number of followers.
average_followers_count = average_followers(result_set_users)
print(f"The average number of followers is {int(average_followers_count)}.")

# The average number of tweets published by users.
average_status_count = average_status_count(result_set_users)
print(f"The average number of statuses is {int(average_status_count)}.")

# What user has the most tweets in the dataset?
highest_status = find_most_statuses(result_set_users)
print(f"The user with the highest status count is {highest_status[1]} with {highest_status[0]} statuses.")

# What user has the most statuses in the dataset?
lowest_status = find_least_statuses(result_set_users)
print(f"The user with the lowest status count is {lowest_status[1]} with {lowest_status[0]} status(es).")

# Highest number of followers
highest_followers = find_highest_followers(result_set_users)
print(f"The user with the highest followers count is {highest_followers[1]} with {highest_followers[0]} followers.")

# Print 5 users without followers
user_without_followers = find_users_without_followers(result_set_users, 3)
limit = user_without_followers[1]
users_list = user_without_followers[0]
users_list_formatted = f"{(', '.join(users_list[:limit-1]))}, and {str(user_without_followers[0][-1])}"
print(f"These are {user_without_followers[1]} (or less) users who don't have any followers at all are {users_list_formatted}.")


print("\n\nText-related stats:")
# The average length of tweets (counting words).
average_length_word = int(average_length_word(result_set_tweets))
print(f"The average number of words per tweet is {average_length_word}.")

# The average length of tweets (counting characters).
average_length_char = int(average_length_char(result_set_tweets))
print(f"The average number of characters per tweet is {average_length_char}.")

# # The percentage of tweets that have a hashtag (#).
# print(f"The percentage of tweets with hashtags is {tweets_with(tweets, limit_search, '#')}%.")
#
# # The percentage of tweets that have a mention (@).
# print(f"The percentage of tweets with a mention (@) is {tweets_with(tweets, limit_search, '@')}%.")
#
# # The 100 most common words.
#
# # The 100 most common symbols.
#
# # Percentage of tweets that use punctuation.
# print(f"The percentage of tweets containing punctuation is {percentage_tweet_punctuation(tweets, limit_search)}%.")
#
# # The longest word in a tweet.
# random_tweet = tweets[randint(0, limit_search -1)]
# longest_word = longest_word_tweet(random_tweet)
# print(f"The longest word of this random tweet is: {longest_word}.")
#
# # Shortest word in a tweet.
# shortest_word = shortest_word_tweet(random_tweet)
# print(f"The shortest word of this random tweet is: {shortest_word}.")
#


# # The hour with the greatest number of tweets.