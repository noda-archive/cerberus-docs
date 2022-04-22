from .types import Schema


class CerberusSchema:
    """
    A class to wrap a cerberus schema to make it possible for Cerberus-docs to find schemas with instance checking.
    """
    def __init__(self, schema: Schema) -> None:
        """
        CerberusSchema constructor

        Args:
            schema (Schema): Cerberus schema that should be recognizeable by cerberus-docs.
        """
        self.schema: Schema = schema

    def to_schema(self) -> Schema:
        """
        Return the schema wrapped by the class.
        """
        return self.schema
