import unittest

from cerberus_docs import CerberusSchema


class TestCerberusSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {'validation_rule': 'test'}

    def test_constructor(self) -> None:
        cerberus_schema = CerberusSchema(self.schema)
        self.assertEqual(cerberus_schema.schema, self.schema)

    def test_to_schema(self) -> None:
        cerberus_schema = CerberusSchema(self.schema)
        self.assertEqual(cerberus_schema.to_schema(), self.schema)
