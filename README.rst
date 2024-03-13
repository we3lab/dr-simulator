Welcome to Demand Response Events Simulator
===========================================

|Build Status| |Documentation| |Coverage|

Incentive based Demand Response programs are voluntary programs offered to residential, 
commercial, and industrial customer. The participants are offered financial incentives 
if they voluntarily reduce loads during stressful times for the grid, which are notified 
as DR events. There are different flavors of these DR programs across the country, 
with different rules that constitute when the events are called, how often they are 
called, the duration of these calls and much more. The DR Simulator tool uses various 
program and simulation parameters to model these incentive-based demand response 
programs across the country. This enables the user to configure any DR programs from 
any ISOs and simulate DR events once they provide the simulation parameters based on 
historical distribution or based on a custom distribution.

--------------

Features
--------

-  Use custom or historic distribution

Quick Start
-----------

Installation
------------

**Stable Release:** ``pip install dr_simulator``\  **Development Head:**
``pip install git+https://github.com/we3lab/dr-simulator.git``

Documentation
-------------

For full package documentation please visit
`we3lab.github.io/dr-simulator <https://we3lab.github.io/dr-simulator>`__.

Development
-----------

See `CONTRIBUTING.md <CONTRIBUTING.md>`__ for information related to
developing the code.

The Commands You Need To Know
----------------------------------

1. ``pip install -e .[dev]``

   This will install your package in editable mode with all the required
   development dependencies (i.e. ``tox``).


Visualizing the DR Simulator using marimo notebook
--------------------------------------------------

You can visualize the DR Simulator using `marimo <https://github.com/marimo-team/marimo>`_ notebook. 

1. Install marimo using ``pip install marimo``

2. From the terminal, run ``marimo run dr_events_simulator.py``. This will open a new tab in your browser with the marimo notebook.

3. You can also run ``marimo edit dr_events_simulator.py`` to open the notebook in edit mode.


.. |Build Status| image:: https://github.com/we3lab/dr_simulator/workflows/Build%20Main/badge.svg
   :target: https://github.com/we3lab/dr-simulator/actions
.. |Documentation| image:: https://github.com/we3lab/dr_simulator/workflows/Documentation/badge.svg
   :target: https://we3lab.github.io/dr-simulator/
.. |Coverage| image:: https://codecov.io/gh/we3lab/dr-simulator/graph/badge.svg?token=HXGOYK8JCD
   :target: https://codecov.io/gh/we3lab/dr-simulator
