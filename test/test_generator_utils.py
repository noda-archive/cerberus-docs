import os
import shutil
import unittest
from types import ModuleType

from cerberus_docs import import_module


class TestGeneratorUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.test_folder: str = 'test_dir'
        self.file_name: str = 'test_file.py'
        self.file_path: str = os.path.join(self.test_folder, self.file_name)
        os.mkdir(self.test_folder)
        self.file = open(self.file_path, 'w')
        self.file.close()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_folder)

    def test_extract_schemas(self) -> None:
        pass

    def test_import_module(self) -> None:
        module = import_module(self.file_name, self.file_path)
        self.assertTrue(isinstance(module, ModuleType))

    def test_generate_docs(self) -> None:
        pass
