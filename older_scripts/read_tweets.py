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
limit_search = 50
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

tweets_table = sqlalchemy.Table("tweets", metadata, autoload=True, autoload_with=engine)

# For every tweet write in database
try:
    i_total = 50
    i_actual = 1
    for tweet in tweets:
        query = sqlalchemy.insert(tweets_table)
        status = api.get_status(tweet.id, tweet_mode="extended")

        tweet_data = {
            "id": tweet.id,
            "created_at": tweet.created_at,
            "text": tweet.text,
            "followers_count": tweet.user.followers_count,
            "full_text": status.full_text,
            "friends_count": tweet.user.friends_count,
            "screen_name": tweet.user.screen_name,
            "statuses_count": tweet.user.statuses_count,
        }

        # Let's avoid retweets
        if tweet.text[:2] != "RT":
            # This is used mostly to avoid duplicates
            try:
                result_proxy = connection.execute(query, tweet_data)
                i_actual += 1
                print(f"Entry number {i_actual} of {i_total} done.")
            except:
                continue
        i_total += 1

except:
    print("The script ended because of an error. Please, try again.")