Getting Started
================
Assuming that you have Python 3.7 or higher and ``virtualenv`` installed, set up your environment and install the required dependencies like this:

.. code-block:: sh

    $ git clone https://github.com/noda/cerberus-docs.git
    $ cd cerberus-docs
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ python -m pip install -r requirements/requirements.txt


Using Cerberus-docs
===================
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

Features
========

Current supported cerberus validation rules
-------------------------------------------

* required
* type
* allowed
* regex
* default
* schema
* meta

Comments in schemas
--------------------

Users can use the Cerberus meta validation rule with the 'description' key in order for cerberus-docs to generate the value as a comment in the documentation.

.. code-block:: py

    cerberus_schema = CerberusSchema({
        'my_field': {
            'type': 'string',
            'meta': {'description': 'Example comment'},
        },
    })

Generated input example
------------------------

Cerberus-docs generates an input example in yaml that will be appended to the documentation for every cerberus schemas .

Schema:

.. code-block:: py

    cerberus_schema = CerberusSchema{
        'name': {
            'required': True,
            'type': 'string',
            'meta': {'description': 'The first name of the person'},
        },
        'age': {
            'required': True,
            'type': 'integer',
        },
        'address': {
            'type': 'dict',
            'required': False,
            'schema': {
                'street': {
                    'type': 'string',
                    'required': True,
                },
                'zip_code': {
                    'type': 'string',
                    'required': True,
                },
                'city': {
                    'type': 'string',
                    'required': True,
                }
            },
        },
    })

Generated input example result:

.. code-block:: yaml

    address:
      city: str
      street: str
      zip_code: str
    age: 12345
    name: str

Example of complete generated documentation
--------------------------------------------

Schema:

.. code-block:: py

    schema = CerberusSchema{
        "version": {
            "required": True,
            "type": "string",
            "meta": {'description': "The version of the schema"},
            "allowed": ["v0", "v1"],
        },
        "type": {
            "required": True,
            "type": "string",
        },
        "spec": {
            "type": "dict",
            "required": False,
            "schema": {
                "sources": {
                    "type": "list",
                    "required": False,
                    "meta": {'description': "Available sources"},
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {
                                "type": "string",
                                "required": True,
                            },
                            "domain": {
                                "type": "string",
                                "required": True,
                            },
                        }
                    },
                }
            },
        },
    })

Result:

.. code-block::

    ## MyFile

    `version`: **[required]** string, one of;
      - v0
      - v1


        The version of the schema

    `type`: **[required]** string,

    `spec`: **[optional]** dict, [MyFileSpec](#MyFileSpec)


    ## MyFileSpec

    `sources`: **[optional]** list, [MyFileSpecSources](#MyFileSpecSources)


        Available sources


    ## MyFileSpecSources

    `name`: **[required]** string,

    `domain`: **[required]** string,


    ## Example Schema Input

    ```
    version: v0
    type: str
    spec:
      sources:
      - domain: str
        name: str
    ```
