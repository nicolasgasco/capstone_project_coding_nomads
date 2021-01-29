import sqlalchemy

# This file contains the vast majority of database queries needed for the project to run

# SQL password stored on separate file for safety
file = r"C:\Users\nicol\Dropbox\Coding\password_SQL.txt"
with open(file) as f:
    password = f.read()
    password = password.replace("\"", "").strip()

# Initializing connection
engine = sqlalchemy.create_engine(f"mysql+pymysql://root:{password}@localhost/tweetsdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()


def select_all_from_db(table_name):
    """Function to fetch all results from a db table"""
    table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([table])
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()

    return result_set


def select_distinct_userid_from_db(table_name):
    """Function to fetch all unique results from the user_id column of a db table"""
    table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([table.columns.user_id]).distinct()
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()

    return result_set

def select_two_columns_from_db(table_name):
    """Function to fetch all unique results from the user_id column of a db table"""
    table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([table.columns.tweet_id, table.columns.created_at])
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()

    return result_set



# I need these tables to be explicitly declared for other scripts in the project
# Table with all the words contained in tweets + the times the occur
table_corpus_words_occurrences = sqlalchemy.Table("corpus_words_occurrences", metadata, autoload=True, autoload_with=engine)
# Table with all the symbols contained in tweets + the times the occur
table_corpus_symbols_occurrences = sqlalchemy.Table("corpus_symbols_occurrences", metadata, autoload=True, autoload_with=engine)
# Table with all the tweet data
table_tweets = sqlalchemy.Table("tweets", metadata, autoload=True, autoload_with=engine)
# Table with all their user data
table_users = sqlalchemy.Table("users", metadata, autoload=True, autoload_with=engine)
# Table containing a list of users to skip when fetching new users
table_users_to_skip = sqlalchemy.Table("users_to_skip", metadata, autoload=True, autoload_with=engine)


# Complete queries called using functions defined above
# Table with all the words contained in tweets + the times the occur
result_set_corpus_words_occurrences = select_all_from_db("corpus_words_occurrences")
# Table with all the symbols contained in tweets + the times the occur
result_set_corpus_symbols_occurrences = select_all_from_db("corpus_symbols_occurrences")
# Table with all the tweet data
result_set_tweets = select_all_from_db("tweets")
# Table with all their user data
result_set_users = select_all_from_db("users")
# Table containing a list of users to skip when fetching new users
result_set_users_to_skip = select_all_from_db("users_to_skip")
# Special filter of the tweets table: unique user_id (= effective number of profiles used)
result_set_unique_users = select_distinct_userid_from_db("tweets")

result_set_tweets_with_time = select_two_columns_from_db("tweets")








