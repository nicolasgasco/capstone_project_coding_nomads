import os
import sqlalchemy
from tweets_time_functions import *
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


print("Time-related stats:")
time_objects_list = create_list_times(result_set_tweets)

# Oldest tweet
oldest_tweet = time_objects_list[0]
newest_tweet = time_objects_list[-1]
print(f"The oldest tweet in this set was written on {oldest_tweet[0].strftime('%d/%m/%Y at %H:%M:%S')}, while the newest on {newest_tweet[0].strftime('%d/%m/%Y at %H:%M:%S')}.")

# # The x hours with the greatest number of tweets. Default value is x=3, but it can be changed.
most_popular_times = find_most_popular_times(time_objects_list, 5)
most_popular_times_formatted = f"{', '.join(most_popular_times[0][:-1])}, and {most_popular_times[0][-1]}"
print(f"The {most_popular_times[1]} most popular hours for writing tweets are {most_popular_times_formatted}.")
