import sqlalchemy
from scripts.tweets_users_functions import *
from database_queries import *

# In this file, user data is analyzed

# First a general overview of the data
line1 = f"The following stats were obtained by analyzing {len(result_set_tweets)} tweets from {len(result_set_users)} users.\n"
print(line1)

line2 = "User-related stats:\n"
print(line2)

# Average values
# The average number of followers.
average_followers_count = average_followers(result_set_users)
line3 = f"The average number of followers is {int(average_followers_count)}."
print(line3)

# The average number of tweets published by users.
average_status_count = average_status_count(result_set_users)
line4 = f"The average number of statuses is {int(average_status_count)}."
print(line4)

# The average number of friends
average_followed_count = average_followed(result_set_users)
line5 = f"The average number of friends (followed accounts) is {int(average_followed_count)}."
print(line5)

# The average followers/friends ratio
average_followers_friends_ratio = find_average_followers_friends_ratio(result_set_users)
line6 = f"The average followers/friends ratio is {int(average_followers_friends_ratio)} followers for every followed account."
print(line6)


# Highest values
print("\n")

# Highest number of tweets
highest_status = find_most_statuses(result_set_users)
line7 = f"The user with the highest status count is {highest_status[1]} with {highest_status[0]} statuses."
print(line7)

# Highest number of followers
highest_followers = find_highest_followers(result_set_users)
line8 = f"The user with the highest followers count is {highest_followers[1]} with {highest_followers[0]} followers."
print(line8)

# Highest number of friends
highest_friends = find_highest_friends(result_set_users)
line9 = f"The user with the highest friend count is {highest_friends[1]} with {highest_friends[0]} friends."
print(line9)

# User with the highest followers/friends ratio
user_highest_ratio = find_highest_followers_friends_ratio(result_set_users)
line10 = f"The user with highest followers/friends ratio ({int(user_highest_ratio[1])} followers for every friend) is {user_highest_ratio[0]} with {user_highest_ratio[2][0]} followers and {user_highest_ratio[2][1]} friends."
print(line10)


print("\n")
# Follower counts

# 5 users without followers
user_without_followers = find_users_without_followers(result_set_users)
limit = user_without_followers[1]
users_list = user_without_followers[0]
# This is to add Oxford comma and 'and' before final item
users_list_formatted = f"{(', '.join(users_list[:limit-1]))}, and {str(user_without_followers[0][-1])}"
line11 = f"These are {user_without_followers[1]} (or less) users who don't have any followers at all: {users_list_formatted}."
print(line11)

# X users with highest followers count (X = 5 per default, but can be changed)
users_highest_followers = find_users_most_followers(result_set_users)
limit = users_highest_followers[1]
users_list = users_highest_followers[0]
# This is to add Oxford comma and 'and' before final item
users_list_formatted = f"{(', '.join(users_list[:limit-1]))}, and {str(users_list[-1])}"
line12 = f"The {users_highest_followers[1]} users with the highest follower counts are {users_list_formatted}."
print(line12)


print("\n")
# Possible bots
# Number of users with less than x followers, but y statuses. x, y can be passed as parameters, eg. (dataset, limit_followers=50, limit_statuses=500)
users_no_followers_but_statuses = find_users_without_followers_but_statuses(result_set_users)
line13 = f"There are {users_no_followers_but_statuses[0]} users with less than {users_no_followers_but_statuses[2]} followers, but at least {users_no_followers_but_statuses[1]} statuses."
print(line13)

users_no_followers_but_statuses = find_users_without_followers_but_statuses(result_set_users, 100, 500)
line14 = f"There are {users_no_followers_but_statuses[0]} users with less than {users_no_followers_but_statuses[2]} followers, but at least {users_no_followers_but_statuses[1]} statuses."
print(line14)

print("\n")
# Users with few friends
# Average of followers of users with less than x friends (default is 5, can be changed)
average_users_no_friends = average_followers_users_no_friends(result_set_users)
line15 = f"On average, users who follow less than {average_users_no_friends[1]} other users have {int(average_users_no_friends[0])} followers."
print(line15)

average_users_no_friends = average_followers_users_no_friends(result_set_users, 100)
line16 = f"On average, users who follow less than {average_users_no_friends[1]} other users have {int(average_users_no_friends[0])} followers."
print(line16)


print("\n")
# Percentages of users with few followers
# Percentage of users with less than x followers (default is 100, can also be passed as parameter
user_with_less_followers = percentage_user_with_less_x_followers(result_set_users, 100)
line17 = f"The percentage of users with less than {user_with_less_followers[1]} followers is {int(user_with_less_followers[0])}%."
print(line17)

user_with_less_followers = percentage_user_with_less_x_followers(result_set_users, 500)
line18 = f"The percentage of users with less than {user_with_less_followers[1]} followers is {int(user_with_less_followers[0])}%."
print(line18)

print("\n")
# ID stats
# Accounts with the highest and smallest IDs
smallest_highest_id = find_smallest_highest_id(result_set_users)
smallest_id = smallest_highest_id[0]
highest_id = smallest_highest_id[1]
print(f"The user with the smallest ID ({smallest_id[1]}) is {smallest_id[0]}, while the biggest ID ({highest_id[1]}) belongs to {highest_id[0]}.")


# Write results to file
file = "../results_users_analysis.txt"
lines = [line1, line2, line3, line4, line5, line6, "\n", line7, line8, line9, line10, "\n", line11, line12, "\n", line13,
         line14, "\n", line15, line16, "\n", line17, line18]
write_results_to_file(file, lines)