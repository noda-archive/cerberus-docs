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
In order for cerberus-docs to be able to find the Cerberus schemas, every schema that should be documented must be wrapped by the CerberusSchema class.

To retrieve the original dict from the class, use the ``.to_schema()`` method.

.. code-block:: python

    from cerberus_docs import CerberusSchema

    class Foo:
        cerberus_schema = CerberusSchema({'name': {'type': 'string'}})

        def __init__(self):
            v = Validator(self.cerberus_schema.to_schema())

To run cerberus-docs use the command ``cerberus-docs`` and specify:

``--source-dir``: The directory with the source code. Cerberus-docs will find every python module in the directory tree and look for CerberusSchema classes. Defaults to the current working directory.

``--build-dir``: The directory where the generated documentation files will be saved. Defaults to the current working directory.

Example:

.. code-block:: sh

    $ cerberus-docs --source-dir ./myProject --build-dir ./myDocs
    Docs successfully generated.

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
To enable logging, add a handler to the `cerberus_docs` logger:

.. code-block:: python

    >>> import logging
    >>> logging.getLogger('cerberus_docs').addHandler(logging.StreamHandler())
    >>> logging.getLogger('cerberus_docs').setLevel(logging.DEBUG)
