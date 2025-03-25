"""
This module contains the cost functions used in the demand response simulator.
"""

# pylint: disable=line-too-long, too-many-arguments, too-many-locals
import numpy as np
import pandas as pd

from dr_simulator import utils as ut


def calculate_dr_payment_region(ratio, domains):
    """Calculate the payment multiplier for a single demand response event for CBP.

    Paremeters
    ----------
    ratio : float
        The ratio of baseline consumption to actual consumption

    domains : list
        list of tuples of the form (lower, upper) that define the regions of the
        payment function

    Returns
    -------
    int
        The domain index the ratio corresponds to
    """

    for i, domain in enumerate(domains):
        lower, upper = domain
        if lower is not None:
            if upper is not None:
                if lower <= ratio < upper:
                    return i
            else:
                if lower <= ratio:
                    return i
        else:
            if upper is not None:
                if ratio < upper:
                    return i
    raise ValueError("Ratio not in any domain")


def calculate_dr_payment(  # pylint: disable=too-many-positional-arguments
    dr_period_details,
    capacity_bid,
    capacity_price,
    payment_functions,
    output_data,
    electricity_purchase_varnames,
    datetime_varname,
    day_of_adj_details=None,
):
    """
    Calculate the payment expression from a demand response event

    Parameters
    ----------
    dr_period_details : dict
        Dictionary with the details of the demand response event period and baseline_days

    capacity_bid : float
        The capacity bid for the demand response event

    capacity_price : float
        The price for the capacity bid

    payment_functions : list
        List of dictionaries with the keys "domain", "slope", and "intercept" that define
        the payment function

    output_data : pandas.DataFrame
        The output data for baseline calculation

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
    dict
        Dictionary with keys "payment", "ratio", "reduction", and "baseline"

    """

    dr_payment = []
    avg_ratio = []
    avg_reduction = []
    avg_baseline_consumption = []
    avg_consumption = []

    dr_event_start_time, dr_event_end_time = dr_period_details["event_dts"]
    baseline_days = dr_period_details["baseline_days"]
    domains = [function["domain"] for function in payment_functions]
    slopes = [function["slope"] for function in payment_functions]
    intercepts = [function["intercept"] for function in payment_functions]

    dr_start_dt = pd.Timestamp(dr_event_start_time)
    dr_end_dt = pd.Timestamp(dr_event_end_time - np.timedelta64(1, "h"))

    for event_start_time in pd.date_range(start=dr_start_dt, end=dr_end_dt, freq="h"):
        baseline_consumption = ut.get_hourly_average_consumption(
            baseline_days,
            event_start_time.hour,
            output_data,
            electricity_purchase_varnames,
            datetime_varname,
        )

        if day_of_adj_details and event_start_time == dr_start_dt:
            day_of_adj_ratio = ut.get_day_of_adj_ratio(
                dr_period_details,
                output_data,
                electricity_purchase_varnames,
                datetime_varname,
                day_of_adj_details,
            )
            baseline_consumption *= 1 + day_of_adj_ratio

        hourly_consumption = ut.get_hourly_average_consumption(
            np.array([event_start_time], dtype="datetime64[h]"),
            event_start_time.hour,
            output_data,
            electricity_purchase_varnames,
            datetime_varname,
        )

        hourly_reduction = baseline_consumption - hourly_consumption

        ratio = hourly_reduction / capacity_bid if capacity_bid > 0 else 0

        ratio_region = calculate_dr_payment_region(ratio, domains)

        dr_payment += [
            (
                capacity_bid
                * capacity_price
                * (slopes[ratio_region] * ratio + intercepts[ratio_region])
            )
        ]
        avg_baseline_consumption += [baseline_consumption]
        avg_consumption += [hourly_consumption]
        avg_ratio += [ratio]
        avg_reduction += [hourly_reduction]

    return {
        "payment_list": dr_payment,
        "payment": sum(dr_payment),
        "ratio_list": avg_ratio,
        "ratio": np.mean(avg_ratio),
        "reduction_list": avg_reduction,
        "reduction": np.mean(avg_reduction),
        "baseline_list": avg_baseline_consumption,
        "baseline": np.mean(avg_baseline_consumption),
    }
