import os
from argparse import ArgumentParser

from .utils.generator import extract_schemas, generate_docs


def dir_path(string):
    if os.path.isdir(string):
        return os.path.abspath(string)
    else:
        raise NotADirectoryError(string)


def main():
    parser = ArgumentParser(prog='cerberus-docs', description='Cerberus-docs package')
    parser.add_argument('--source-dir', type=dir_path, action='store', default=os.getcwd())
    parser.add_argument('--build-dir', type=dir_path, action='store', default=os.getcwd())
    args = parser.parse_args()

    for root, dirs, filenames in os.walk(args.source_dir):
        for name in filenames:
            if name.endswith('.py'):
                file_path = os.path.join(root, name)
                try:
                    schema_map = extract_schemas(name, file_path)
                    generate_docs(schema_map, args.build_dir)
                except Exception as e:
                    print(f'{file_path} failed: {e}')
                    continue

    print('Docs successfully generated.')


if __name__ == '__main__':
    main()
