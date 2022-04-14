import os
import shutil
import unittest
from pathlib import Path

from cerberus_docs import MarkDownFile, CerberusDocsException


class TestMarkDownFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_folder = 'test_dir'
        os.mkdir(self.test_folder)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_folder)

    def test_file_created(self) -> None:
        file_name = 'testfile.md'
        MarkDownFile(file_name, file_path=self.test_folder)
        md_file = Path(os.path.join(self.test_folder, file_name))
        self.assertTrue(md_file.is_file())

    def test_file_name(self) -> None:
        file_name = 'testfile'
        md_file = MarkDownFile(file_name, file_path=self.test_folder)
        self.assertEqual(md_file.file_name, f'{file_name}.md')

    def test_file_path(self) -> None:
        file_name = 'testfile.md'
        file_path = 'temp_dir'
        os.mkdir(os.path.join(self.test_folder, file_path))
        MarkDownFile(
            file_name=file_name,
            file_path=os.path.join(self.test_folder, file_path)
        )
        md_file = Path(os.path.join(self.test_folder, file_path, file_name))
        self.assertTrue(md_file.is_file())

    def test_file_mode(self) -> None:
        file_name = 'testfile.md'
        file_mode = 'a+'
        md_file = MarkDownFile(file_name, file_mode, self.test_folder)
        self.assertEqual(md_file.file_mode, file_mode)

    def test_no_file_name(self) -> None:
        self.assertRaises(CerberusDocsException, MarkDownFile, None)

    def test_write(self) -> None:
        file_name = 'testfile.md'
        content = 'This is a test!'
        md_file = MarkDownFile(file_name, file_path=self.test_folder)
        md_file.write(content)
        with open(os.path.join(self.test_folder, file_name), 'r') as file:
            self.assertEqual(file.read(), content)
