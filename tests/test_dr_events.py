#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the `dr_events` module of the `dr_simulator` package.

Docs: https://docs.pytest.org/en/latest/
      https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery
"""

import os
from datetime import datetime as dt
import numpy as np
import pytest
from dr_simulator.dr_events import DemandResponseEvents
from dr_simulator import utils

SKIP_ALL_TESTS = False # Set to True to skip all tests

INPUT_DIR = "./data/input/"
OUTPUT_DIR = "./data/output/"

# Change working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    "start_dt, end_dt, name, time_step, program_parameters, expected",
    [
        (
            "5-1-21",
            "5-31-21",
            "test_program",
            60,
            "dr_program_parameters.json",
            "dr_program_parameters.json",
        ),
    ],
)
def test_set_program_paramters(start_dt, end_dt, name, time_step, program_parameters, expected):
    start_dt = dt.strptime(start_dt, "%m-%d-%y")
    end_dt = dt.strptime(end_dt, "%m-%d-%y")
    program_parameters = utils.json_load(INPUT_DIR + program_parameters)
    expected = utils.json_load(INPUT_DIR + expected)
    dr = DemandResponseEvents(start_dt, end_dt, name, time_step)
    dr.set_program_parameters(**program_parameters)
    for key, value in expected.items():
        assert getattr(dr, key) == value

@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    "start_dt, end_dt, name, time_step, program_parameters, seed, distribution, distribution_parameters, expected",
    [
        (
            "5-1-21",
            "5-31-21",
            "test_program",
            60,
            "dr_program_parameters.json",
            12345,
            "poisson",
            {
                "lam": 3
            },
            3,
        ),
    ],
)
def test_set_ndays(start_dt, end_dt, name, time_step, program_parameters, seed, distribution, distribution_parameters, expected):
    start_dt = dt.strptime(start_dt, "%m-%d-%y")
    end_dt = dt.strptime(end_dt, "%m-%d-%y")
    program_parameters = utils.json_load(INPUT_DIR + program_parameters)
    dr = DemandResponseEvents(start_dt, end_dt, name, time_step)
    dr.set_program_parameters(**program_parameters)
    dr.set_ndays(seed=seed, distribution=distribution, distribution_parameters=distribution_parameters)
    assert dr.ndays == expected

@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    "start_dt, end_dt, name, time_step, program_parameters, simulation_parameters, expected",
    [
        (
            "5-1-21",
            "5-31-21",
            "test_program",
            60,
            "dr_program_parameters.json",
            "dr_simulation_parameters.json",
            [16, 17, 19],
        ),
    ],
)
def test_set_start_times(start_dt, end_dt, name, time_step, program_parameters, simulation_parameters, expected):
    start_dt = dt.strptime(start_dt, "%m-%d-%y")
    end_dt = dt.strptime(end_dt, "%m-%d-%y")
    program_parameters = utils.json_load(INPUT_DIR + program_parameters)
    simulation_parameters = utils.json_load(INPUT_DIR + simulation_parameters)
    dr = DemandResponseEvents(start_dt, end_dt, name, time_step)
    dr.set_program_parameters(**program_parameters)
    dr.set_ndays(**simulation_parameters["n_days"])
    dr.set_start_times(**simulation_parameters["start_time"])
    assert np.allclose(dr.start_times, expected)

@pytest.mark.skipif(SKIP_ALL_TESTS, reason="Exclude all tests")
@pytest.mark.parametrize(
    "start_dt, end_dt, name, time_step, program_parameters, simulation_parameters, expected",
    [
        (
            "5-1-21",
            "5-31-21",
            "test_program_1",
            60,
            "dr_program_parameters.json",
            "dr_simulation_parameters.json",
            "dr_program_events_1.pkl",
        ),
        (
            "6-1-22",
            "6-30-22",
            "test_program_2",
            60,
            "dr_program_parameters.json",
            "dr_simulation_parameters.json",
            "dr_program_events_2.pkl",
        ),
    ],
)
def test_simulating_dr_events(start_dt, end_dt, name, time_step, program_parameters, simulation_parameters, expected):
    start_dt = dt.strptime(start_dt, "%m-%d-%y")
    end_dt = dt.strptime(end_dt, "%m-%d-%y")
    program_parameters = utils.json_load(INPUT_DIR + program_parameters)
    simulation_parameters = utils.json_load(INPUT_DIR + simulation_parameters)
    dr = DemandResponseEvents(start_dt, end_dt, name, time_step)
    event_dict = dr.generate_event_dict(program_parameters, simulation_parameters)
    expected = utils.pickle_load(OUTPUT_DIR + expected)
    assert event_dict == expected
