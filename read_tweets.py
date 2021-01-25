import os
import tweepy
import sqlalchemy
import datetime

# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']


# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

start_date = datetime.date(2020, 12, 10)


# create the connection
limit_search = 950
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search,
q="cyberpunk",
lang="en",
).items(limit_search)

# Password stored in another file
file = r"C:\Users\nicol\Dropbox\Coding\password_SQL.txt"
with open(file) as f:
    password = f.read()
    password = password.replace("\"", "").strip()


# Connecting to database
engine = sqlalchemy.create_engine(f"mysql+pymysql://root:{password}@localhost/tweetsdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()


# For every tweet write the user_name and other stats in database "users"
table_users = sqlalchemy.Table("users", metadata, autoload=True, autoload_with=engine)
table_tweets = sqlalchemy.Table("tweets", metadata, autoload=True, autoload_with=engine)


# This is to avoid error like max limit reach
try:
    i_total = 1
    i_actual = 1
    for tweet in tweets:

        status = api.get_status(tweet.id, tweet_mode="extended")
        data_for_users = {
            "user_id": tweet.user.id,
            "followers_count": tweet.user.followers_count,
            "friends_count": tweet.user.friends_count,
            "screen_name": tweet.user.screen_name,
            "statuses_count": tweet.user.statuses_count,
        }

        data_for_tweets = {
            "user_id": tweet.user.id,
            "tweet_id": tweet.id,
            "created_at": tweet.created_at,
            "full_text": status.full_text,
            "screen_name": tweet.user.screen_name,
        }

        query_tweets = sqlalchemy.insert(table_tweets)
        query_users = sqlalchemy.insert(table_users)

        # This is to avoid error caused by duplicates, unique users
        if data_for_tweets["full_text"][:2] != "RT":
            try:
                result_proxy = connection.execute(query_tweets, data_for_tweets)
                result_proxy = connection.execute(query_users, data_for_users)
                print(f"Entry number {i_actual} of {i_total} done.")
                i_actual += 1
            except Exception as e:
                print(f"Number {i_total} was skipped ({e}).")
                continue
        else:
            print(f"Number {i_total} is an RT and was skipped.")
        i_total += 1

except Exception as e:
    print(f"The script ended because of an error ({e}). Please, try again.")