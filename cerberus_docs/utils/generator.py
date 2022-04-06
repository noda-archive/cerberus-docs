import inspect
from importlib import util

from ..classes.cerberus_schema import CerberusSchema
from .mdutils import ExtendedMdutils


def extract_schemas(name, file_path):
    file = import_file(name, file_path)
    classes = [obj[1] for obj in inspect.getmembers(file) if inspect.isclass(obj[1])]
    schema_map = {}
    for class_ in classes:
        schemas = []
        for i in inspect.getmembers(class_):
            if isinstance(i[1], CerberusSchema):
                schema = getattr(class_, i[0])
                schemas.append(schema.to_schema())
        if schemas:
            schema_map[class_.__name__] = schemas
    return schema_map


def import_file(name, path):
    """
    Import a python module from a path. 3.5+ only.
    """
    spec = util.spec_from_file_location(name, path)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def generate_docs(schema_map, build_dir):
    for class_name in schema_map.keys():
        schemas = schema_map[class_name]
        for i, schema in enumerate(schemas):
            file_mode = 'w+' if i == 0 else 'a'
            md_file = ExtendedMdutils(
                file_name=f'{class_name}_cerberus_doc.md',
                title=class_name,
                file_mode=file_mode,
                file_path=build_dir
            )

            for key in schema.keys():
                md_file.new_header(level=1, title=f'{key}')
                md_file.new_list(schema[key].keys())

            md_file.create_md_file()
