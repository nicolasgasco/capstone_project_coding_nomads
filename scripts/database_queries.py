import sqlalchemy

file = r"C:\Users\nicol\Dropbox\Coding\password_SQL.txt"
with open(file) as f:
    password = f.read()
    password = password.replace("\"", "").strip()

# Connecting to database
engine = sqlalchemy.create_engine(f"mysql+pymysql://root:{password}@localhost/tweetsdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()


def select_all_from_db(table_name):
    """Function to fetch results from a db"""
    table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([table])
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()

    return result_set


def select_distinct_userid_from_db(table_name):
    """Function to fetch results from a db"""
    table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([table.columns.user_id]).distinct()
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()

    return result_set




# Need these two for another script
table_corpus_words_occurrences = sqlalchemy.Table("corpus_words_occurrences", metadata, autoload=True, autoload_with=engine)
table_corpus_symbols_occurrences = sqlalchemy.Table("corpus_symbols_occurrences", metadata, autoload=True, autoload_with=engine)
table_tweets = sqlalchemy.Table("tweets", metadata, autoload=True, autoload_with=engine)
table_users = sqlalchemy.Table("users", metadata, autoload=True, autoload_with=engine)
table_users_to_skip = sqlalchemy.Table("users_to_skip", metadata, autoload=True, autoload_with=engine)


# Queries
# Counting the unique users who published the tweets fetched
# query_unique_users = sqlalchemy.select([table_tweets.columns.user_id]).distinct()

# Result proxies
# result_proxy_unique_users = connection.execute(query_unique_users)


# Result sets
result_set_corpus_words_occurrences = select_all_from_db("corpus_words_occurrences")
result_set_corpus_symbols_occurrences = select_all_from_db("corpus_symbols_occurrences")
result_set_tweets = select_all_from_db("tweets")
result_set_users = select_all_from_db("users")
result_set_users_to_skip = select_all_from_db("users_to_skip")
result_set_unique_users = select_distinct_userid_from_db("tweets")









