import marimo

__generated_with = "0.3.2"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo

    from dr_simulator.dr_events import DemandResponseEvents as dr_eve
    return dr_eve, mo


@app.cell
def __(mo):
    mo.md(
        r"""
    ---------------------------------------------
    # Welcome to Demand Response Events Simulator
    ---------------------------------------------

    ## Incentive Based DR Program: Overview
    ------------------------------------------

    Incentive based Demand Response programs are voluntary programs offered to residential, commercial, and industrial customer. The participants are offered financial incentives if they voluntarily reduce loads during stressful times for the grid, which are notified as DR events. There are different flavors of these DR programs across the country, with different rules that constitute when the events are called, how often they are called, the duration of these calls and much more. The DR Simulator tool uses various program and simulation parameters to model these incentive-based demand response programs across the country. This enables the user to configure any DR programs from any ISOs and simulate DR events once they provide the simulation parameters based on historical distribution or based on a custom distribution.

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

    You can also change the program parameters according to what you 

        """
    )
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
