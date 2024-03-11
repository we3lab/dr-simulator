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

The Four Commands You Need To Know
----------------------------------

1. ``pip install -e .[dev]``

   This will install your package in editable mode with all the required
   development dependencies (i.e. ``tox``).

2. ``make build``

   This will run ``tox`` which will run all your tests in both Python
   3.7 and Python 3.8 as well as linting your code.

3. ``make clean``

   This will clean up various Python and build generated files so that
   you can ensure that you are working in a clean environment.

4. ``make docs``

   This will generate and launch a web browser to view the most
   up-to-date documentation for your Python package.

**MIT license**

Copyright (c) 2024, Adhithyan Sakthivelu

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. |Build Status| image:: https://github.com/we3lab/dr_simulator/workflows/Build%20Main/badge.svg
   :target: https://github.com/we3lab/dr-simulator/actions
.. |Documentation| image:: https://github.com/we3lab/dr_simulator/workflows/Documentation/badge.svg
   :target: https://we3lab.github.io/dr-simulator/
.. |Coverage| image:: https://codecov.io/gh/we3lab/dr-simulator/graph/badge.svg?token=HXGOYK8JCD
   :target: https://codecov.io/gh/we3lab/dr-simulator
