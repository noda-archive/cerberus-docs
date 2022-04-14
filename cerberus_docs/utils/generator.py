import inspect
from importlib import util
from types import ModuleType
from typing import Dict, List

from ..classes.cerberus_schema import CerberusSchema
from ..classes.markdown_utils import MarkDownUtils
from ..classes.types import SchemaMap, Schema


def extract_schemas(file_name: str, file_path: str) -> SchemaMap:
    """
    Imports module at the provided file_path and name,
    finds all CerberusSchema classes and extracts the schemas into a schema map.

    Args:
         file_name (str): Name of the file.
         file_path (str): Path of the file.

    Returns:
        Returns the extracted schemas in a SchemaMap
    """
    module = import_module(file_name, file_path)
    classes = [obj[1] for obj in inspect.getmembers(module) if inspect.isclass(obj[1])]
    schema_map: SchemaMap = {}
    for class_ in classes:
        schemas: List[Dict] = []
        for i in inspect.getmembers(class_):
            if isinstance(i[1], CerberusSchema):
                schema: CerberusSchema = getattr(class_, i[0])
                schemas.append(schema.to_schema())
        if schemas:
            schema_map[class_.__name__] = schemas
    return schema_map


def import_module(file_name: str, file_path: str) -> ModuleType:
    """
    Import and return a python module from a path and name. Python 3.5+ only.

    Args:
        file_name (str): Name of the file.
        file_path (str): Path of the file.

    Returns:
        Returns the imported module
    """
    spec = util.spec_from_file_location(file_name, file_path)
    module: ModuleType = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_docs(schema_map: SchemaMap, build_dir: str) -> None:
    """
    Generate documentation given a SchemaMap and build directory.
    Creates a markdown file per schema and populates it with generated documentation from the schema attributes.

    Args:
        schema_map (SchemaMap) A dict which contains schemas grouped by the parent class name as key.
        build_dir (str): The directory where the generated docs should be saved.
    """
    for class_name in schema_map.keys():
        schemas: List[Schema] = schema_map[class_name]
        for i, schema in enumerate(schemas):
            file_mode: str = 'w+' if i == 0 else 'a'
            md_file = MarkDownUtils(
                file_name=f'{class_name}_cerberus_doc.md',
                file_mode=file_mode,
                file_path=build_dir
            )
            md_file.generate_header(level=2, title=class_name)
            md_file.generate_attributes(class_name, schema)
            md_file.create_md_file()
