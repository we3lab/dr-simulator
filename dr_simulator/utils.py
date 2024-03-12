""" This module contains utility functions for DR Simulator """

import json
import pickle
import datetime as dt
import numpy as np


def pickle_load(path):
    """Loads a pickled object (fitted model, dictionary with data, etc)

    Parameters
    ----------
    path : str
        path to object to load

    Returns
    -------
    object
        unpickled object found at the `path`
    """
    with open(path, "rb") as f:
        object_ = pickle.load(f)
    return object_


def pickle_dump(object_, path):
    """Pickles an object (fitted model, dictionary with data, etc)

    Parameters
    ----------
    object_
        object to compress

    path : str
        path where the pickled object is saved
    """
    with open(path, "wb") as f:
        pickle.dump(object_, f)


def json_load(path):
    """Loads a json string to python

    Parameters
    ----------
    path : str
        path to object to load

    Returns
    -------
    object_ : object
        python object converted from str
    """
    with open(path, "r", encoding="utf-8") as f:
        object_ = json.load(f)
    return object_


def json_dump(object_, path):
    """Dumps a python object to a json string

    Parameters
    ----------
    object_ : object
        python object to convert to str

    path : str
        path where the json string is saved
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(object_, f, ensure_ascii=False, indent=4)


def create_calender(dates):
    """
    This function creates a calendar for the given dates

    Parameters
    ----------
    dates : list
        List of dates

    Returns
    -------
    woy : numpy.ndarray
        Week of the year of the dates
    dow : numpy.ndarray
        Day of the week of the dates
    calendar : numpy.ndarray
        Calendar of the dates

    """
    woy, dow = zip(*[d.isocalendar()[1:] for d in dates])
    woy = np.array(woy) - min(woy)  # make lowest week 0
    dow = np.array(dow) - 1  # make Monday 0
    ni = max(woy) + 1  # number of weeks in dates
    calendar = np.zeros((ni, 7))  # create arrays of Zeros for the calendar
    return woy, dow, calendar


def get_n_similar_weekdays(date, prev_event_days, n_weekdays=10):
    """
    This function gets the 10 similar weekdays excluding the event days

    Parameters
    ----------
    date : datetime.datetime
        Date of the event
    prev_event_days : list
        List of previous event days
    n_weekdays : int (default=10)
        Number of similar weekdays to return

    Returns
    -------
    similar_weekdays : list
        List of length of previous n_weekdays excluding the event days

    """
    similar_weekdays = []
    while len(similar_weekdays) < n_weekdays:
        date = date - dt.timedelta(days=1)
        if date.weekday() < 5 and date not in prev_event_days:
            similar_weekdays.append(date)
    return similar_weekdays
