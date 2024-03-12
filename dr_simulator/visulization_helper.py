""" Helper functions for visualizing the DR event data """

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


# helper function to visualize event data in a monthly calender
def plot_dr_events(start_dt, end_dt, dr_events, sampled_event_hours):
    """

    Plots the DR events in a monthly calendar

    Parameters
    ----------
    start_dt : datetime.datetime
        Start date of the calendar

    end_dt : datetime.datetime
        End date of the calendar

    dr_events : list
        List of datetime.datetime objects representing the start of each event

    sampled_event_hours : list
        List of floats representing the number of hours of each event

    Returns
    -------
    matplotlib.pyplot.figure, matplotlib.pyplot.axes
        Figure and axes objects containing the calendar

    """
    dates, data = _generate_data(start_dt, end_dt, dr_events, sampled_event_hours)
    fig, ax = plt.subplots(figsize=(5, 5))
    cbar = _calendar_heatmap(ax, dates, data)
    return fig, ax, cbar


def _generate_data(start_dt, end_dt, dr_events, sampled_event_hours):
    ndays = (end_dt - start_dt).days + 1
    data = np.nan * np.zeros(ndays)
    for i, dr_event in enumerate(dr_events):
        idx = (dr_event - start_dt).days
        data[idx] = sampled_event_hours[i]
    dates = [start_dt + dt.timedelta(days=i) for i in range(ndays)]
    return dates, data


def _calendar_array(dates, data):
    woy, dow = zip(*[d.isocalendar()[1:] for d in dates])
    woy = np.array(woy) - min(woy)  # make lowest week 0
    dow = np.array(dow) - 1  # make Monday 0
    ni = max(woy) + 1  # number of weeks in dates
    calendar = np.nan * np.zeros((ni, 7))  # create arrays of NaN for the calendar
    calendar[woy, dow] = data
    return woy, dow, calendar


def _calendar_heatmap(ax, dates, data):
    woy, dow, calendar = _calendar_array(dates, data)
    cmap = colors.ListedColormap(
        ["#FDD9D9", "#FCC0C0", "#FBA7A7", "#FA8E8E", "#F97575", "#F85C5C", "#F74343"]
    )
    bounds = [1, 2, 3, 4, 5, 6, 7, 8]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    im = ax.imshow(calendar, interpolation="none", cmap=cmap, norm=norm)
    _label_days(ax, dates, woy, dow, calendar)
    _label_months(ax, dates, woy)
    cbar = ax.figure.colorbar(im)
    return cbar


def _label_days(ax, dates, woy, dow, calendar):
    ni, _ = calendar.shape
    day_of_month = np.nan * np.zeros((ni, 7))
    day_of_month[woy, dow] = [d.day for d in dates]
    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day):
            ax.text(j, i, int(day), ha="center", va="center")
    ax.set(xticks=np.arange(7), xticklabels=["M", "T", "W", "T", "F", "S", "S"])
    ax.xaxis.tick_top()


def _label_months(ax, dates, woy):
    month_labels = np.array(
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
    )
    months = np.array([d.month for d in dates])
    uniq_months = sorted(set(months))
    yticks = [woy[months == m].mean() for m in uniq_months]
    labels = [month_labels[m - 1] for m in uniq_months]
    ax.set(yticks=yticks)
    ax.set_yticklabels(labels, rotation=90)
