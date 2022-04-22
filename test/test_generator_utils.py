import os
import shutil
import unittest
from pathlib import Path
from types import ModuleType

from cerberus_docs import import_module, extract_schemas, generate_docs
from cerberus_docs.classes.types import SchemaMap


class TestGeneratorUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.test_folder: str = 'test_dir'
        self.test_folder_path = os.path.join(self.current_dir, self.test_folder)
        self.file_name: str = 'test_file.py'
        self.file_path: str = os.path.join(self.test_folder_path, self.file_name)
        os.mkdir(self.test_folder_path)
        self.file = open(self.file_path, 'w')
        self.file.close()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_folder_path)

    def test_extract_schemas(self) -> None:
        schema_path = os.path.join(self.current_dir, '__mocks__/mock_folder_1/mock_file_1.py')
        schema_map: SchemaMap = extract_schemas('mock_file_1', schema_path)
        self.assertIsNotNone(schema_map.get('MockFileParent'))
        self.assertEqual(len(schema_map['MockFileParent']), 1)
        self.assertIsNotNone(schema_map.get('MockFileChild'))
        self.assertEqual(len(schema_map['MockFileChild']), 1)
        self.assertEqual(len(schema_map.keys()), 2)

    def test_import_module(self) -> None:
        module = import_module(self.file_name, self.file_path)
        self.assertTrue(isinstance(module, ModuleType))

    def test_generate_docs(self) -> None:
        schema_path = os.path.join(self.current_dir, '__mocks__/mock_folder_1/mock_file_1.py')
        schema_map: SchemaMap = extract_schemas('mock_file_1', schema_path)
        generate_docs(schema_map, self.test_folder_path)

        parent_file_path = os.path.join(self.test_folder_path, 'MockFileParent_cerberus_doc.md')
        child_file_path = os.path.join(self.test_folder_path, 'MockFileChild_cerberus_doc.md')
        md_file_parent = Path(parent_file_path)
        md_file_child = Path(child_file_path)

        self.assertTrue(md_file_parent.is_file())
        self.assertTrue(md_file_child.is_file())

        with open(parent_file_path, 'r') as parent_file:
            self.assertEqual(parent_file.read(), '\n## MockFileParent\n\n`name`: string, \n\n')

        with open(child_file_path, 'r') as child_file:
            self.assertEqual(child_file.read(), '\n## MockFileChild\n\n`name`: string, \n\n')
