Demand Response Simulator
=========================

|Build Status| |Documentation| |Coverage|

Demand Response Simulator enables you to sample DR events based on
historic or custom distribution and optimize your energy flexible
process

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
-------------------------------------------------

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
