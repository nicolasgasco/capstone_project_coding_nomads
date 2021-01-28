import os
import tweepy
import sqlalchemy

# In this file, user_id are fetched filtering the newest tweets written in English and containing the word "cyberpunk"
# The keyword will give the dataset a faint direction towards the world of gaming

# Fetch the secrets and keys/tokens from virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']


# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


# Query with parameters, search for 500 users at a time
limit_search = 500
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3)
tweets = tweepy.Cursor(api.search,
q="cyberpunk",
lang="en",
).items(limit_search)


# Password stored in another file for safety
file = r"C:\Users\nicol\Dropbox\Coding\password_SQL.txt"
with open(file) as f:
    password = f.read()
    password = password.replace("\"", "").strip()

# Connecting to database used for project
engine = sqlalchemy.create_engine(f"mysql+pymysql://root:{password}@localhost/tweetsdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()


# Store the users in a first table called 'users'
table_users = sqlalchemy.Table("users", metadata, autoload=True, autoload_with=engine)



# No infinite loop needed for this query. Only a relatively small number of users is required
# Counting error to stop if there are too many, e.g. when there are no fresh users to fetch
err_count = 0

# Counting total tweets and those which meet criteria
number_tweets_total = 1
number_tweets_successful = 1

# for every tweet found in the query
for tweet in tweets:

    # We only care about users and user stats, no text
    # Dictionary matching db table pattern
    data_for_users = {
        "user_id": tweet.user.id,
        "followers_count": tweet.user.followers_count,
        "friends_count": tweet.user.friends_count,
        "screen_name": tweet.user.screen_name,
        "statuses_count": tweet.user.statuses_count,
    }

    # Insert in db table
    query_users = sqlalchemy.insert(table_users)

    # This is to avoid error caused by duplicates, only unique users wanted
    try:
        result_proxy = connection.execute(query_users, data_for_users)
        print(f"Entry number {number_tweets_successful} of {number_tweets_total} done.")

        number_tweets_successful += 1
        number_tweets_total += 1

        # This is to make the errors consecutive and not total
        err_count -= 1

    except Exception as e:
        print(f"Number {number_tweets_total} was skipped ({e}).")
        number_tweets_total += 1

        # Break after 100 errors
        if err_count >= 100:
            break
        err_count += 1
        continue

# Either ends on its own or because of an error
if err_count < 100:
    print("\nThe search is complete.")
else:
    # This is mostly triggered when you only get duplicates as results as fresh tweets weren't published yet
    print("\nThe script was interrupted. Too many errors.")