import sqlalchemy

file = r"C:\Users\nicol\Dropbox\Coding\password_SQL.txt"
with open(file) as f:
    password = f.read()
    password = password.replace("\"", "").strip()

# Connecting to database
engine = sqlalchemy.create_engine(f"mysql+pymysql://root:{password}@localhost/tweetsdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()


# Tables
table_corpus_words_occurrences = sqlalchemy.Table("corpus_words_occurrences", metadata, autoload=True, autoload_with=engine)
table_tweets = sqlalchemy.Table("tweets", metadata, autoload=True, autoload_with=engine)
table_users = sqlalchemy.Table("users", metadata, autoload=True, autoload_with=engine)
table_users_to_fix = sqlalchemy.Table("users_to_skip", metadata, autoload=True, autoload_with=engine)


# Queries
query_tweets = sqlalchemy.select([table_tweets])
query_users = sqlalchemy.select([table_users])
query_user_to_skip = sqlalchemy.select([table_users_to_fix]) # .columns.user_id]
query_corpus_words_occurrences = sqlalchemy.select([table_corpus_words_occurrences])

# Result proxies
result_proxy_corpus_words_occurrences = connection.execute(query_corpus_words_occurrences)
result_proxy_tweets = connection.execute(query_tweets)
result_proxy_users = connection.execute(query_users)
result_proxy_users_to_skip = connection.execute(query_user_to_skip)

# Result sets
result_set_corpus_words_occurrences = result_proxy_corpus_words_occurrences.fetchall()
result_set_tweets = result_proxy_tweets.fetchall()
result_set_users = result_proxy_users.fetchall()
result_set_users_to_skip = result_proxy_users_to_skip.fetchall()

