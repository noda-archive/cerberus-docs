__version__ = '0.1.0'

import logging

from .classes.cerberus_schema import CerberusSchema

logging.getLogger(__name__).addHandler(logging.NullHandler())
