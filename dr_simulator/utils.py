""" This module contains utility functions for DR Simulator """

import json
import pickle
import datetime as dt
from enum import Enum
import numpy as np


class DistributionTypes(Enum):
    """Enum class for supported distributions"""

    NORMAL = "normal"
    UNIFORM = "uniform"
    POISSON = "poisson"


distr_param_mapping = {
    DistributionTypes.NORMAL: ["loc", "scale"],
    DistributionTypes.UNIFORM: ["low", "high"],
    DistributionTypes.POISSON: ["lam"],
}


def validate_distribution_params(distr_type, distr_params):
    """Validates the distribution parameters

    Parameters
    ----------
    distr_type : DistributionTypes
        Distribution type

    distr_params : dict
        Distribution parameters

    Returns
    -------
    bool
        True if the parameters are valid, False otherwise
    """
    if distr_type not in DistributionTypes:
        return False
    if not isinstance(distr_params, dict):
        return False
    if not all(k in distr_params for k in distr_param_mapping[distr_type]):
        return False
    return True


def text_to_param_dict(distr_type, distr_params_text):
    """Converts distribution parameters entered as text to param_dict

    Parameters
    ----------
    distr_type : DistributionTypes
        Distribution type

    distr_params_text : str
        Distribution parameters entered as text

    Returns
    -------
    dict
        Distribution parameters as dictionary

    """
    param_list = distr_params_text.split(",")
    if not len(param_list) == len(distr_param_mapping[distr_type]):
        raise ValueError(f"Invalid number of parameters for {distr_type} distribution")
    param_dict = {
        k: int(v) for k, v in zip(distr_param_mapping[distr_type], param_list)
    }
    return param_dict


def days_in_year_month(year, month):
    """
    Parameters
    ----------
    year : int
    month : int

    Returns
    -------
    int
        number of days in a `month` of `year`
    """
    if month == 2:
        # Check if it's a leap year
        if year % 4 == 0:
            return 29
        return 28
    if month in [4, 6, 9, 11]:
        return 30
    return 31


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
