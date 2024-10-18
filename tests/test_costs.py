""" 
Tests for functions for `costs.py` module of the `dr_simulator` package.
"""

import os
import pytest
import pandas as pd

from dr_simulator import costs
from dr_simulator import utils as ut
from dr_simulator import data


os.chdir(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = "data/input/"

SKIP_ALL_TESTS = False  # Set to True to skip all tests


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "event_data",
        "output_data",
        "electricity_purchase_varnames",
        "datetime_varname",
        "day_of_adj_bool",
        "day_of_adj_max",
        "expected",
    ),
    [
        (
            ut.sanitize_dr_data(ut.json_load("data/input/dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            False,
            0,
            {
                "payment_list": [2352.0, 2352.0],
                "payment": 4704.0,
                "ratio_list": [3.778084881288042, 3.9774409459309994],
                "ratio": 3.8,
                "reduction_list": [377.8084881288042, 397.74409459309993],
                "reduction": 387.7,
                "baseline_list": [627.8084881288069, 647.7440945931025],
                "baseline": 637.7,
            },
        ),
        (
            ut.sanitize_dr_data(ut.json_load("data/input/dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            True,
            0.4,
            {
                "payment_list": [2352.0, 2352.0],
                "payment": 4704.0,
                "ratio_list": [5.519352242961088, 3.9774409459309994],
                "ratio": 4.7,
                "reduction_list": [551.9352242961088, 397.74409459309993],
                "reduction": 473.7,
                "baseline_list": [801.9352242961114, 647.7440945931025],
                "baseline": 723.7,
            },
        ),
    ],
)
def test_calculate_dr_payment(
    event_data,
    output_data,
    electricity_purchase_varnames,
    datetime_varname,
    day_of_adj_bool,
    day_of_adj_max,
    expected,
):
    """ 
    Test for the `calculate_dr_payment` function in the `costs.py` module.

    Parameters
    ----------
    event_data : dict
        Dictionary with the details of the demand response event

    output_data : str
        Path to the output data file

    electricity_purchase_varnames : list
        List of electricity purchase variable names

    datetime_varname : str
        Name of the datetime variable in the output data

    day_of_adj_bool : bool
        Boolean indicating whether to use day-of-adjustment

    day_of_adj_max : float
        Maximum day-of-adjustment value

    expected : dict
        Dictionary

    """

    output_data = pd.read_csv(output_data)
    output_data[datetime_varname] = pd.to_datetime(output_data[datetime_varname])

    if day_of_adj_bool:
        event_data[data.DR_DAY_OF_ADJUSTMENT_KEY]["maximum"] = day_of_adj_max
    else:
        event_data[data.DR_DAY_OF_ADJUSTMENT_KEY] = {}

    event_data = ut.sanitize_dr_data(event_data)
    event_data[data.DR_EVENTS_PERIODS_KEY] = ut.get_dr_dates(
        event_data[data.DR_EVENT_DETAILS_KEY],
        output_data[datetime_varname].values[0],
        output_data[datetime_varname].values[-1],
    )
    capacity_bid = event_data[data.DR_CAPACITY_BID_KEY]["value"]
    capacity_price = event_data[data.DR_CAPACITY_PRICE_KEY]["value"]
    payment_function = event_data[data.DR_PAYMENT_FUNCTION_KEY]

    first_event_period = list(event_data[data.DR_EVENTS_PERIODS_KEY].values())[0]

    print("first_event_period", first_event_period)

    result = costs.calculate_dr_payment(
        first_event_period,
        capacity_bid,
        capacity_price,
        payment_function,
        output_data,
        electricity_purchase_varnames,
        datetime_varname,
        event_data[data.DR_DAY_OF_ADJUSTMENT_KEY],
    )
    print("result", result)
    for key, value in expected.items():
        assert value == pytest.approx(result[key], 0.1)


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "event_data",
        "output_data",
        "electricity_purchase_varnames",
        "datetime_varname",
        "day_of_adj_bool",
        "day_of_adj_max",
        "expected",
    ),
    [
        (
            ut.sanitize_dr_data(ut.json_load("data/input/dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            False,
            0,
            [
                {
                    "payment_list": [2352.0, 2352.0],
                    "payment": 4704.0,
                    "ratio_list": [3.78, 3.98],
                    "ratio": 3.88,
                    "reduction_list": [377.81, 397.74],
                    "reduction": 387.78,
                    "baseline_list": [627.81, 647.74],
                    "baseline": 637.78,
                },
                {
                    "payment_list": [2352.0, -1344.0, -949.78, 2352.0],
                    "payment": 2410.22,
                    "ratio_list": [3.46, -0.01, 0.18, 1.05],
                    "ratio": 1.17,
                    "reduction_list": [346.48, -0.73, 17.6, 105.0],
                    "reduction": 117.09,
                    "baseline_list": [596.48, 609.48, 627.81, 647.74],
                    "baseline": 620.38,
                },
                {
                    "payment_list": [2352.0, -1344.0, 1120.0],
                    "payment": 2128.0,
                    "ratio_list": [1.68, -0.44, 0.65],
                    "ratio": 0.63,
                    "reduction_list": [168.08, -44.25, 65.34],
                    "reduction": 63.06,
                    "baseline_list": [577.23, 588.57, 604.45],
                    "baseline": 590.08,
                },
                {
                    "payment_list": [2352.0, -1344.0, -1213.22, 2352.0],
                    "payment": 2146.78,
                    "ratio_list": [2.83, -0.16, 0.06, 1.05],
                    "ratio": 0.95,
                    "reduction_list": [283.33, -15.74, 5.84, 105.0],
                    "reduction": 94.61,
                    "baseline_list": [578.24, 597.0, 618.58, 614.53],
                    "baseline": 602.09,
                },
            ],
        ),
        (
            ut.sanitize_dr_data(ut.json_load("data/input/dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            True,
            0.4,
            [
                {
                    'payment_list': [2352.0, 2352.0],
                    'payment': 4704.0,
                    'ratio_list': [5.52, 3.98],
                    'ratio': 4.75,
                    'reduction_list': [551.94, 397.74],
                    'reduction': 474.84,
                    'baseline_list': [801.94, 647.74],
                    'baseline': 724.84
                },
                {
                    'payment_list': [2352.0, -1344.0, -949.78, 2352.0],
                    'payment': 2410.22,
                    'ratio_list': [5.05, -0.01, 0.18, 1.05],
                    'ratio': 1.57,
                    'reduction_list': [505.0, -0.73, 17.6, 105.0],
                    'reduction': 156.72,
                    'baseline_list': [755.0, 609.48, 627.81, 647.74],
                    'baseline': 660.01
                },
                {
                    'payment_list': [2352.0, -1344.0, 1120.0],
                    'payment': 2128.0,
                    'ratio_list': [3.93, -0.44, 0.65],
                    'ratio': 1.38,
                    'reduction_list': [393.02, -44.25, 65.34],
                    'reduction': 138.04,
                    'baseline_list': [802.18, 588.57, 604.45],
                    'baseline': 665.07
                },
                {
                    'payment_list': [2352.0, -1344.0, -1213.22, 2352.0],
                    'payment': 2146.78,
                    'ratio_list': [4.68, -0.16, 0.06, 1.05],
                    'ratio': 1.41,
                    'reduction_list': [468.1, -15.74, 5.84, 105.0],
                    'reduction': 140.8,
                    'baseline_list': [763.02, 597.0, 618.58, 614.53],
                    'baseline': 648.28
                }
            ]
        )
    ],
)
def test_calculate_dr_payments(
    event_data,
    output_data,
    electricity_purchase_varnames,
    datetime_varname,
    day_of_adj_bool,
    day_of_adj_max,
    expected,
):
    """
    Test for the `calculate_dr_payments` function in the `costs.py` module.

    Parameters
    ----------
    event_data : dict
        Dictionary with the details of the demand response event

    output_data : str
        Path to the output data file

    electricity_purchase_varnames : list
        List of electricity purchase variable names

    datetime_varname : str
        Name of the datetime variable in the output data

    day_of_adj_bool : bool
        Boolean indicating whether to use day-of-adjustment

    day_of_adj_max : float
        Maximum day-of-adjustment value

    expected : dict
        Dictionary

    """
    output_data = pd.read_csv(output_data)
    output_data[datetime_varname] = pd.to_datetime(output_data[datetime_varname])

    event_data = ut.sanitize_dr_data(event_data)
    event_data[data.DR_EVENTS_PERIODS_KEY] = ut.get_dr_dates(
        event_data[data.DR_EVENT_DETAILS_KEY],
        output_data[datetime_varname].values[0],
        output_data[datetime_varname].values[-1],
    )
    capacity_bid = event_data[data.DR_CAPACITY_BID_KEY]["value"]
    capacity_price = event_data[data.DR_CAPACITY_PRICE_KEY]["value"]
    payment_function = event_data[data.DR_PAYMENT_FUNCTION_KEY]

    if day_of_adj_bool:
        event_data[data.DR_DAY_OF_ADJUSTMENT_KEY]["maximum"] = day_of_adj_max
    else:
        event_data[data.DR_DAY_OF_ADJUSTMENT_KEY] = {}

    results = []
    for dr_event_period in event_data[data.DR_EVENTS_PERIODS_KEY].values():
        result = costs.calculate_dr_payment(
            dr_event_period,
            capacity_bid,
            capacity_price,
            payment_function,
            output_data,
            electricity_purchase_varnames,
            datetime_varname,
            event_data[data.DR_DAY_OF_ADJUSTMENT_KEY],
        )
        results.append(result)
    for i, result in enumerate(results):
        for key, value in expected[i].items():
            if isinstance(value, list):
                for j, val in enumerate(value):
                    assert val == pytest.approx(result[key][j], 0.4)
            else:
                assert value == pytest.approx(result[key], rel=0.1)
