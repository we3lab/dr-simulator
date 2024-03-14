import marimo

__generated_with = "0.3.2"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
    ---------------------------------------------
    # Welcome to Demand Response Events Simulator
    ---------------------------------------------
        """
    )
    return


@app.cell
def __(mo):
    overview = mo.md(
        r"""

    ## Incentive Based DR Program: Overview
    ------------------------------------------

    Incentive based Demand Response programs are voluntary programs offered to residential, commercial, and industrial customer. The participants are offered financial incentives if they voluntarily reduce loads during stressful times for the grid, which are notified as DR events. There are different flavors of these DR programs across the country, with different rules that constitute when the events are called, how often they are called, the duration of these calls and much more. The DR Simulator tool uses various program and simulation parameters to model these incentive-based demand response programs across the country. This enables the user to configure any DR programs from any ISOs and simulate DR events once they provide the simulation parameters based on historical distribution or based on a custom distribution.
    """
    )

    how_to = mo.md(
        r"""
    ## How to use this package
    --------------------------

    Use this package to simulate any *incentive-based demand response* events for a custom distribution or distribution learned from historic demand response events.

    Essentially you need to set two types of parameters

    1. Program Parameters
    2. Simulation Parameters

    ### 1. Program Parameters

    These are the set of parameters that describes the DR program and its rules.

    | Parameter Name                | Definition                                                                                                   |
    |:------------------------------|:--------------------------------------------------------------------------------------------------------------|
    | Minimum number of event days | The minimum number of days the program event is called for a customer per month                                     |
    | Maximum number of event days | The maximum number of days the program event is called for a customer per month                                   |
    | Minimum duration of event    | The event should last for more than the minimum duration specified by the program                            |
    | Maximum duration of event    | The event should not last longer than the maximum duration specified by the program                          |
    | Program start time           | The program can be either 24 hours or last for a specified period of time, and the start time is generally provided if it is not a 24-hour period |
    | Program end time             | The program can be either 24 hours or last for a specified period of time, and the end time is generally provided if it is not a 24-hour period   |
    | Events per day               | The maximum event that a customer can provide on a single day.                                               |
    | Maximum consecutive event days | The maximum consecutive days the customer can be called in a particular month                               |
    | Notification type            | The event is generally notified the day before, or the day of and is captures by this parameter              |
    | Notification time            | If the event is notified the day before or the day of, the program generally specifies the time. Note: This can also be historic event related |
    | Number of similar weekdays   | The number of previous weekdays used to calculate the baseline                                               |


    ### 2. Simulation Parameters

    These parameters describes the likelihood of the DR event's number, duration and dates

    | Parameter Name     | Definition                                          | Distribution Type (default) | Distribution Parameters                              |
    |:---------------------|:----------------------------------------------------|:--------------------|:-------------------------------------------------------|
    | Number of days     | The number of event days given the time period    | Poisson            | $\lambda_{days}$ - mean number of days              |
    | Event duration     | The event duration for the DR events               | Poisson            | $\lambda_{dur}$ - mean duration of events           |
    | Start time         | Start time of the event                             | Uniform            | $\underline{T_s}$ - Program start time, $\bar{T_s}$ - Program end time |
    | Event days         | The probability of each day is selected            | Uniform            | $d \in D$, where D = Weekdays                        |

    ### Output

    After you populate both the parameter's values, you can simulate DR events for any given month & year. The output from a sample of a DR event would look like 

    | Event Date | Duration | Start Time | End Time | Notification Time | Similar Weekdays |
    |------------|----------|------------|----------|-------------------|------------------|
    | 2020-08-10 | 1        | 19:00      | 20:00    | 2020-08-09 17:00  | 2020-08-07, 2020-08-06,... |
    | 2020-08-12 | 3        | 17:00      | 20:00    | 2020-08-11 17:00  | 2020-08-11, 2020-08-07,... |
    | 2020-08-28 | 1        | 19:00      | 20:00    | 2020-08-27 17:00  | 2020-08-27, 2020-08-26,... |
    | 2020-08-31 | 3        | 17:00      | 20:00    | 2020-08-30 17:00  | 2020-08-27, 2020-08-26,... |

    (the above sample output is simulated from INSERT LINK program and simulation parameters)

    You can also generate *Monte-Carlo* samples by calling  `DemandResponseEvents.create_dr_events_mtcs` function.
    """
    )
    example = mo.md(
        r"""
    ## Example
    -----------

    To understand the tool more clearly let us look at the example of [**PG&E's Capacity Bidding Program**](https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_E-CBP.pdf)

    Based on the tariff structure, the program parameters for the PG&E CBP's Prescribed option are

    | Program Parameter              | Value       |
    |:-------------------------------|:------------|
    | Minimum number of event days  | 1           |
    | Maximum number of event days  | 6           |
    | Minimum duration of event     | 1           |
    | Maximum duration of event     | 8           |
    | Program start time            | 16          |
    | Program end time              | 20          |
    | Notification type             | day_before  |
    | Notification time             | 17          |
    | Maximum consecutive event days| 3           |
    | Number of similar weekdays    | 10          |

    You can also change the program parameters according to your preference. 
        """
    )

    mo.accordion({"Overview": overview, "How to use": how_to, "Example": example})
    return example, how_to, overview


@app.cell
def __(mo):
    mo.md(
        r"""
    ### Step 1: Select the month and year you want to simulate the DR events
    """
    )
    return


@app.cell
def __(dt, mo):
    month_dict = {dt.date(2021, i, 1).strftime("%B"): i for i in range(1, 13)}
    year_dict = {dt.date(i, 1, 1).strftime("%Y"): i for i in range(2019, 2023)}
    sim_month = mo.ui.dropdown(options=month_dict, label="Month", value="May")
    sim_year = mo.ui.dropdown(options=year_dict, label="Year", value="2021")
    dispay_month = mo.left(mo.hstack([sim_month, sim_year]))
    dispay_month
    return dispay_month, month_dict, sim_month, sim_year, year_dict


@app.cell
def __(mo):
    mo.md(
        r""" 
        ### Step 2: Enter the Program Parameters
        """
    )
    return


@app.cell
def __(mo):
    min_days = mo.ui.number(
        start=1, stop=20, step=1, value=1, label="Minimum number of event days"
    )

    max_days = mo.ui.number(
        start=1, stop=20, step=1, value=6, label="Maximum number of event days"
    )

    min_duration = mo.ui.number(
        start=1, stop=24, step=1, value=1, label="Minimum duration of event"
    )

    max_duration = mo.ui.number(
        start=1, stop=24, step=1, value=8, label="Maximum duration of event"
    )

    program_start_time = mo.ui.number(
        start=0, stop=24, step=1, value=16, label="Program start time"
    )

    program_end_time = mo.ui.number(
        start=0, stop=24, step=1, value=20, label="Program end time"
    )

    notification_type = mo.ui.dropdown(
        options=["day_before", "day_of", "hour_before"],
        value="day_before",
        label="Notification type",
    )

    notification_time = mo.ui.number(
        start=0, stop=24, step=1, value=17, label="Notification time"
    )

    max_consecutive_event_days = mo.ui.number(
        start=1, stop=31, step=1, value=3, label="Maximum consecutive event days"
    )

    number_similar_weekdays = mo.ui.number(
        start=1, stop=20, step=1, value=10, label="Number of similar weekdays"
    )
    program_parameter_form = (
        mo.md(
            """
    - {min_days}
    - {max_days}
    - {min_duration}
    - {max_duration}
    - {program_start_time}
    - {program_end_time}
    - {notification_type}
    - {notification_time}
    - {max_consecutive_event_days}
    - {number_similar_weekdays}

    """
        )
        .batch(
            min_days=min_days,
            max_days=max_days,
            min_duration=min_duration,
            max_duration=max_duration,
            program_start_time=program_start_time,
            program_end_time=program_end_time,
            notification_type=notification_type,
            notification_time=notification_time,
            max_consecutive_event_days=max_consecutive_event_days,
            number_similar_weekdays=number_similar_weekdays,
        )
        .form(show_clear_button=False, bordered=False)
    )
    program_parameter_form
    return (
        max_consecutive_event_days,
        max_days,
        max_duration,
        min_days,
        min_duration,
        notification_time,
        notification_type,
        number_similar_weekdays,
        program_end_time,
        program_parameter_form,
        program_start_time,
    )


@app.cell
def __(mo, program_parameter_form):
    mo.stop(
        program_parameter_form.value is None, mo.md("**Submit the form to continue.**")
    )
    return


@app.cell
def __(mo):
    mo.md(
        r""" 
        ### Step 3: Enter the Simulation Parameters
        """
    )
    return


@app.cell
def __(DistributionTypes, mo):
    ndays_distr_type = mo.ui.dropdown(
        options=[d.value for d in DistributionTypes],
        value=DistributionTypes.POISSON.value,
    )
    event_duration_distr_type = mo.ui.dropdown(
        options=[d.value for d in DistributionTypes],
        value=DistributionTypes.POISSON.value,
    )
    start_time_distr_type = mo.ui.dropdown(
        options=[d.value for d in DistributionTypes],
        value=DistributionTypes.UNIFORM.value,
    )
    mo.md(
        f"""
    Select the distribution types for

    - Number of days {ndays_distr_type}
    - Event Duration {event_duration_distr_type}
    - Start time {start_time_distr_type}

        """
    )
    return (
        event_duration_distr_type,
        ndays_distr_type,
        start_time_distr_type,
    )


@app.cell
def __(
    DistributionTypes,
    event_duration_distr_type,
    mo,
    ndays_distr_type,
    start_time_distr_type,
    ut,
):
    ndays_distr_param = mo.ui.text(placeholder="ndays param", value="3")
    event_duration_distr_param = mo.ui.text(
        placeholder="event_duration param", value="4"
    )
    start_time_distr_param = mo.ui.text(placeholder="start_time param", value="16, 21")
    mo.md(
        f"""
    Enter the distribution parameter of the simulation
    (if the distribution needs more than one values seperate them by comma)

    - Number of days ( {ut.distr_param_mapping[DistributionTypes(ndays_distr_type.value)]} ) {ndays_distr_param}
    - Event Duration ( {ut.distr_param_mapping[DistributionTypes(event_duration_distr_type.value)]} ) {event_duration_distr_param}
    - Start Time param ( {ut.distr_param_mapping[DistributionTypes(start_time_distr_type.value)]} ) {start_time_distr_param}
    """
    )
    return (
        event_duration_distr_param,
        ndays_distr_param,
        start_time_distr_param,
    )


@app.cell
def __(
    DistributionTypes,
    event_duration_distr_param,
    event_duration_distr_type,
    mo,
    ndays_distr_param,
    ndays_distr_type,
    start_time_distr_param,
    start_time_distr_type,
    ut,
):
    try:
        ndays_distr_param_val = ut.text_to_param_dict(
            DistributionTypes(ndays_distr_type.value), ndays_distr_param.value
        )
        event_duration_distr_param_val = ut.text_to_param_dict(
            DistributionTypes(event_duration_distr_type.value),
            event_duration_distr_param.value,
        )
        start_time_distr_param_val = ut.text_to_param_dict(
            DistributionTypes(start_time_distr_type.value), start_time_distr_param.value
        )
    except ValueError as exec:
        mo.output.replace(mo.callout(exec, kind="danger"))
    return (
        event_duration_distr_param_val,
        ndays_distr_param_val,
        start_time_distr_param_val,
    )


@app.cell
def __(
    event_duration_distr_param_val,
    event_duration_distr_type,
    ndays_distr_param_val,
    ndays_distr_type,
    program_parameter_form,
    start_time_distr_param_val,
    start_time_distr_type,
):
    simulation_parameters = {
        "n_days": {
            "distribution": ndays_distr_type.value,
            "distribution_parameters": ndays_distr_param_val,
        },
        "event_duration": {
            "distribution": event_duration_distr_type.value,
            "distribution_parameters": event_duration_distr_param_val,
        },
        "start_time": {
            "distribution": start_time_distr_type.value,
            "distribution_parameters": start_time_distr_param_val,
        },
        "event_days": {"p_dates": None},
    }
    program_parameters = program_parameter_form.value
    return program_parameters, simulation_parameters


@app.cell
def __(
    dr_eve,
    end_dt,
    plot_dr_events,
    plt,
    program_parameters,
    simulation_parameters,
    start_dt,
):
    dr_events = dr_eve(start_dt=start_dt, end_dt=end_dt, name="PG&E CBP May 2021")
    event_dict = dr_events.generate_event_dict(
        program_parameters=program_parameters,
        simulation_parameters=simulation_parameters,
    )
    fig, ax, cbar = plot_dr_events(
        start_dt, end_dt, dr_events.event_days, dr_events.event_duration
    )
    plt.gca()
    return ax, cbar, dr_events, event_dict, fig


@app.cell
def __(simulation_parameters):
    print(simulation_parameters)
    return


@app.cell
def __(dt, sim_month, sim_year, ut):
    start_dt = dt.datetime(sim_year.value, sim_month.value, 1, 0, 0, 0)
    sim_start_dt = start_dt - dt.timedelta(days=13)
    end_dt = dt.datetime(
        sim_year.value,
        sim_month.value,
        ut.days_in_year_month(sim_year.value, sim_month.value),
        0,
        0,
        0,
    )
    sim_end_dt = end_dt + dt.timedelta(days=2)
    return end_dt, sim_end_dt, sim_start_dt, start_dt


@app.cell
def __():
    import marimo as mo
    import datetime as dt
    import matplotlib.pyplot as plt
    from dr_simulator.dr_events import DemandResponseEvents as dr_eve
    from dr_simulator.visulization_helper import plot_dr_events
    from dr_simulator import utils as ut
    from dr_simulator.utils import DistributionTypes
    return DistributionTypes, dr_eve, dt, mo, plot_dr_events, plt, ut


if __name__ == "__main__":
    app.run()
