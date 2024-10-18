""" 
Tests for functions for `utils.py` module of the `dr_simulator` package.

Docs: https://docs.pytest.org/en/latest/
      https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery
"""

import os
from datetime import datetime as dt
import numpy as np
import pandas as pd
import pytest

from dr_simulator import utils as ut
from dr_simulator import data


os.chdir(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = "data/input/"

SKIP_ALL_TESTS = False  # Set to True to skip all tests

BASELINE_DAYS_17 = np.array(
    [
        np.datetime64(dt(2020, 8, 14, 0, 0)),
        np.datetime64(dt(2020, 8, 13, 0, 0)),
        np.datetime64(dt(2020, 8, 12, 0, 0)),
        np.datetime64(dt(2020, 8, 11, 0, 0)),
        np.datetime64(dt(2020, 8, 10, 0, 0)),
        np.datetime64(dt(2020, 8, 7, 0, 0)),
        np.datetime64(dt(2020, 8, 6, 0, 0)),
        np.datetime64(dt(2020, 8, 5, 0, 0)),
        np.datetime64(dt(2020, 8, 4, 0, 0)),
        np.datetime64(dt(2020, 8, 3, 0, 0)),
    ],
    dtype="datetime64[s]",
)

BASELINE_DAYS_18 = BASELINE_DAYS_17

BASELINE_DAYS_25 = np.array(
    [
        np.datetime64(dt(2020, 8, 24, 0, 0)),
        np.datetime64(dt(2020, 8, 21, 0, 0)),
        np.datetime64(dt(2020, 8, 20, 0, 0)),
        np.datetime64(dt(2020, 8, 19, 0, 0)),
        np.datetime64(dt(2020, 8, 14, 0, 0)),
        np.datetime64(dt(2020, 8, 13, 0, 0)),
        np.datetime64(dt(2020, 8, 12, 0, 0)),
        np.datetime64(dt(2020, 8, 11, 0, 0)),
        np.datetime64(dt(2020, 8, 10, 0, 0)),
        np.datetime64(dt(2020, 8, 7, 0, 0)),
    ],
    dtype="datetime64[s]",
)

BASELINE_DAYS_31 = np.array(
    [
        np.datetime64(dt(2020, 8, 28, 0, 0)),
        np.datetime64(dt(2020, 8, 27, 0, 0)),
        np.datetime64(dt(2020, 8, 26, 0, 0)),
        np.datetime64(dt(2020, 8, 24, 0, 0)),
        np.datetime64(dt(2020, 8, 21, 0, 0)),
        np.datetime64(dt(2020, 8, 20, 0, 0)),
        np.datetime64(dt(2020, 8, 19, 0, 0)),
        np.datetime64(dt(2020, 8, 14, 0, 0)),
        np.datetime64(dt(2020, 8, 13, 0, 0)),
        np.datetime64(dt(2020, 8, 12, 0, 0)),
    ],
    dtype="datetime64[s]",
)


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "similar_days",
        "event_hour",
        "output_data",
        "electricity_purchase_varnames",
        "datetime_varname",
        "expected_baseline",
    ),
    [
        pytest.param(
            BASELINE_DAYS_17,
            19,
            INPUT_DIR + "baseline_data_ww_dr_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            627.8,
            id="test_ww",
        ),
        pytest.param(
            BASELINE_DAYS_17,
            19,
            INPUT_DIR + "baseline_data_batt_dr_08_2020.csv",
            [
                "PowerGrid_SVCW_VirtualDemand_Electricity_Flow",
                "PowerGrid_SVCW_TeslaPowerpack_Electricity_Flow",
            ],
            "DateTime",
            717.2,
            id="test_batt",
        ),
        pytest.param(
            BASELINE_DAYS_17,
            19,
            INPUT_DIR + "baseline_data_gas_dr_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            619.2,
            id="test_gas",
        ),
        pytest.param(
            BASELINE_DAYS_17,
            [19, 20],
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            637.7,
            id="test_dr_payment",
        ),
    ],
)
def test_get_hourly_average_consumption(
    similar_days,
    event_hour,
    output_data,
    electricity_purchase_varnames,
    datetime_varname,
    expected_baseline,
):
    """Test function for get_hourly_average_consumption,"""
    # Load data
    output_data = pd.read_csv(output_data)
    output_data[datetime_varname] = pd.to_datetime(output_data[datetime_varname])

    # Get the baseline consumption
    if isinstance(event_hour, int):
        baseline = ut.get_hourly_average_consumption(
            similar_days,
            event_hour,
            output_data,
            electricity_purchase_varnames,
            datetime_varname,
        )
    elif isinstance(event_hour, list):
        baseline = []
        for hour in event_hour:
            baseline.append(
                ut.get_hourly_average_consumption(
                    similar_days,
                    hour,
                    output_data,
                    electricity_purchase_varnames,
                    datetime_varname,
                )
            )
        baseline = np.mean(baseline)

    assert baseline == pytest.approx(expected_baseline, 0.1)


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "dr_event_data",
        "output_data_path",
        "electricity_purchase_varnames",
        "datetime_varname",
        "day_of_adj_max",
        "day_of_adj_window",
        "expected",
    ),
    [
        pytest.param(
            ut.sanitize_dr_data(ut.json_load(INPUT_DIR + "dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            0.4,
            3,
            0.27,
            id="test_ww_1",
        ),
        pytest.param(
            ut.sanitize_dr_data(ut.json_load(INPUT_DIR + "dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            0.2,
            3,
            0.2,
            id="test_ww_2",
        ),
        pytest.param(
            ut.sanitize_dr_data(ut.json_load(INPUT_DIR + "dr_events_08_2020.json")),
            INPUT_DIR + "output_data_dr_ww_08_2020.csv",
            ["PowerGrid_SVCW_VirtualDemand_Electricity_Flow"],
            "DateTime",
            0.4,
            2,
            0.4,
            id="test_ww_3",
        ),
    ],
)
def test_get_day_of_adj_ratio(
    dr_event_data,
    output_data_path,
    electricity_purchase_varnames,
    datetime_varname,
    day_of_adj_max,
    day_of_adj_window,
    expected,
):
    """Test function for get_day_of_adj_ratio,"""
    # Load data
    output_data = pd.read_csv(output_data_path)
    output_data[datetime_varname] = pd.to_datetime(output_data[datetime_varname])

    dr_event_data[data.DR_EVENTS_PERIODS_KEY] = ut.get_dr_dates(
        dr_event_data[data.DR_EVENT_DETAILS_KEY],
        output_data[datetime_varname].values[0],
        output_data[datetime_varname].values[-1],
    )

    first_event_period = list(dr_event_data[data.DR_EVENTS_PERIODS_KEY].values())[0]

    # Load event details
    dr_event_data[data.DR_DAY_OF_ADJUSTMENT_KEY] = {
        "maximum": day_of_adj_max,
        "hours before": 4,
        "duration": day_of_adj_window,
    }

    # Get the day of adjustment ratio
    result = ut.get_day_of_adj_ratio(
        first_event_period,
        output_data,
        electricity_purchase_varnames,
        datetime_varname,
        dr_event_data[data.DR_DAY_OF_ADJUSTMENT_KEY],
    )
    assert result == pytest.approx(expected, 0.1)


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "dr_event_path",
        "expected",
    ),
    [
        pytest.param(
            INPUT_DIR + "dr_events_08_2020.json",
            {
                "name": "PG&E CBP",
                "reduction compensation": {"value": 22.4, "parametrize": False},
                "reduction capacity": {"value": 100, "parametrize": False},
                "day of adjustment": {"maximum": 0.4, "hours before": 4, "duration": 3},
                "payment function": [
                    {"domain": [1.05, None], "slope": 0, "intercept": 1.05},
                    {"domain": [0.75, 1.05], "slope": 1, "intercept": 0},
                    {"domain": [0.6, 0.75], "slope": 0, "intercept": 0.5},
                    {"domain": [0, 0.6], "slope": 1, "intercept": -0.6},
                    {"domain": [None, 0], "slope": 0, "intercept": -0.6},
                ],
                "events detail": [
                    {
                        "year": 2020,
                        "month": 8,
                        "day": 17,
                        "duration": 2,
                        "start_time": 19,
                        "baseline days": BASELINE_DAYS_17,
                    },
                    {
                        "year": 2020,
                        "month": 8,
                        "day": 18,
                        "duration": 4,
                        "start_time": 17,
                        "baseline days": BASELINE_DAYS_18,
                    },
                    {
                        "year": 2020,
                        "month": 8,
                        "day": 25,
                        "duration": 3,
                        "start_time": 17,
                        "baseline days": BASELINE_DAYS_25,
                    },
                    {
                        "year": 2020,
                        "month": 8,
                        "day": 31,
                        "duration": 4,
                        "start_time": 17,
                        "baseline days": BASELINE_DAYS_31,
                    },
                ],
            },
            id="test_ww",
        ),
    ],
)
def test_sanitize_dr_data(dr_event_path, expected):
    """Test function for sanitize_dr_data,"""
    # Load event details
    dr_data = ut.json_load(dr_event_path)
    dr_data = ut.sanitize_dr_data(dr_data)

    for key in expected:
        assert key in dr_data

    for key in dr_data:
        assert key in expected

    for i, event_detail in enumerate(dr_data["events detail"]):
        expected_event_detail = expected["events detail"][i]

        for key in event_detail:
            assert key in expected_event_detail

        for key in expected_event_detail:
            assert key in event_detail

        assert np.array_equal(
            event_detail["baseline days"], expected_event_detail["baseline days"]
        )
        assert event_detail["year"] == expected_event_detail["year"]
        assert event_detail["month"] == expected_event_detail["month"]
        assert event_detail["day"] == expected_event_detail["day"]
        assert event_detail["start_time"] == expected_event_detail["start_time"]
        assert event_detail["duration"] == expected_event_detail["duration"]


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "event_detail",
        "expected",
    ),
    [
        pytest.param(
            {
                "year": 2020,
                "month": 8,
                "day": 17,
                "duration": "2",
                "start_time": "19",
                "baseline days": [
                    "2020-08-14 00:00:00",
                    "2020-08-13 00:00:00",
                    "2020-08-12 00:00:00",
                    "2020-08-11 00:00:00",
                    "2020-08-10 00:00:00",
                    "2020-08-07 00:00:00",
                    "2020-08-06 00:00:00",
                    "2020-08-05 00:00:00",
                    "2020-08-04 00:00:00",
                    "2020-08-03 00:00:00",
                ],
            },
            {
                "year": 2020,
                "month": 8,
                "day": 17,
                "duration": 2,
                "start_time": 19,
                "baseline days": BASELINE_DAYS_17,
            },
        )
    ],
)
def test_convert_dr_event_details(event_detail, expected):
    """Test function for convert_dr_event_details,"""
    result = ut.convert_dr_event_details(event_detail)
    for key in expected:
        assert key in result


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "event_start_dt",
        "horizon_start_dt",
        "horizon_end_dt",
        "resolution",
    ),
    [
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 17, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            "15m",
            id="test_15m_2020_01_01_17_00",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 15, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            "15m",
            id="test_15m_2020_01_01_15_00",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 15, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            "1h",
            id="test_1h_2020_01_01_15_00",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 3, 15, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            "1h",
            id="test_1h_2020_01_03_15_00",
        ),
    ],
)
def test_get_hourly_dr_event_arrays(
    event_start_dt, horizon_start_dt, horizon_end_dt, resolution, request
):
    """Test function for get_hourly_dr_event_arrays,"""
    result = ut.get_hourly_dr_event_arrays(
        event_start_dt, horizon_start_dt, horizon_end_dt, resolution
    )
    test_id = request.node.callspec.id
    expected = np.array(
        ut.json_load(f"data/output/hourly_dr_event_arrays_{test_id}.json")
    )
    assert np.array_equal(result, expected)


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "dr_data",
        "horizon_start_dt",
        "horizon_end_dt",
        "expected",
    ),
    [
        pytest.param(
            ut.sanitize_dr_data(ut.json_load(INPUT_DIR + "dr_events_08_2020.json")),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            {},
            id="test_no_events",
        ),
        pytest.param(
            ut.sanitize_dr_data(ut.json_load(INPUT_DIR + "dr_events_08_2020.json")),
            np.datetime64(dt(2020, 8, 1, 0, 0)),
            np.datetime64(dt(2020, 8, 30, 0, 0)),
            {
                "event_0": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-17T19:00:00.000000"),
                            np.datetime64("2020-08-17T21:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_17,
                },
                "event_1": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-18T17:00:00.000000"),
                            np.datetime64("2020-08-18T21:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_18,
                },
                "event_2": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-25T17:00:00.000000"),
                            np.datetime64("2020-08-25T20:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_25,
                },
            },
            id="test_3_events_in_horizon",
        ),
        pytest.param(
            ut.sanitize_dr_data(ut.json_load(INPUT_DIR + "dr_events_08_2020.json")),
            np.datetime64(dt(2020, 8, 1, 0, 0)),
            np.datetime64(dt(2020, 9, 1, 0, 0)),
            {
                "event_0": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-17T19:00:00.000000"),
                            np.datetime64("2020-08-17T21:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_17,
                },
                "event_1": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-18T17:00:00.000000"),
                            np.datetime64("2020-08-18T21:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_18,
                },
                "event_2": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-25T17:00:00.000000"),
                            np.datetime64("2020-08-25T20:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_25,
                },
                "event_3": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-08-31T17:00:00.000000"),
                            np.datetime64("2020-08-31T21:00:00.000000"),
                        ]
                    ),
                    "baseline days": BASELINE_DAYS_31,
                },
            },
            id="test_all_events_in_horizon",
        ),
        pytest.param(
            {
                "events detail": [
                    {
                        "day": 1,
                        "month": 1,
                        "year": 2020,
                        "duration": 1,
                        "start_time": 15,
                        "baseline days": np.array(
                            ["2020-01-02 00:00:00"], dtype="datetime64[s]"
                        ),
                    },
                    {
                        "day": 1,
                        "month": 1,
                        "year": 2020,
                        "duration": 2,
                        "start_time": 19,
                        "baseline days": np.array(
                            ["2020-01-02 00:00:00"], dtype="datetime64[s]"
                        ),
                    },
                ],
            },
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            {
                "event_0": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-01-01T15:00:00.000000"),
                            np.datetime64("2020-01-01T16:00:00.000000"),
                        ]
                    ),
                    "baseline days": np.array(
                        ["2020-01-02T00:00:00"], dtype="datetime64[s]"
                    ),
                },
                "event_1": {
                    "event_dts": np.array(
                        [
                            np.datetime64("2020-01-01T19:00:00.000000"),
                            np.datetime64("2020-01-01T21:00:00.000000"),
                        ]
                    ),
                    "baseline days": np.array(
                        ["2020-01-02T00:00:00"], dtype="datetime64[s]"
                    ),
                },
            },
            id="test_2_events_in_horizon",
        ),
    ],
)
def test_get_dr_dates(dr_data, horizon_start_dt, horizon_end_dt, expected):
    """Test function for get_dr_dates,"""
    events_detail = dr_data["events detail"]
    result = ut.get_dr_dates(events_detail, horizon_start_dt, horizon_end_dt)
    for key, value in result.items():
        assert key in expected
        assert np.array_equal(value["event_dts"], expected[key]["event_dts"])
        assert np.array_equal(value["baseline days"], expected[key]["baseline days"])


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "dr_data",
        "horizon_start_dt",
        "horizon_end_dt",
    ),
    [
        pytest.param(
            {
                "events detail": [
                    {
                        "day": 1,
                        "month": 1,
                        "year": 2020,
                        "duration": 3,
                        "start_time": 15,
                        "baseline days": np.array(
                            ["2020-01-02 00:00:00"], dtype="datetime64[s]"
                        ),
                    },
                    {
                        "day": 1,
                        "month": 1,
                        "year": 2020,
                        "duration": 2,
                        "start_time": 17,
                        "baseline days": np.array(
                            ["2020-01-02 00:00:00"], dtype="datetime64[s]"
                        ),
                    },
                ],
            },
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            id="test_overalap_events_in_horizon",
        ),
    ],
)
def test_get_dr_dates_overlap(dr_data, horizon_start_dt, horizon_end_dt):
    """Test function for get_dr_dates,"""
    events_detail = dr_data["events detail"]
    pytest.raises(
        ValueError, ut.get_dr_dates, events_detail, horizon_start_dt, horizon_end_dt
    )


@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    (
        "dr_start_dt",
        "dr_end_dt",
        "horizon_start_dt",
        "horizon_end_dt",
        "expected",
    ),
    [
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 3, 0, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            (np.datetime64(dt(2020, 1, 1, 0, 0)), np.datetime64(dt(2020, 1, 2, 0, 0))),
            id="test_horizon_in_dr",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 17, 0)),
            np.datetime64(dt(2020, 1, 1, 19, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            (
                np.datetime64(dt(2020, 1, 1, 17, 0)),
                np.datetime64(dt(2020, 1, 1, 19, 0)),
            ),
            id="test_dr_in_horizon",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 1, 17, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            np.datetime64(dt(2020, 1, 3, 0, 0)),
            (None, None),
            id="dr_before_horizon",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 4, 0, 0)),
            np.datetime64(dt(2020, 1, 4, 17, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            np.datetime64(dt(2020, 1, 3, 0, 0)),
            (None, None),
            id="dr_after_horizon",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 17, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            np.datetime64(dt(2020, 1, 3, 0, 0)),
            (np.datetime64(dt(2020, 1, 2, 0, 0)), np.datetime64(dt(2020, 1, 2, 17, 0))),
            id="dr_start_not_in_horizon",
        ),
        pytest.param(
            np.datetime64(dt(2020, 1, 1, 17, 0)),
            np.datetime64(dt(2020, 1, 2, 17, 0)),
            np.datetime64(dt(2020, 1, 1, 0, 0)),
            np.datetime64(dt(2020, 1, 2, 0, 0)),
            (np.datetime64(dt(2020, 1, 1, 17, 0)), np.datetime64(dt(2020, 1, 2, 0, 0))),
            id="dr_end_not_in_horizon",
        ),
    ],
)
def test_get_start_end_dt(
    dr_start_dt, dr_end_dt, horizon_start_dt, horizon_end_dt, expected
):
    """Test function for get_start_end_dt,"""
    result = ut.get_start_end_dt(
        dr_start_dt, dr_end_dt, horizon_start_dt, horizon_end_dt
    )
    assert result == expected
