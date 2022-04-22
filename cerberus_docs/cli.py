import os
import sys
from argparse import ArgumentParser, Namespace

from .classes.types import SchemaMap
from .utils.generator import extract_schemas, generate_docs


def dir_path(string: str) -> str:
    """
    Returns the absolute path of the input argument if it is a directory.

    Args:
         string (str): A string argument input from argparse.

    Raises:
        NotADirectoryError
    """
    if os.path.isdir(string):
        return os.path.abspath(string)
    else:
        raise NotADirectoryError(string)


def parse_args(args) -> None:
    """
    The entry point for argparse.
    Will generate documentation of the CerberusSchemas that can be found in the given source-dir
    """
    parser: ArgumentParser = ArgumentParser(prog='cerberus-docs', description='Cerberus-docs package')
    parser.add_argument('--source-dir', type=dir_path, action='store', default=os.getcwd())
    parser.add_argument('--build-dir', type=dir_path, action='store', default=os.getcwd())
    args: Namespace = parser.parse_args(args)

    for root, dirs, filenames in os.walk(args.source_dir):
        for name in filenames:
            if name.endswith('.py'):
                file_path: str = os.path.join(root, name)
                try:
                    schema_map: SchemaMap = extract_schemas(name, file_path)
                    generate_docs(schema_map, args.build_dir)
                except Exception as e:
                    print(f'{file_path} failed: {e}')
                    continue

    print('Docs successfully generated.')


def main() -> None:
    parse_args(sys.argv[1:])  # pragma: no cover


if __name__ == '__main__':
    main()  # pragma: no cover
