import os
import time



def create_ordered_list_times(dataset):
    """Function that returns a list of time objects and relative tweet ID"""
    time_objects = []
    for data in dataset:
        time = data[3]
        tweet_id = data[0]

        time_objects.append((time, tweet_id))
        time_objects.sort()

    return time_objects


def dict_occurrences_hours(time_objects):
    """Function returns the occurrence of every time object (only hour, not date)"""

    all_hours = [time[0].strftime("%H") for time in time_objects]
    hours_occurrences = {}

    for hour in all_hours:
        hours_occurrences.setdefault(hour, 0)
        hours_occurrences[hour] += 1

    return hours_occurrences


def find_most_popular_times(time_objects, limit=3):
    """Returns limit number of most popular hours"""
    hours_dict = dict_occurrences_hours(time_objects)
    hours_list = [(value, f"{int(key)}:00") for key, value in hours_dict.items()]
    hours_list.sort(reverse=True)
    most_popular_hours = hours_list[:limit]

    result = [f"{hour[1]} ({hour[0]:,})" for hour in most_popular_hours]

    return result, limit


def find_least_popular_times(time_objects, limit=3):
    """Returns limit number of least popular hours"""
    hours_dict = dict_occurrences_hours(time_objects)
    hours_list = [(value, f"{int(key)}:00") for key, value in hours_dict.items()]
    hours_list.sort()
    most_popular_hours = hours_list[:limit]

    result = [f"{hour[1]} ({hour[0]:,})" for hour in most_popular_hours]

    return result, limit


def tweets_per_moment_day(time_objects):
    """Returns the number of tweets published in specific moments of the day"""
    work_hours = 0
    night_hours = 0
    after_work = 0

    hours_dict = dict_occurrences_hours(time_objects)
    for time, count in hours_dict.items():
        if 8 <= int(time) <= 16:
            work_hours += count
        elif 17 <= int(time) <= 23:
            after_work += count
        else:
            night_hours += count

    dict_occurrences_daymoment = {}
    dict_occurrences_daymoment["work_hours"] = work_hours
    dict_occurrences_daymoment["night_hours"] = night_hours
    dict_occurrences_daymoment["after_work"] = after_work

    return dict_occurrences_daymoment
