"""This module contains utility functions for DR Simulator"""

# pylint: disable=line-too-long, too-many-arguments, too-many-locals
import re
import json
import pickle
import datetime as dt
from enum import Enum
from warnings import warn
import numpy as np
import pandas as pd


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


def parse_freq(freq):
    """Parses a time frequency code string, returning its type and its freq_binsize

    Parameters
    ----------
    freq: str
        string of the form [type][freq_binsize], where type corresponds to a numpy.timedelta64 encoding
        and freq binsize is an integer giving the number of increments of `type` of one binned increment of our time variable
        (for example '6h' means the data are grouped into increments of 6 hours)

    Returns
    -------
    tuple
        tuple of the form (`int`,`str`) giving the binsize and type of the time frequency given
    """
    freq_type = re.sub("[0-9]", "", freq)
    freq_binsize = int(re.sub("[^0-9]", "", freq))
    return freq_binsize, freq_type


def get_freq_binsize_minutes(freq):
    """Gets size of a given time frequency expressed in units of minutes
    Parameters
    ----------
    freq: str
        a string of the form [type][freq_binsize], where type corresponds to a numpy.timedelta64 encoding
        and freq binsize is an integer giving the number of increments of `type` of one binned increment of our time variable
        (for example '6h' means the data are grouped into increments of 6 hours)

    Raises
    ------
    ValueError
        when resolution is not minute, hourly, or daily

    Returns
    -------
    int
        integer giving the number of minutes in the given time frequency unit
    """
    freq_binsize, freq_type = parse_freq(freq)
    if freq_type == "m":
        multiplier = 1
    elif freq_type == "h":
        multiplier = 60
    elif freq_type in ["D", "d"]:
        multiplier = 60 * 24
    else:
        raise ValueError(
            "Cannot deal with data that are not in minute, hourly, or daily resolution"
        )
    return multiplier * freq_binsize


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


def get_date_range_prev_month(date, n_days):
    """
    This function gets the date range for the previous month

    Parameters
    ----------
    date : datetime.datetime
        Date of the event
    n_days : int
        Number of days in the previous month

    Returns
    -------
    date_range : list
        List of length n_days with the dates of the previous month

    """
    date_range = []
    for _ in range(n_days):
        date = date - dt.timedelta(days=1)
        date_range.append(date)
    return date_range


def get_hourly_average_consumption(
    similar_days,
    event_hour,
    output_data,
    electricity_purchase_varnames,
    datetime_varname,
):
    """Get the baseline consumption for a given demand response event

    Parameters
    ----------
    similar_days : np.array of np.datetime64
        List of similar weekdays

    event_hour : int
        Hour of the day of the demand response event

    output_data : pandas.DataFrame
        the output data for baseline calculation

    electricity_purchase_varnames : list
        List of electricity purchase variable names

    datetime_varname : str
        Name of the datetime variable in the output data

    Returns
    -------
    baseline_consumption : float
        Baseline consumption in kWh
    """

    # Extract the unique years, months, and days
    similar_days = pd.Series(similar_days)

    years = np.unique(similar_days.dt.year)
    months = np.unique(similar_days.dt.month)
    days = np.unique(similar_days.dt.day)

    # Filter the output data to only include the similar days
    filter_mask = (
        np.isin(output_data[datetime_varname].dt.year, years)
        & np.isin(output_data[datetime_varname].dt.month, months)
        & np.isin(output_data[datetime_varname].dt.day, days)
        & (output_data[datetime_varname].dt.hour == event_hour)
    )

    if filter_mask.sum() == 0:
        raise ValueError("No similar days found in the output data")

    baseline_consumption = (
        output_data.loc[filter_mask, electricity_purchase_varnames].sum(axis=1).mean()
    )

    return baseline_consumption


def get_day_of_adj_ratio(
    dr_period_details,
    output_data,
    electricity_purchase_varnames,
    datetime_varname,
    day_of_adj_details=None,
):
    """
    Get the day-of-adjustment ratio for a given demand response event.
    The day-of-adjustment ratio is calculated as the average consumption
    of the window hours before the event divided by the average consumption
    of the same hours on similar weekdays.
    The day-of-adjustment ratio is capped at the day_of_adj_max value.

    Parameters
    ----------
    dr_period_details : dict
        Dictionary with the details of the demand response event period and baseline_days

    output_data : pandas.DataFrame
        the output data for baseline calculation

    electricity_purchase_varnames : list
        List of electricity purchase variable names

    datetime_varname : str
        Name of the datetime variable in the output data

    day_of_adj_details : dict
        Dictionary with the details of the day-of-adjustment calculation
        (default is {
            "maximum": 0.4,
            "hours before": 4,
            "duration": 3
        }) for PG&E's CBP DR

    Returns
    -------
    day_of_adj_ratio : float
        Day-of-adjustment ratio
    """
    if day_of_adj_details is None:  # Default values for PG&E's CBP DR
        day_of_adj_details = {"maximum": 0.4, "hours before": 4, "duration": 3}

    day_of_adj_baseline_consumption = 0
    day_of_adj_consumption = 0
    doa_max = day_of_adj_details["maximum"]
    doa_hours_before = day_of_adj_details["hours before"]
    doa_duration = day_of_adj_details["duration"]

    baseline_days = dr_period_details["baseline_days"]
    event_start_dt, _ = dr_period_details["event_dts"]

    doa_hours_before = np.timedelta64(doa_hours_before - 1, "h")
    doa_duration = np.timedelta64(doa_duration - 1, "h")

    for day_of_adj_hour in pd.date_range(
        event_start_dt - doa_hours_before,
        event_start_dt - doa_hours_before + doa_duration,
        freq="h",
    ):
        baseline_consumption = get_hourly_average_consumption(
            baseline_days,
            day_of_adj_hour.hour,
            output_data,
            electricity_purchase_varnames,
            datetime_varname,
        )
        day_of_adj_baseline_consumption += baseline_consumption

        day_of_adj_consumption = get_hourly_average_consumption(
            np.array([np.datetime64(day_of_adj_hour)]),
            day_of_adj_hour.hour,
            output_data,
            electricity_purchase_varnames,
            datetime_varname,
        )

        day_of_adj_consumption += day_of_adj_consumption

    day_of_adj_consumption /= 3
    day_of_adj_baseline_consumption /= 3

    day_of_adj_ratio = (
        day_of_adj_consumption / day_of_adj_baseline_consumption
        if day_of_adj_baseline_consumption != 0
        else 0
    )
    day_of_adj_ratio = min(day_of_adj_ratio, doa_max)
    return day_of_adj_ratio


def get_hourly_dr_event_arrays(
    event_start_dt, horizon_start_dt, horizon_end_dt, resolution="15m"
):
    """
    Get the hourly demand response event arrays for the optimization data
    with 1 for the hours of the demand response event and 0 otherwise
    for each demand response event hours

    Parameters
    ----------
    event_start_dt : np.datetime64
        Start datetime of the demand response event

    event_end_dt : np.datetime64
        End datetime of the demand response event

    horizon_start_dt : np.datetime64
        Start datetime of the optimization horizon

    horizon_end_dt : np.datetime64
        End datetime of the optimization horizon

    resolution : str
        Resolution of the optimization data

    Returns
    -------
    hourly_dr_event_arrays : list of np.array
        List of np.array with 1 for the hours of the demand response event and 0 otherwise
    """
    res_binsize_minutes = get_freq_binsize_minutes(resolution)
    n_per_hour = int(60 / res_binsize_minutes)
    ntsteps = int(
        (horizon_end_dt - horizon_start_dt) / np.timedelta64(res_binsize_minutes, "m")
    )
    datetime = pd.DataFrame(
        np.array(
            [
                horizon_start_dt + np.timedelta64(i * res_binsize_minutes, "m")
                for i in range(ntsteps)
            ]
        ),
        columns=["DateTime"],
    )
    hourly_dr_event_arrays = np.zeros(ntsteps)
    event_idx = np.where(datetime["DateTime"] == event_start_dt)
    if len(event_idx[0]) == 0:
        return hourly_dr_event_arrays
    event_idx = event_idx[0][0]
    hourly_dr_event_arrays[event_idx : event_idx + n_per_hour] = 1
    return hourly_dr_event_arrays


def get_dr_dates(event_details, horizon_start_dt, horizon_end_dt):
    """
    Get the demand response event dates for the optimization horizon

    Parameters
    ----------
    event_details : list of dict
        Dictionary with the details of the demand response event

    horizon_start_dt : np.datetime64
        Start datetime of the optimization horizon

    horizon_end_dt : np.datetime64
        End datetime of the optimization horizon

    Returns
    -------
    dr_events_dts : dict of np.datetime64
        List of np.datetime64 with the demand response event dates for the optimization horizon
    """
    if event_details[0]["day"] is None:  # If there are no demand response events
        return {}
    dr_events_dts = {}
    for i, event in enumerate(event_details):
        event_start_dt = np.datetime64(
            dt.datetime(
                event["year"], event["month"], event["day"], event["start_time"], 0, 0
            ),
            "s",
        )
        event_end_dt = event_start_dt + np.timedelta64(event["duration"], "h")
        start_dt, end_dt = get_start_end_dt(
            event_start_dt, event_end_dt, horizon_start_dt, horizon_end_dt
        )
        if start_dt is not None:
            dr_events_dts[f"event_{i}"] = {}
            dr_events_dts[f"event_{i}"]["event_dts"] = np.array([start_dt, end_dt])
            dr_events_dts[f"event_{i}"]["baseline_days"] = event["baseline_days"]

    dr_events_dts = (
        combine_overlapping_dr_events(dr_events_dts)
        if len(dr_events_dts) > 1
        else dr_events_dts
    )
    return dr_events_dts


def combine_overlapping_dr_events(dr_events_dts):
    """
    Sorts the events in choronological order
    and combines overlapping demand response (DR) events into a single event

    Parameters
    ----------
    dr_events_dts : dict
    A dictionary where values are lists or arrays of start and end times of DR events.

    Returns
    -------
    dr_events_dts: dict
    A dictionary where values are lists or arrays of start and end times of combined if overlapping DR events.
    """
    # Convert dictionary values to a numpy array and sort by start times
    dr_dates_array = np.array(
        [val["event_dts"] for val in dr_events_dts.values()], dtype="datetime64"
    )
    baseline_days = [val["baseline_days"] for val in dr_events_dts.values()]
    dr_dates_array = dr_dates_array[np.argsort(dr_dates_array[:, 0])]
    baseline_days = [baseline_days[i] for i in np.argsort(dr_dates_array[:, 0])]

    # Initialize the combined events array
    combined_events = [dr_dates_array[0]]
    for i in range(1, len(dr_dates_array)):
        if dr_dates_array[i][0] < combined_events[-1][1]:
            raise ValueError("Overlapping DR events are not allowed")

    return dr_events_dts


def get_start_end_dt(dr_start_dt, dr_end_dt, horizon_start_dt, horizon_end_dt):
    """
    Get the start and end datetime of the demand response event within the optimization horizon

    Parameters
    ----------
    dr_start_dt : np.datetime64
        Start datetime of the demand response event

    dr_end_dt : np.datetime64
        End datetime of the demand response event

    horizon_start_dt : np.datetime64
        Start datetime of the optimization horizon

    horizon_end_dt : np.datetime64
        End datetime of the optimization horizon

    Returns
    -------
    start_dt : np.datetime64
        Start datetime of the demand response event within the optimization horizon

    end_dt : np.datetime64
        End datetime of the demand response event within the optimization horizon
    """
    start_dt = dr_start_dt
    end_dt = dr_end_dt
    # check if the DR event is within the control horizon
    if dr_start_dt < horizon_start_dt:
        if dr_end_dt < horizon_start_dt:
            warn("DR event is before the control horizon")
            start_dt = None
            end_dt = None
        if dr_end_dt >= horizon_end_dt:
            warn(
                "DR event engulfs the control horizon. Setting start time "
                "and end time to start and end of horizon respectively"
            )
            start_dt = horizon_start_dt
            end_dt = horizon_end_dt
        if horizon_start_dt <= dr_end_dt < horizon_end_dt:
            warn(
                "DR event starts before the control horizon. Setting start time "
                "to the start of the control horizon"
            )
            start_dt = horizon_start_dt
    elif horizon_start_dt <= dr_start_dt < horizon_end_dt:
        if dr_end_dt >= horizon_end_dt:
            warn(
                "DR event ends past the control horizon. Setting end time "
                "to the end of the control horizon"
            )
            end_dt = horizon_end_dt
    else:
        warn("DR event is after the control horizon")
        start_dt = None
        end_dt = None
    return start_dt, end_dt


def convert_dr_event_details(event_details):
    """
    Converts the demand response event details to the format required by the optimizer

    Parameters
    ----------
    event_details : dict
        Dictionary with the details of the demand response event

    Returns
    -------
    event_details : dict
        Dictionary with the details of the demand response event in the format required by the optimizer
    """
    event_details["baseline_days"] = np.array(
        [
            np.datetime64(similar_weekday)
            for similar_weekday in event_details["baseline_days"]
        ],
        dtype="datetime64",
    )
    event_details["day"] = int(event_details["day"])
    event_details["month"] = int(event_details["month"])
    event_details["year"] = int(event_details["year"])
    event_details["start_time"] = int(event_details["start_time"])
    event_details["duration"] = int(event_details["duration"])

    return event_details


def sanitize_dr_data(dr_data):
    """
    Sanitize the demand response data

    Parameters
    ----------
    dr_data : dict
        Dictionary with the demand response data

    Returns
    -------
    dr_data : dict
        Dictionary with the sanitized demand response data
    """
    if dr_data["name"] is None:
        return dr_data
    for i, event_details in enumerate(dr_data["events detail"]):
        dr_data["events detail"][i] = convert_dr_event_details(event_details)
    return dr_data


def get_dr_baseline_dates(dr_data):
    """
    Get the demand response baseline dates

    Parameters
    ----------
    dr_data : dict
        Dictionary with the demand response data


    Returns
    -------
    dr_baseline_dates : array of np.datetime64
        np.array of np.datetime64 with the demand response baseline dates
    """
    dr_baseline_dates = []
    for event_details in dr_data["events detail"]:
        dr_baseline_dates.extend(event_details["baseline_days"])
    return np.array(dr_baseline_dates, dtype="datetime64")
