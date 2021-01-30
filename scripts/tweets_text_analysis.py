import sqlalchemy
from scripts.tweets_text_functions import *
from scripts.tweets_users_functions import write_results_to_file
from database_queries import *

# In this script, the text of the tweets is analyzed

line1 = f"The following stats were obtained by analyzing {len(result_set_tweets):,} tweets from {len(result_set_unique_users):,} users. " \
        f"These users were selected from a total of {len(result_set_users):,} user.\n"
print(line1)

# Two corpora necessary for the analysis
words_corpus = create_corpus_with_occurrences_words(result_set_tweets)
symbols_corpus = create_corpus_with_occurrences_characters(result_set_tweets)

# Updating the two databases with the freshest data
update_words_occurrences_table(result_set_corpus_words_occurrences, words_corpus, table_corpus_words_occurrences)
update_symbols_occurrences_table(result_set_corpus_symbols_occurrences, symbols_corpus, table_corpus_symbols_occurrences)

# Corpus statistis
print("\n")
line2 = f"In the tweets, there are {len(words_corpus):,} different words for a total of {sum(words_corpus.values()):,} occurrences."
print(line2)

line3 = f"There are also {len(symbols_corpus):,} different symbols for a total of {sum(symbols_corpus.values()):,} occurrences."
print(line3)


print("\n")
line5 = "Text-related stats:"
print(line5)

# Keywords
# Number of tweets containing a specific keywords (not case sensitive)
tweets_with_keyword = find_num_tweets_containing_keyword(result_set_tweets, "CyBeRpUnK")
percentage_tweets_with_keyword = (tweets_with_keyword[0] * 100) / len(result_set_tweets)
line6 = f"There are a total of {tweets_with_keyword[0]:,} tweets containing the word \"{tweets_with_keyword[1].lower()}\", " \
         f"the keyword used to filter users. This makes {round(percentage_tweets_with_keyword, 2)}% of the total tweets."
print(line6)

print("\n")
# The average length of tweets (counting words).
average_length_word = int(average_length_word(result_set_tweets))
line7 = f"The average number of words (not counting mentions, hashtags, and URLs) per tweet is {average_length_word}."
print(line7)

# The average length of tweets (counting characters).
average_length_char = int(average_length_char(result_set_tweets))
line8 = f"The average number of characters (counting everything) per tweet is {average_length_char}."
print(line8)


print("\n")
# Percentages
# The percentage of tweets that have a hashtag (#).
tweets_with_hashtag = tweets_with(result_set_tweets, "#")
line9 = f"The percentage of tweets with hashtags is {tweets_with_hashtag}%."
print(line9)
#
# The percentage of tweets that have a mention (@).
tweets_with_mention = tweets_with(result_set_tweets, "@")
line10 = f"The percentage of tweets with a mention (@) is {tweets_with_mention}%."
print(line10)

# Percentage of tweets that use punctuation.
tweets_with_punctuation = percentage_tweet_punctuation(result_set_tweets)
line11 = f"The percentage of tweets containing punctuation is {tweets_with_punctuation}%."
print(line11)


print("\n")
# The longest word
longest_word_with_tweet = find_longest_word_tweet(result_set_tweets)
line12 = f"The longest word in this set of tweets is: {longest_word_with_tweet[0]}.\nIt was found in the following tweet:\n\t{longest_word_with_tweet[1]}."
print(line12)


print("\n")
# The x most common words. X can be changed, 10 by default
most_common_words = find_most_frequent_occurrences_words(words_corpus, 15)
line13 = f"The {most_common_words[1]} most common words are:\n" + "\n".join(most_common_words[0]) + "."
print(line13)


# Most frequent symbols. X can be changed, 10 by default
most_common_symbols = find_most_frequent_occurrences_symbols(symbols_corpus, 15)
line14 = f"\nThe {most_common_symbols[1]} most common symbols are:\n" + "\n".join(most_common_symbols[0]) + "."
print(line14)


file = "../results_text_analysis.txt"
lines = [line1, "\n", line2, line3, "\n", line5, line6, "\n", line7,  line8, "\n", line9, line10, line11, "\n", line12, "\n", line13, line14]
write_results_to_file(file, lines)