import os
import tweepy
import sqlalchemy
import time

# In this file, user_id in db are used to fetch last 20 tweets (English and no RT)

# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']


# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


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
query = sqlalchemy.select([table_users.columns.user_id])
result_proxy = connection.execute(query)

result_set = result_proxy.fetchall()

# File containing user_id which were already searched
# Script can be run several times without duplicating results or wasting time on already researched users
file_for_already_searched_users = ".users_searched_already.txt"


# Make a list out of IDs in the file
with open(file_for_already_searched_users) as file:
    list_already_searched_users = file.readlines()

general_crashes = 0
user_number = len(list_already_searched_users)

print(f"{user_number} users were already inserted into the database.")

loop = True
print("The search has begun.")
while loop:
    user_number += 1
    # Keep track of users searched
    # user is a tuple, only index 0 is relevant
    for user in result_set:
        # If user was searched already
        if f"{user[0]}\n" in list_already_searched_users:
            # This is to break the loop if no users are available. 20000 is an arbitrary value just to be safe
            if user_number > len(list_already_searched_users)+20000:
                print("Please fetch more users.")
                loop = False
                break
            else:
                print(f"User {user_number} was skipped.")
                user_number += 1
                continue


        # Connection created only for new IDs
        else:

            # This is to avoid error triggered by users with protected tweets
            try:
                # create the connection waiting if max limit is reached
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, timeout=3, retry_count=3)
                tweets = api.user_timeline(user[0])

            except Exception as e:
                print(f"User {user_number} was skipped ({e}).")
                # Write in file so that it can be skipped in the future
                with open(file_for_already_searched_users, "a") as file:
                    file.write(f"{user[0]}\n")
                user_number += 1
                continue


            print(f"User number {user_number} ({user[0]}).")

            # This is to avoid error like max limit reach
            # try:
            # Keeping track of all tweets and those successfully added to database
            number_tweets_total = 1
            number_tweets_successful = 1

            for tweet in tweets:
                # Status needed to access status info (one layer beyond tweet)
                status = api.get_status(tweet.id, tweet_mode="extended")
                data_for_tweets = {
                    "user_id": tweet.user.id,
                    "tweet_id": tweet.id,
                    "created_at": tweet.created_at,
                    "full_text": status.full_text,
                    "screen_name": tweet.user.screen_name,
                }

                # Insert in table tweets
                query_tweets = sqlalchemy.insert(table_tweets)

                # We don't want retweets nor tweets in languages other than English
                if data_for_tweets["full_text"][:2] != "RT" and status.lang == "en":

                    # This is to avoid error caused by duplicates, only unique users wanted
                    try:

                        result_proxy = connection.execute(query_tweets, data_for_tweets)
                        print(f"User number {user_number} ({user[0]}). Tweet {number_tweets_successful} of {number_tweets_total} done.")

                        user_number += 1
                        number_tweets_successful += 1
                        number_tweets_total += 1

                    # Exception mostly raised for duplicates
                    except Exception as e:
                        print(f"User number {user_number}. Tweet {number_tweets_total} was skipped (duplicate).")
                        number_tweets_total += 1
                        continue

                # Tweets which are RTs, in language other than English or both
                else:
                    print(f"User number {user_number}. Tweet {number_tweets_total} was skipped (RT or language other than English).")
                    number_tweets_total += 1

            # Placed here so that if not all 20 tweets from a user were fetched, user isn't counted
            with open(file_for_already_searched_users, "a") as file:
                file.write(f"{user[0]}\n")



            # # This is mostly for limit reached, it's basically impossible the the script runs till the end
            # except Exception as e:
            #     print(f"The script ended because of an error ({e}). Please, try again.")
            #     if general_crashes >= 3:
            #         loop = False
            #     general_crashes += 1
            #
            #

