import os
import tweepy
import sqlalchemy
from database_queries import *
from twitter_authentication import *


# For every user fetched in get_user.py, the last 20 tweets are retrieved (only if written in English and if not an RT)

# This is done to make the whole script more understandable
list_already_searched_users = [user_id[0] for user_id in result_set_users_to_skip]

# Start counting users from those already fetched
users_number = len(result_set_unique_users)
print(f"Tweets from {users_number} users were already inserted into the database. {len(result_set_users)-len(result_set_users_to_skip)} new users remaining before new users must be fetched.")

# Required because sometimes the script works with no input for longer times
print("Please wait while the search begins.")

# Infinite loop to be able to farm tweets indefinitely
loop = True
while loop:
    # One user more than those already searched, triggered only once
    users_number += 1

    # user is a tuple, only index 0 is relevant
    for user in result_set_users:
        user = user[0]

        # If user was
        # searched already
        if user in list_already_searched_users:
            continue


        # Connection created only for new IDs
        else:

            # This is to avoid error triggered by users with protected tweets
            try:

                # create the connection waiting if max limit is reached
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                tweets = api.user_timeline(user)

            except Exception as e:

                # Write in file so that it can be skipped in the future
                user_to_add = user
                query_users_to_skip = sqlalchemy.insert(table_users_to_skip).values(user_id=user_to_add)
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

                        number_tweets_successful += 1
                        number_tweets_total += 1

                    # Exception mostly raised for duplicates
                    except Exception as e:

                        number_tweets_total += 1
                        continue

                # Tweets which are RTs, in language other than English or both
                else:
                    number_tweets_total += 1

            print(f"User number {users_number} ({user}).")

            # Placed here so that if not all tweets from a user were fetched, user isn't counted
            try:

                user_to_add = user
                query_users_to_skip = sqlalchemy.insert(table_users_to_skip).values(user_id=user_to_add)
                result_proxy = connection.execute(query_users_to_skip)

                users_number += 1

            # This is triggered when a duplicate is inserted in the users_to_skip database
            except:
                print("Please fetch more users.")
                loop = False
                break
