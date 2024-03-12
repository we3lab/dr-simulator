""" 
    This module contains the DemandResponseEvents class which is used to 
    generate demand response events for a given time period based on user's inputs. 
"""

import datetime as dt
import numpy as np
from dr_simulator import utils

NOTIFICATION_TIME_ERROR = """
    For day before notification please set self.notification time
    class attribute
"""


class DemandResponseEvents:  # pylint: disable=too-many-instance-attributes
    """
    This class is intended to be used to generate demand response events
    for a given time period based on user's inputs.

    Follow the steps below to generate demand response events:

        1) Create an instance of the class
        2) Set the program parameters using the set_program_parameters function
        3) Sample the ndays of the events using the set_ndays function
        4) Sample the start times of the events using the set_start_times function
        5) Sample the event duration of the events using the set_event_duration function
        6) Sample the probability of each day being selected using the get_pdates function
           this is uniform now, but you can provide a distribution with the same length
           as the number of days between the start and end dates
        7) Sample the event dates of the events using the set_event_dates function
        8) Set the notification time of the events using the set_notification_time function
        9) Generate the event dictionary using the generate_event_dict function

    Parameters
    ----------
    start_dt : datetime.datetime
        Start date of the demand response events period
    end_dt : datetime.datetime
        End date of the demand response events period
    time_step : int
        Time step of the demand response events period in minutes

    """

    def __init__(self, start_dt, end_dt, name="DR Program", time_step=60):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.name = name
        self.time_step = time_step
        self.min_days = None
        self.max_days = None
        self.min_duration = None
        self.max_duration = None
        self.min_start_time = None
        self.max_start_time = None
        self.max_consecutive_events = None
        self.notification_time = None
        self.notification_type = None
        self.n_similar_weekdays = None
        self.ndays = None
        self.start_times = None
        self.event_duration = None
        self.event_days = None
        self.notification_time = None
        self.event_dict = None
        self.dr_events_mtcs = None

    def set_program_parameters(  # pylint: disable=too-many-arguments
        self,
        min_days,
        max_days,
        min_duration,
        max_duration,
        min_start_time,
        max_start_time,
        max_consecutive_events=3,
        notification_time=None,
        notification_type="day_before",
        n_similar_weekdays=10,
        **kwargs
    ):
        """
        This function sets the program parameters for the demand response program

        Parameters
        ----------
        min_days : int
            Minimum number of days between two demand response events
        max_days : int
            Maximum number of days between two demand response events
        min_duration : int
            Minimum duration of a demand response event in hours
        max_duration : int
            Maximum duration of a demand response event in hours
        min_start_time : int
            Minimum start time of a demand response event in hours
        max_start_time : int
            Maximum start time of a demand response event in hours
        notification_time : int
            Notification time of a demand response event in hours
        notification_type : str
            Type of notification time. Default is "day_before".
            Other options are "day_of" and "hour_before"

        """
        self.min_days = min_days
        self.max_days = max_days
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.min_start_time = min_start_time
        self.max_start_time = max_start_time
        self.max_consecutive_events = max_consecutive_events
        self.notification_time = notification_time
        self.notification_type = notification_type
        self.n_similar_weekdays = n_similar_weekdays
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_ndays(self, distribution, distribution_parameters, seed=None):
        """
        This function sets the number of days of the events based on a
        given distribution

        Parameters
        ----------
        ndays : int
            Number of days between two demand response events

        """
        rng = np.random.default_rng(seed)
        self.ndays = np.fmin(
            np.fmax(
                getattr(rng, distribution)(**distribution_parameters), self.min_days
            ),
            self.max_days,
        )

    def set_start_times(self, distribution, distribution_parameters, seed=None):
        """
        This function sets the start times of the events based on a given distribution

        Parameters
        ----------
        start_times : int
            Start time of the demand response events

        """
        # if "size" not in distribution_parameters.keys():
        distribution_parameters["size"] = self.ndays
        rng = np.random.default_rng(seed)
        self.start_times = np.fmin(
            np.fmax(
                getattr(rng, distribution)(**distribution_parameters),
                np.full(self.ndays, self.min_start_time),
            ),
            np.full(self.ndays, self.max_start_time - 1),
        ).astype(int)

    def set_event_duration(self, distribution, distribution_parameters, seed=None):
        """
        This function sets the event duration of the events based on a
        given distribution

        Parameters
        ----------
        event_hours : int
            Number of hours of the demand response events

        """
        distribution_parameters["size"] = self.ndays
        rng = np.random.default_rng(seed)
        event_duration = getattr(rng, distribution)(**distribution_parameters)
        self.event_duration = np.fmin(
            np.fmax(event_duration, np.full(self.ndays, self.min_duration)),
            np.full(self.ndays, self.max_duration),
        ).astype(int)
        self.event_duration = np.fmin(
            self.event_duration,
            np.full(self.ndays, self.max_start_time) - self.start_times,
        )

    def get_pdates(self):
        """
        This function sets the probability of each day being selected based on a
        uniform distribution

        Parameters
        ----------
        None

        Returns
        -------
        p_calendar : numpy.ndarray
            Probability of each day being selected

        """
        dates = [
            self.start_dt + dt.timedelta(days=i)
            for i in range((self.end_dt - self.start_dt).days + 1)
        ]
        woy, dow, p_calendar = utils.create_calender(dates)
        weekdays_idx = (woy[dow < 5], dow[dow < 5])
        n_weekdays = dow[dow < 5].shape[0]
        p_calendar[weekdays_idx] = 1 / n_weekdays
        return p_calendar[woy, dow].ravel()

    def set_event_dates(self, seed=None, p_dates=None):
        """
        This function sets the event dates of the events based on a given distribution

        Parameters
        ----------
        p_dates : float
            Probability of each day being selected

        """
        rng = np.random.default_rng(seed)
        if p_dates is None:
            p_dates = self.get_pdates()
        while True:
            dates = [
                self.start_dt + dt.timedelta(days=i)
                for i in range((self.end_dt - self.start_dt).days + 1)
            ]
            self.event_days = sorted(
                rng.choice(dates, size=self.ndays, p=p_dates, replace=False)
            )
            if self.max_consecutive_events >= self.ndays:
                break
            # find the maximum number of consecutive events
            max_consecutive_events = 0
            for i, event_day in enumerate(self.event_days):
                if i == 0:
                    consecutive_events = 1
                else:
                    if (event_day - self.event_days[i - 1]).days == 1:
                        consecutive_events += 1
                    else:
                        consecutive_events = 1
                max_consecutive_events = max(max_consecutive_events, consecutive_events)
            if max_consecutive_events <= self.max_consecutive_events:
                break

    def set_notification_time(self, notification_time=None):
        """
        This function sets the notification time of the events

        Parameters
        ----------
        notification_time : int
            Notification time of the demand response events

        """
        if notification_time is not None:
            self.notification_time = notification_time

        if self.notification_time is None and (
            self.notification_type in ["day_before", "day_of"]
        ):
            raise ValueError(NOTIFICATION_TIME_ERROR)
        notifiction_time = []

        for i, event_day in enumerate(self.event_days):
            if self.notification_type == "day_before":
                event_detail = dt.datetime(
                    event_day.year,
                    event_day.month,
                    event_day.day,
                    self.notification_time,
                    0,
                    0,
                )
                notifiction_time.append(event_detail - dt.timedelta(days=1))
            elif self.notification_type == "hour_before":
                event_detail = dt.datetime(
                    event_day.year,
                    event_day.month,
                    event_day.day,
                    self.start_times[i],
                    0,
                    0,
                )
                notifiction_time.append(event_detail - dt.timedelta(hours=1))
            elif self.notification_type == "day_of":
                notifiction_time.append(
                    dt.datetime(
                        event_day.year,
                        event_day.month,
                        event_day.day,
                        self.notification_time,
                        0,
                        0,
                    )
                )

        self.notification_time = notifiction_time

    def generate_event_dict(self, program_parameters, simulation_parameters):
        """
        This function generates the event dictionary

        Parameters
        ----------
        None

        """
        self.set_program_parameters(**program_parameters)
        self.set_ndays(**simulation_parameters["n_days"])
        self.set_start_times(**simulation_parameters["start_time"])
        self.set_event_duration(**simulation_parameters["event_duration"])
        self.set_event_dates(**simulation_parameters["event_days"])
        self.set_notification_time()
        self.event_dict = {}
        self.event_dict = {}
        self.event_dict["event_days"] = self.event_days
        self.event_dict["event_details"] = []
        for i, event_day in enumerate(self.event_days):
            end_time = min(self.start_times[i] + self.event_duration[i], 23)
            self.event_dict["event_details"].append(
                {
                    "day": event_day.day,
                    "month": event_day.month,
                    "year": event_day.year,
                    "duration": self.event_duration[i],
                    "start_time": self.start_times[i],
                    "end_time": end_time,
                    "event_hours": list(range(self.start_times[i], end_time)),
                    "notification_time": self.notification_time[i],
                    "similar_weekdays": utils.get_n_similar_weekdays(
                        event_day, self.event_days[:i], self.n_similar_weekdays
                    ),
                }
            )
        return self.event_dict

    def create_dr_events_mtcs(
        self, program_parameters, simulation_parameters, n_simulations
    ):
        """
        This function creates the demand response events for the given number of simulations

        Parameters
        ----------
        n_simulations : int
            Number of simulations

        """
        self.dr_events_mtcs = []
        for _ in range(n_simulations):
            dr_instance = DemandResponseEvents(
                self.start_dt, self.end_dt, name=self.name, time_step=self.time_step
            )
            event_dict = dr_instance.generate_event_dict(
                program_parameters=program_parameters,
                simulation_parameters=simulation_parameters,
            )
            self.dr_events_mtcs.append(event_dict)

        return self.dr_events_mtcs
