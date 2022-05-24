Enable Debug Logging
====================
To enable logging, add a handler to the `cerberus_docs` logger:

.. code-block:: python

    >>> import logging
    >>> logging.getLogger('cerberus_docs').addHandler(logging.StreamHandler())
    >>> logging.getLogger('cerberus_docs').setLevel(logging.DEBUG)
