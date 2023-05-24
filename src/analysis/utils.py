import pandas.arrays as pdarray
import numpy as np


def calculate_days_between(datetimes: pdarray.DatetimeArray):
    days_between = list()
    if len(datetimes) == 1:
        return None
    else:
        time_order = datetimes.argsort()
        for i in range(len(time_order)-1):
            days_between.append((datetimes[time_order[i+1]]-datetimes[time_order[i]]).days)
    return days_between
    

def calculate_result_of_waiting(array_of_days_between, max_days_to_wait: int):
    """
    Best explained through an example:
    If the company is willing to wait 1 day before shipping, how many less shipments will be made for this list of days
    between shipping.
    [10/05/2001, 11/05/2001, 12/05/2001, 13/05/2001, 15/05/2001, 16/05/2001, 17/05/2001]
    days_between:
    [1, 1, 1, 2, 1, 1]
    First two shipments could be one shipment
    3rd and 4th could be one shipment
    5th and 6th could be one shipment
    7th could be one shipment
    Resulting decrease in shipments = 3

    [10/05/2001, 11/05/2001, 12/05/2001, 13/05/2001, 14/05/2001, 15/05/2001, 16/05/2001]
    days_between:
    [1, 1, 1, 1, 1, 1]
    This would also return 3 as cannot wait more than a day

    [10/05/2001, 12/05/2001, 15/05/2001, 18/05/2001, 22/05/2001, 24/05/2001, 26/05/2001]
    days_between:
    [2, 3, 3, 4, 2, 2]
    This would return 0 as no waiting is a day

    [10/05/2001, 12/05/2001, 15/05/2001, 18/05/2001, 22/05/2001, 23/05/2001, 26/05/2001]
    days_between:
    [2, 3, 3, 4, 1, 3]
    This would return 1

    [10/05/2001, 12/05/2001, 14/05/2001, 18/05/2001, 22/05/2001, 23/05/2001, 26/05/2001]
    [2, 2, 4, 4, 1, 3]
    waiting for 4 would return 4
    as 1st, 2nd, 3rd could be 1
    4th, 5th could be 1
    5th, 6th could be 1
    so resulting drop in shipments = 4

    [10/05/2001, 12/05/2001, 14/05/2001, 18/05/2001, 22/05/2001, 23/05/2001, 26/05/2001]
    [2, 2, 4, 4, 1, 3]

    :param array_of_days_between:
    :param max_days_to_wait:
    :return:
    """
    if array_of_days_between is None:
        return 0
    count = 0
    current_no_days = 0
    for i in array_of_days_between:
        current_no_days += i
        if current_no_days <= max_days_to_wait:
            count += 1
        else:
            current_no_days = 0
    return count

