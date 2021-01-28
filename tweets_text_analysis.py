import os
import sqlalchemy
from tweets_text_functions import *
from tweets_users_functions import write_results_to_file

# Here the actual text from the tweets is analyzed

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

line1 = f"The following stats were obtained by analyzing {len(result_set_tweets)} tweets from {len(result_set_users)} users.\n"
print(line1)


line2 = "Text-related stats:"
print(line2)
# The average length of tweets (counting words).
average_length_word = int(average_length_word(result_set_tweets))
line3 = f"The average number of words (not counting mentions, hashtags, and URLs) per tweet is {average_length_word}."
print(line3)

# The average length of tweets (counting characters).
average_length_char = int(average_length_char(result_set_tweets))
line4 = f"The average number of characters (counting everything) per tweet is {average_length_char}."
print(line4)


print("\n")
# Percentages
# The percentage of tweets that have a hashtag (#).
tweets_with_hashtag = tweets_with(result_set_tweets, "#")
line5 = f"The percentage of tweets with hashtags is {tweets_with_hashtag}%."
print(line5)
#
# The percentage of tweets that have a mention (@).
tweets_with_mention = tweets_with(result_set_tweets, "@")
line6 = f"The percentage of tweets with a mention (@) is {tweets_with_mention}%."
print(line6)

# Percentage of tweets that use punctuation.
tweets_with_punctuation = percentage_tweet_punctuation(result_set_tweets)
line7 = f"The percentage of tweets containing punctuation is {tweets_with_punctuation}%."
print(line7)


print("\n")
# The longest word
longest_word_with_tweet = find_longest_word_tweet(result_set_tweets)
line8 = f"The longest word in this set of tweets is: {longest_word_with_tweet[0]} and was found in the following tweet:\n\t{longest_word_with_tweet[1]}."
print(line8)


print("\n")
# Corpus analysis
words_corpus = create_corpus_with_occurrences_words(result_set_tweets)
# The x most common words. X can be changed, 10 by default
most_common_words = find_most_frequent_occurrences_words(words_corpus, 15)
line9 = f"The {most_common_words[1]} most common words are:\n" + "\n".join(most_common_words[0]) + "."
print(line9)


symbols_corpus = create_corpus_with_occurrences_characters(result_set_tweets)
# Most frequent symbols. X can be changed, 10 by default
most_common_symbols = find_most_frequent_occurrences_symbols(symbols_corpus, 15)
line10 = f"\nThe {most_common_symbols[1]} most common symbols are:\n" + "\n".join(most_common_symbols[0]) + "."
print(line10)

print("\n")
# Keywords
# Number of tweets containing a specific keywords (not case sensitive)
tweets_with_keyword = find_num_tweets_containing_keyword(result_set_tweets, "CyBeRpUnK")
line11 = f"There are a total of {tweets_with_keyword[0]} tweets containing the word \"{tweets_with_keyword[1].lower()}\"."
print(line11)


file = "results_text_analysis.txt"
lines = [line1, line2, line3, line4, "\n", line5, line6, line7, "\n", line8, "\n", line9, line10, "\n", line11]
write_results_to_file(file, lines)