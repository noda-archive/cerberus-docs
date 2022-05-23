import os
import shutil
import unittest
from pathlib import Path

from cerberus_docs.cli import dir_path, parse_args


class TestCli(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.test_folder: str = 'test_dir'
        self.test_folder_path = os.path.join(self.current_dir, self.test_folder)
        os.mkdir(self.test_folder_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_folder_path)

    def test_dir_path(self) -> None:
        with self.subTest('is dir'):
            path = dir_path(self.test_folder_path)
            self.assertIn(self.test_folder_path, path)
        with self.subTest('is not dir'):
            self.assertRaises(NotADirectoryError, dir_path, 'doesnotexist')

    def test_parse_args(self) -> None:
        source_dir = os.path.join(self.current_dir, '__mocks__')
        parse_args([f'--source-dir={source_dir}', f'--build-dir={self.test_folder_path}'])

        parent_file_path = os.path.join(self.test_folder_path, 'MockFileParent_cerberus_doc.md')
        child_file_path = os.path.join(self.test_folder_path, 'MockFileChild_cerberus_doc.md')
        mock_file_path = os.path.join(self.test_folder_path, 'MockFile1_cerberus_doc.md')

        md_file_parent = Path(parent_file_path)
        md_file_child = Path(child_file_path)
        md_file_mock = Path(mock_file_path)

        self.assertTrue(md_file_parent.is_file())
        self.assertTrue(md_file_child.is_file())
        self.assertTrue(md_file_mock.is_file())

        with open(parent_file_path, 'r') as parent_file:
            self.assertEqual(parent_file.read(), '\n## MockFileParent\n\n`name`: string, \n\n\n## Example Schema Input\n\n```\nname: str\n```\n')  # noqa: E501

        with open(child_file_path, 'r') as child_file:
            self.assertEqual(child_file.read(), '\n## MockFileChild\n\n`name`: string, \n\n\n## Example Schema Input\n\n```\nname: str\n```\n')  # noqa: E501

        with open(mock_file_path, 'r') as mock_file:
            self.assertEqual(mock_file.read(), '\n## MockFile1\n\n`name`: string, \n\n\n## Example Schema Input\n\n```\nname: str\n```\n')  # noqa: E501
