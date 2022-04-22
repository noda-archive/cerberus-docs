import os
import copy
import shutil
import unittest
from typing import List, Union, Any

from cerberus_docs import MarkDownUtils
from cerberus_docs.classes.types import SortedAttribute, Attribute, Schema


class TestMarkDownUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.attribute = {
            'allowed': ['1', '2'],
            'regex': '(?<=-)w+',
            'type': 'string',
            'required': True,
            'schema': {},
            'default': {},
        }
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.test_folder: str = 'test_dir'
        self.test_folder_path = os.path.join(self.current_dir, self.test_folder)
        self.file_name: str = 'testfile'
        self.md_utils = MarkDownUtils(self.file_name, file_path=self.test_folder_path)
        os.mkdir(self.test_folder_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_folder_path)

    def test_is_last_item(self) -> None:
        iterator: List[int] = [1, 2, 3]
        with self.subTest('is last'):
            i: int = 2
            self.assertTrue(self.md_utils._is_last_item(i, iterator))

        with self.subTest('is not last'):
            i: int = 1
            self.assertFalse(self.md_utils._is_last_item(i, iterator))

    def test_append_to_content(self) -> None:
        self.md_utils._append_to_content('Hello ')
        self.md_utils._append_to_content('world!')
        self.assertEqual(self.md_utils.content, 'Hello world!')

    def test_generate_name(self) -> None:
        name: str = 'John Doe'
        generated_name: str = self.md_utils._generate_name(name)
        self.assertEqual(generated_name, f'`{name}`: ')

    def test_generate_required(self) -> None:
        with self.subTest('required is false'):
            self.assertEqual(self.md_utils._generate_required(False), '**[optional]**')
        with self.subTest('required is true'):
            self.assertEqual(self.md_utils._generate_required(True), '**[required]**')

    def test_generate_type(self) -> None:
        type_: str = 'str'
        self.assertEqual(self.md_utils._generate_type(type_), type_)

    def test_generate_allowed(self) -> None:
        with self.subTest('successfully generates markdown'):
            allowed_values: List[Union[str, int]] = ['1', '2', 3]
            self.assertEqual(
                self.md_utils._generate_allowed(allowed_values),
                f'one of;\n  - {allowed_values[0]}\n  - {allowed_values[1]}\n  - {allowed_values[2]}'
            )
        with self.subTest('allowed_values is empty'):
            allowed_values: List[Union[str, int]] = []
            self.assertEqual(self.md_utils._generate_allowed(allowed_values), '')

    def test_generate_regex(self) -> None:
        regex: str = '(?<=-)w+'
        self.assertEqual(self.md_utils._generate_regex(regex), f'must match {regex}')

    def test_generate_default(self) -> None:
        default_value: Any = {}
        self.assertEqual(self.md_utils._generate_default(default_value), f'defaults to {default_value}')

    def test_generate_schema(self) -> None:
        class_name: str = 'TestClass'
        self.assertEqual(self.md_utils._generate_schema(class_name), f'[{class_name}](#{class_name})')

    def test_sort_attribute_fields_order(self) -> None:
        sorted_attribute: SortedAttribute = self.md_utils._sort_attribute_fields_order(self.attribute)
        sorted_attribute_list = list(sorted_attribute.items())
        for i, item in enumerate(sorted_attribute_list):
            key = item[0]
            self.assertEqual(self.md_utils.validation_rule_priority_list[i], key)

    def test_get_validation_rule_separator(self) -> None:
        with self.subTest('gets default separator'):
            self.assertEqual(self.md_utils._get_validation_rule_separator('uknown_field'), ' ')

        with self.subTest('gets separator'):
            self.assertEqual(self.md_utils._get_validation_rule_separator('type'), ', ')

    def test_attribute_to_string(self) -> None:
        attribute: Attribute = {
            'required': '**[required]**',
            'type': 'str',
            'regex': 'must match (?<=-)w+',
        }
        self.assertEqual(self.md_utils._attribute_to_string(attribute), '**[required]** str, must match (?<=-)w+, \n\n')

    def test_generate_header(self) -> None:
        title: str = 'TestTitle'
        with self.subTest('input level is below 1'):
            self.md_utils.generate_header(title, level=-1)
            self.assertEqual(self.md_utils.content, f'\n# {title}\n\n')
            self.md_utils.content = ''

        with self.subTest('input level is over 6'):
            self.md_utils.generate_header(title, level=99)
            self.assertEqual(self.md_utils.content, f'\n###### {title}\n\n')
            self.md_utils.content = ''

        with self.subTest('input level is in legal span'):
            self.md_utils.generate_header(title, level=4)
            self.assertEqual(self.md_utils.content, f'\n#### {title}\n\n')
            self.md_utils.content = ''

    def test_generate_attribute(self) -> None:
        with self.subTest('with no nested schemas'):
            attribute: Attribute = copy.deepcopy(self.attribute)
            del attribute['schema']
            schema: Schema = {'test_attribute': attribute}
            self.md_utils.generate_attributes('TestClass', schema)
            self.assertEqual(
                self.md_utils.content,
                '`test_attribute`: **[required]** string, must match (?<=-)w+, defaults to {}, one of;\n  - 1\n  - 2 \n\n'  # noqa: E501
            )
            self.md_utils.content = ''
        with self.subTest('with nested schemas'):
            attribute: Attribute = copy.deepcopy(self.attribute)
            nested_attribute: Attribute = copy.deepcopy(self.attribute)
            del nested_attribute['schema']
            attribute['schema'] = {'nested_schema': nested_attribute}
            schema: Schema = {'test_attribute': attribute}
            self.md_utils.generate_attributes('TestClass', schema)
            self.assertEqual(
                self.md_utils.content,
                '`test_attribute`: **[required]** string, must match (?<=-)w+, defaults to {}, [TestClassTest_attribute](#TestClassTest_attribute) one of;\n  - 1\n  - 2 \n\n'  # noqa: E501
                '\n## TestClassTest_attribute\n\n'
                '`nested_schema`: **[required]** string, must match (?<=-)w+, defaults to {}, one of;\n  - 1\n  - 2 \n\n'  # noqa: E501
            )
            self.md_utils.content = ''

    def test_create_md_file(self) -> None:
        content = 'Hello World!'
        self.md_utils.content = content
        self.md_utils.create_md_file()
        with open(os.path.join(self.test_folder_path, self.file_name), 'r') as file:
            self.assertEqual(file.read(), content)
