Getting Started
---------------
Assuming that you have Python 3.7 or higher and ``virtualenv`` installed, set up your environment and install the required dependencies like this:

.. code-block:: sh

    $ git clone https://github.com/noda/cerberus-docs.git
    $ cd cerberus-docs
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ python -m pip install -r requirements/requirements.txt


Using Cerberus-docs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TODO

Running Tests
~~~~~~~~~~~~~
You can run tests in all supported Python versions using ``tox``. By default,
it will run all of the unit tests, linters and coverage. Note that this requires that you have all supported
versions of Python installed, otherwise you must pass ``-e``.

.. code-block:: sh

    $ tox
    $ tox -e py37,py38

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~
Logging can be enabled in order to debug sent requests to the EnergyView API. To enable logging, add a handler to the `selfhost_client` logger:

.. code-block:: python

    >>> import logging
    >>> logging.getLogger('cerberus_docs').addHandler(logging.StreamHandler())
    >>> logging.getLogger('cerberus_docs').setLevel(logging.DEBUG)
