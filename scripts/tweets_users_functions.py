import os
import re
from datetime import datetime
# All functions to use to generate the stats

def average_followers(dataset):
    """Function to calculate the average number of followers"""
    user_count = len(dataset)
    followers_count = 0

    for data in dataset:
        followers_count += data[3]

    average = followers_count / user_count

    return average


def average_followed(dataset):
    """Function to calculate the average number of friends (followed)"""

    user_count = len(dataset)
    followed_count = 0

    for data in dataset:
        followed_count += data[4]

    average = followed_count / user_count

    return average


def average_status_count(dataset):
    """Function to calculate the average number of statuses (tweets written)"""

    user_count = len(dataset)
    statuses_count = 0

    for data in dataset:
        statuses_count += data[2]

    average = statuses_count / user_count

    return average


def find_most_statuses(dataset):
    """Functions to find user with most written tweets"""

    highest_statuses = 0
    user_name = ""

    for data in dataset:
        if data[2] > highest_statuses:
            highest_statuses = data[2]
            user_name = data[1]

    return highest_statuses, user_name


def find_least_statuses(dataset):
    """Functions to find user with least writtentweets"""

    least_statuses = dataset[0][2]
    user_name = ""

    for data in dataset:
        if data[2] < least_statuses:
            least_statuses = data[2]
            user_name = data[1]

    return least_statuses, user_name


def find_highest_followers(dataset):
    """Functions to find user with most followers"""

    highest_followers = 0
    user_name = ""

    for data in dataset:
        if data[3] > highest_followers:
            highest_followers = data[3]
            user_name = data[1]

    return highest_followers, user_name


def find_highest_friends(dataset):
    """Functions to find user with most friends (followed accounts)"""

    highest_friends = 0
    user_name = ""

    for data in dataset:
        if data[4] > highest_friends:
            highest_friends = data[4]
            user_name = data[1]

    return highest_friends, user_name


def find_users_without_followers(dataset, limit=5):
    """Functions to find x users without followers"""

    users_without_followers = []

    for data in dataset:
        if data[3] == 0:
            users_without_followers.append(data[1])

    # If a huge or too small number is passed as an argument
    if limit > 5 or limit <= 2:
        limit = 5

    # If numbers of elements found smaller than limit
    length_list_result = len(users_without_followers)
    if length_list_result < limit:
        limit = length_list_result

    return users_without_followers, limit


def find_users_most_followers(dataset, limit=5):
    """Functions to find x users with the biggest number of followers"""

    users_with_followers = []

    for data in dataset:
        user_with_count = (data[3], data[1])
        users_with_followers.append(user_with_count)

    users_with_followers.sort()

    if limit > len(users_with_followers):
        limit = len(users_with_followers)

    users_with_followers = users_with_followers[-limit:]

    result_list = []

    for user in users_with_followers:
        result_list.append(f"{user[1]} ({user[0]:,})")

    return result_list, limit


def find_smallest_highest_id(dataset):
    """Function to find the smallest and highest ID"""

    smallest_id = [dataset[0][1], int(dataset[0][0])]
    biggest_id = [dataset[0][1], 0]

    for data in dataset:
        if int(data[0]) < smallest_id[1]:
            smallest_id[0] = data[1]
            smallest_id[1] = int(data[0])

        elif int(data[0]) > biggest_id[1]:
            biggest_id[0] = data[1]
            biggest_id[1] = int(data[0])

    return smallest_id, biggest_id


def find_users_without_followers_but_statuses(dataset, limit_followers=50, limit_statuses=500):
    """Functions to find users with x statuses, but y followers"""

    users_without_followers = []

    for data in dataset:
        if data[3] <= limit_followers and data[2] >= limit_statuses:
            users_without_followers.append(data[1])

    return len(users_without_followers), limit_statuses, limit_followers


def percentage_user_with_less_x_followers(dataset, limit=100):
    """Function to find the percentage of users with less than x followers"""

    users_with_less = 0

    for data in dataset:
        if data[3] <= limit:
            users_with_less += 1

    percentage = (users_with_less * 100)/len(dataset)

    return percentage, limit


def average_followers_users_no_friends(dataset, limit=5):
    """Function to determine the average follower count of users with less than x friends"""

    followers_users_no_friends = []

    for data in dataset:
        if data[4] <= limit:
            followers_users_no_friends.append(data[3])

    average = sum(followers_users_no_friends) / len(followers_users_no_friends)

    return average, limit


def find_highest_followers_friends_ratio(dataset):
    """Function to find the user with the highest followers/friends ratio"""

    username_highest_ratio = ()
    highest_ratio = 0
    followers_friends = (0, 0)

    for data in dataset:
        if data[4] != 0 and data[3] / data[4] > highest_ratio:
            highest_ratio = data[3] / data[4]
            username_highest_ratio = data[1]
            followers_friends = (data[3], data[4])

    return username_highest_ratio, highest_ratio, followers_friends


def find_average_followers_friends_ratio(dataset):
    """Function to find the average followers/friends ratio"""

    followers_friends_ratios = []

    for data in dataset:
        if data[4] != 0:
            followers_friends_ratios.append(data[3] / data[4])

    average = sum(followers_friends_ratios) / len(followers_friends_ratios)

    return average


def write_results_to_file(file, lines):
    """Function to write results to external files"""

    now = datetime.now()

    with open(file,'w') as f:
        f.write(f"These results were generated on {now.strftime('%B, %d %Y at %H:%M:%S')} (GMT+1)." + "\n\n\n")

        for line in lines:
            f.writelines(f"{line}\n")
