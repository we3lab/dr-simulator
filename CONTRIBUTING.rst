
Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Get Started!
------------

Ready to contribute? Here’s how to set up ``dr_simulator`` for local
development.

1. Fork the ``dr_simulator`` repo on GitHub.

2. Clone your fork locally:

   .. code:: bash

      git clone git@github.com:{your_name_here}/dr_simulator.git

3. Install the project in editable mode. (It is also recommended to work
   in a virtualenv or anaconda environment):

   .. code:: bash

      cd dr_simulator/
      pip install -e .[dev]

4. Create a branch for local development:

   .. code:: bash

      git checkout -b {your_development_type}/short-description

   Ex: feature/read-tiff-files or bugfix/handle-file-not-found Now you
   can make your changes locally.

5. When you’re done making changes, check that your changes pass linting
   and tests, including testing other Python versions with make:

   .. code:: bash

      make build

6. Commit your changes and push your branch to GitHub:

   .. code:: bash

      git add .
      git commit -m "Resolves gh-###. Your detailed description of your changes."
      git push origin {your_development_type}/short-description

7. Submit a pull request through the GitHub website.

Deploying
---------

A reminder for the maintainers on how to deploy. Make sure all your
changes are committed. Then run:

.. code:: bash

   bump2version patch # possible: major / minor / patch
   git push
   git push --tags

This will release a new package version on Git + GitHub and publish to
PyPI.