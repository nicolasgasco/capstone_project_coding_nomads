import os
import sqlalchemy
from tweets_text_functions import *
import re
from pprint import pprint

# This is where the actual data analysis will take place, using the data in the database

# Password stored in another file for security
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


print(f"The following stats were obtained by analyzing {len(result_set_tweets)} tweets from {len(result_set_users)} users.\n")


print("Text-related stats:")
# The average length of tweets (counting words).
average_length_word = int(average_length_word(result_set_tweets))
print(f"The average number of words per tweet is {average_length_word}.")

# The average length of tweets (counting characters).
average_length_char = int(average_length_char(result_set_tweets))
print(f"The average number of characters per tweet is {average_length_char}.")

# The percentage of tweets that have a hashtag (#).
tweets_with_hashtag = tweets_with(result_set_tweets, "#")
print(f"The percentage of tweets with hashtags is {tweets_with_hashtag}%.")
#
# The percentage of tweets that have a mention (@).
tweets_with_mention = tweets_with(result_set_tweets, "@")
print(f"The percentage of tweets with a mention (@) is {tweets_with_mention}%.")

# Percentage of tweets that use punctuation.
tweets_with_punctuation = percentage_tweet_punctuation(result_set_tweets)
print(f"The percentage of tweets containing punctuation is {tweets_with_punctuation}%.")

print("\n")
# The longest word
longest_word_with_tweet = find_longest_word_tweet(result_set_tweets)
print(f"The longest word in this set of tweets is: {longest_word_with_tweet[0]} and was found in the following tweet:\n\t{longest_word_with_tweet[1]}.")

words_corpus = create_corpus_with_occurrences_words(result_set_tweets)

# The x most common words. X can be changed, 10 by default
print("\n")
most_common_words = find_most_frequent_occurrences_words(words_corpus)
print(f"The {most_common_words[1]} most common words are:\n", "\n".join(most_common_words[0]) + ".")


symbols_corpus = create_corpus_with_occurrences_characters(result_set_tweets)
# Most frequent symbols. X can be changed, 10 by default
most_common_symbols = find_most_frequent_occurrences_symbols(symbols_corpus, 10)
print(f"\nThe {most_common_symbols[1]} most common symbols are:\n", "\n".join(most_common_symbols[0]) + ".")

# Number of tweets containing a specific keywords (not case sensitive)
tweets_with_keyword = find_num_tweets_containing_keyword(result_set_tweets, "CyBeRpUnK")
print(f"\nThere are a total of {tweets_with_keyword[0]} tweets containing the word \"{tweets_with_keyword[1].lower()}\".")

