import os
import tweepy
import sqlalchemy
import time
from database_queries import *
from twitter_authentication import *


# For every user fetched in get_user.py, the last 20 tweets are retrieved (only if written in English and if not an RT)

# This is done to make the whole script more understandable
list_already_searched_users = [user_id[0] for user_id in result_set_users_to_skip]

# Start counting users from those already fetched
user_number = len(list_already_searched_users)
print(f"{user_number} users were already inserted into the database.")

# Required because sometimes the script works with no input for longer times
print("The search has begun.")

# Infinite loop to be able to farm tweets indefinitely
error_count = 0
loop = True
while loop:
    # One user more than those already searched, triggered only once
    user_number += 1

    # user is a tuple, only index 0 is relevant
    for user in result_set_users:

        # If user was searched already
        if user[0] in list_already_searched_users:
            error_count += 1

            # This is to break the loop if no users are available (but count keeps going on).
            # 20000 is an arbitrary value just to be safe, it's big enough and it takes a couple of seconds to get there
            if error_count > len(list_already_searched_users) + 20000:
                print("Please fetch more users.")
                loop = False
                break


            else:
                # print(f"User {user_number} ({user[0]}) was skipped.")
                continue


        # Connection created only for new IDs
        else:

            # This is to avoid error triggered by users with protected tweets
            try:
                # create the connection waiting if max limit is reached
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                tweets = api.user_timeline(user[0])

            except Exception as e:
                # print(f"User {user_number} was skipped ({e}).")

                # Write in file so that it can be skipped in the future
                user_to_add = user[0]
                query_users_to_skip = sqlalchemy.insert(table_users_to_fix).values(user_id=user_to_add)
                result_proxy = connection.execute(query_users_to_skip)


            # Keeping track of all tweets and those successfully added to database
            number_tweets_total = 1
            number_tweets_successful = 1

            # Analysis of last 20 tweets
            for tweet in tweets:
                # Status needed to access status info (one layer beyond tweet)
                status = api.get_status(tweet.id, tweet_mode="extended")
                # Pattern matching the 'tweets' table in the db
                data_for_tweets = {
                    "user_id": tweet.user.id,
                    "tweet_id": tweet.id,
                    "created_at": tweet.created_at,
                    "full_text": status.full_text,
                    "screen_name": tweet.user.screen_name,
                }

                # Insert in 'tweets' table
                query_tweets = sqlalchemy.insert(table_tweets)

                # We don't want retweets nor tweets in languages other than English
                if data_for_tweets["full_text"][:2] != "RT" and status.lang == "en":

                    # This is to avoid error caused by duplicates, only unique tweets wanted
                    try:

                        result_proxy_users = connection.execute(query_tweets, data_for_tweets)
                        # print(f"User number {user_number} ({user[0]}). Tweet {number_tweets_successful} of {number_tweets_total} done.")

                        number_tweets_successful += 1
                        number_tweets_total += 1

                    # Exception mostly raised for duplicates
                    except Exception as e:
                        # print(f"User number {user_number}. Tweet {number_tweets_total} was skipped (duplicate).")
                        number_tweets_total += 1
                        continue

                # Tweets which are RTs, in language other than English or both
                else:
                    # print(f"User number {user_number}. Tweet {number_tweets_total} was skipped (RT or language other than English).")
                    number_tweets_total += 1

            # Placed here so that if not all tweets from a user were fetched, user isn't counted
            user_to_add = user[0]
            query_users_to_skip = sqlalchemy.insert(table_users_to_fix).values(user_id=user_to_add)
            result_proxy = connection.execute(query_users_to_skip)

            print(f"User number {user_number} ({user[0]}).")
            user_number += 1


