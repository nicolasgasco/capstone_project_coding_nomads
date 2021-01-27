import os
import time


def create_list_times(dataset):
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
    hours_list = [(value, key) for key, value in hours_dict.items()]
    hours_list.sort(reverse=True)
    most_popular_hours = hours_list[:limit]

    result = [f"{hour[1]} ({hour[0]})" for hour in most_popular_hours]

    return result, limit
