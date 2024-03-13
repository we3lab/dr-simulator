How to use the Demand Response Simulator Tool
=============================================

How to use this package
------------------------

Use this package to simulate any *incentive-based demand response* events for a custom distribution or distribution learned from historic demand response events.

Essentially you need to set two types of parameters

1. Program Parameters
2. Simulation Parameters

1. Program Parameters
^^^^^^^^^^^^^^^^^^^^^

These are the set of parameters that describes the DR program and its rules.

.. csv-table:: Program Parameters
   :file: ../data/metadata/program_parameters.csv

1. Simulation Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

These parameters describes the likelihood of the DR event's number, duration and dates

.. csv-table:: Simulation Parameters
   :file: ../data/metadata/simulation_parameters.csv

Output
------

After you populate both the parameter's values, you can simulate DR events for any given month & year. The output from a sample of a DR event would look like 

.. csv-table:: Sample Output
   :file: ../data/sample_output.csv


(the above sample output is simulated from INSERT LINK program and simulation parameters)

You can also generate *Monte-Carlo* samples by calling  `DemandResponseEvents.create_dr_events_mtcs` function.
