import sqlalchemy
from scripts.tweets_text_functions import *
from scripts.tweets_users_functions import write_results_to_file
from database_queries import *


words_corpus = create_corpus_with_occurrences_words(result_set_tweets)
symbols_corpus = create_corpus_with_occurrences_characters(result_set_tweets)



# This line of code update the database with the data fetched from the tweets
update_words_occurrences_table(result_set_corpus_words_occurrences, words_corpus, table_corpus_words_occurrences)

update_symbols_occurrences_table(result_set_corpus_symbols_occurrences, symbols_corpus, table_corpus_symbols_occurrences)

# Here start the text stats
line1 = f"The following stats were obtained by analyzing {len(result_set_tweets)} tweets from {len(result_set_users)} users.\n"
print(line1)


line2 = "Text-related stats:"
print(line2)

# Keywords
# Number of tweets containing a specific keywords (not case sensitive)
tweets_with_keyword = find_num_tweets_containing_keyword(result_set_tweets, "CyBeRpUnK")
percentage_tweets_with_keyword = (tweets_with_keyword[0] * 100) / len(result_set_tweets)
line3 = f"There are a total of {tweets_with_keyword[0]} tweets containing the word \"{tweets_with_keyword[1].lower()}\", " \
         f"the keyword used to filter users. This makes {round(percentage_tweets_with_keyword, 2)}% of the total tweets."
print(line3)

print("\n")
# The average length of tweets (counting words).
average_length_word = int(average_length_word(result_set_tweets))
line4 = f"The average number of words (not counting mentions, hashtags, and URLs) per tweet is {average_length_word}."
print(line4)

# The average length of tweets (counting characters).
average_length_char = int(average_length_char(result_set_tweets))
line5 = f"The average number of characters (counting everything) per tweet is {average_length_char}."
print(line5)


print("\n")
# Percentages
# The percentage of tweets that have a hashtag (#).
tweets_with_hashtag = tweets_with(result_set_tweets, "#")
line6 = f"The percentage of tweets with hashtags is {tweets_with_hashtag}%."
print(line6)
#
# The percentage of tweets that have a mention (@).
tweets_with_mention = tweets_with(result_set_tweets, "@")
line7 = f"The percentage of tweets with a mention (@) is {tweets_with_mention}%."
print(line7)

# Percentage of tweets that use punctuation.
tweets_with_punctuation = percentage_tweet_punctuation(result_set_tweets)
line8 = f"The percentage of tweets containing punctuation is {tweets_with_punctuation}%."
print(line8)


print("\n")
# The longest word
longest_word_with_tweet = find_longest_word_tweet(result_set_tweets)
line9 = f"The longest word in this set of tweets is: {longest_word_with_tweet[0]} and was found in the following tweet:\n\t{longest_word_with_tweet[1]}."
print(line9)


print("\n")

# The x most common words. X can be changed, 10 by default
most_common_words = find_most_frequent_occurrences_words(words_corpus, 15)
line10 = f"The {most_common_words[1]} most common words are:\n" + "\n".join(most_common_words[0]) + "."
print(line10)


# Most frequent symbols. X can be changed, 10 by default
most_common_symbols = find_most_frequent_occurrences_symbols(symbols_corpus, 15)
line11 = f"\nThe {most_common_symbols[1]} most common symbols are:\n" + "\n".join(most_common_symbols[0]) + "."
print(line11)




file = "../results_text_analysis.txt"
lines = [line1, line2, line3, "\n", line4,  line5, "\n", line6, line7, line8, "\n", line9, "\n", line10, line11]
write_results_to_file(file, lines)