import sqlalchemy
from scripts.tweets_time_functions import *
from scripts.tweets_users_functions import write_results_to_file
from database_queries import *

# This is where the actual data analysis will take place, using the data in the database

line1 = f"The following stats were obtained by analyzing {len(result_set_tweets):,} tweets from {len(result_set_unique_users):,} users. " \
        f"These users were selected from a total of {len(result_set_users):,} user.\n"
print(line1)

line2 = "Time-related stats:"
print(line2)

# List used for stats
time_objects_list = create_ordered_list_times(result_set_tweets_with_time)

# Oldest tweet
oldest_tweet = time_objects_list[0]
newest_tweet = time_objects_list[-1]
line3 = f"The oldest tweet in this set was written on {oldest_tweet[0].strftime('%d/%m/%Y at %H:%M:%S')}, " \
        f"while the newest on {newest_tweet[0].strftime('%d/%m/%Y at %H:%M:%S')}."
print(line3)

# Number of tweets per moment of day (work, afterwork, night)
print("\n")
tweets_moment_day = tweets_per_moment_day(time_objects_list)
line4 = f"The is how tweets were written throughout the day:\n" \
      f"\t- Between 12 PM and 8 AM: {tweets_moment_day.get('night_hours'):,} tweets.\n" \
      f"\t- Between 8 AM and 4 PM: {tweets_moment_day.get('work_hours'):,} tweets.\n" \
      f"\t- Between 4 PM and 12 PM: {tweets_moment_day.get('after_work'):,} tweets."
print(line4)


print("\n")
# Number of tweets per hour of the day
line5 = "This is the number of tweets published for every hour of the day:"
print(line5)
dict_hours_tweet_count = dict_occurrences_hours(time_objects_list)
list_hours_tweet_count = [(int(key), value) for key, value in dict_hours_tweet_count.items()]
list_hours_tweet_count.sort()

# This look a bit messy, but only way to make it look good both on terminal and file
line6 = "\n".join([f"\t- {hour[0]}:00: {hour[1]:,} tweets" for hour in list_hours_tweet_count])
print(line6)


print("\n")
# The x hours with the greatest number of tweets. Default value is x=3, but it can be changed.
most_popular_times = find_most_popular_times(time_objects_list, 5)
most_popular_times_formatted = f"{', '.join(most_popular_times[0][:-1])}, and {most_popular_times[0][-1]}"
line7 = f"The {most_popular_times[1]} most popular hours for writing tweets are {most_popular_times_formatted}."
print(line7)

# The x hours with the greatest number of tweets. Default value is x=3, but it can be changed.
least_popular_times = find_least_popular_times(time_objects_list, 5)
least_popular_times_formatted = f"{', '.join(least_popular_times[0][:-1])}, and {least_popular_times[0][-1]}"
line8 = f"The {least_popular_times[1]} least popular hours for writing tweets are {least_popular_times_formatted}."
print(line8)


file = "../results_time_analysis.txt"
lines = [line1, "\n", line2, line3, "\n", line4, "\n", line5, line6, "\n", line7, line8]
write_results_to_file(file, lines)