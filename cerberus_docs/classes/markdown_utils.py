from collections import OrderedDict
from typing import Optional, Dict, Any, List, Union

from .markdown_file import MarkDownFile
from .types import Schema, Attribute, SortedAttribute, FormattedAttribute


class MarkDownUtils:
    """
    Class that helps generate documentation for cerberus in Markdown format.
    """
    def __init__(self,
                 file_name: str,
                 file_mode: Optional[str] = 'w+',
                 file_path: Optional[str] = None
                 ) -> None:
        """
        MarkDownUtils constructor

        Attributes:
            self.content (str): Contains the string that will be written to the
                markdown file when calling create_md_file
            self.generator_map (Dict[str, Any]): Mapping for using the right generator
                function for the right validation rule
            self.validation_rule_priority_list (List[str]): Determines the order in which each validation rule should
                be displayed in the MarkDown file
            self.validation_rule_separators (Dict[str, str]): The separator that should be added
                after each validation rule

        Args:
            file_name (str): Name of the file.
            file_mode (Optional[str]): Modes described here: https://docs.python.org/3/library/functions.html#open
            file_path (Optional[str]): File path to save the file at.
        """
        self.file_name: str = file_name
        self.file_path: str = file_path
        self.file_mode: str = file_mode
        self.content: str = ''
        self.generator_map: Dict[str, Any] = {
            'required': self._generate_required,
            'type': self._generate_type,
            'allowed': self._generate_allowed,
            'regex': self._generate_regex,
            'default': self._generate_default,
            'schema': self._generate_schema,
            'meta': self._generate_description
        }
        self.validation_rule_priority_list: List[str] = [
            'required',
            'type',
            'regex',
            'default',
            'schema',
            'allowed',
            'meta'
        ]
        self.validation_rule_separators: Dict[str, str] = {
            'type': ', ',
            'regex': ', ',
            'default': ', '
        }

    def _is_last_item(self, index: int, iterable: List) -> bool:
        """
        Returns if the input index is the last entry in the list or not

        Args:
             index (int): index to check
             iterable (List): List to compare the index with
        """
        return index == len(iterable) - 1

    def _append_to_content(self, data: str) -> None:
        """
        Append data to self.content

        Args:
            data (str): String value to append.
        """
        self.content += data

    def _generate_name(self, name: str) -> str:
        """
        Generate the name of a validation rule in MarkDown format.

        Args:
             name (str): Name to generate MarkDown formatted string from.

        Returns:
            MarkDown formatted string.
        """
        return f'`{name}`: '

    def _generate_required(self, is_required: bool) -> str:
        """
        Generate the validation rule 'required' in MarkDown format.

        Args:
             is_required (bool): Determines what string should be returned.

        Returns:
            MarkDown formatted string depending on if is_required is True or False.
        """
        return '**[required]**' if is_required else '**[optional]**'

    def _generate_type(self, attribute_type: str) -> str:
        """
        Generate the validation rule 'type' in MarkDown format.

        Args:
             attribute_type (str): Type to generate MarkDown formatted string from.

        Returns:
            MarkDown formatted string.
        """
        return attribute_type

    def _generate_allowed(self, allowed_values: List[Union[str, int]]) -> str:
        """
        Generate the validation rule 'allowed' in MarkDown format.

        Args:
             allowed_values (List[Union[str, int]]): List of values that should be displayed in a MarkDown list.

        Returns:
            MarkDown formatted string.
        """
        if not allowed_values:
            return ''
        result: str = 'one of;\n'
        for i, value in enumerate(allowed_values):
            result += f'  - {value}'
            if not self._is_last_item(i, allowed_values):
                result += '\n'
        return result

    def _generate_regex(self, regex: str) -> str:
        """
        Generate the validation rule 'regex' in MarkDown format.

        Args:
             regex (str): Regex string to generate MarkDown formatted string from

        Returns:
            MarkDown formatted string.
        """
        return f'must match {regex}'

    def _generate_default(self, default_value: Any) -> str:
        """
        Generate the validation rule 'default' in MarkDown format.

        Args:
             default_value (any): Default value to generate MarkDown formatted string from

        Returns:
            MarkDown formatted string.
        """
        return f'defaults to {default_value}'

    def _generate_schema(self, class_name: str) -> str:
        """
        Generate the validation rule 'schema' in MarkDown format.

        Args:
             class_name (str): Class name to generate MarkDown formatted string from

        Returns:
            MarkDown formatted string.
        """
        return f'[{class_name}](#{class_name})'

    def _generate_description(self, meta_object) -> Optional[str]:
        """
        Generate a description of the attribute in MarkDown format by
        reading the 'description' field in the meta object.

        Args:
            meta_object:

        Returns:
             MarkDown formatted string.
        """
        description = meta_object.get('description')
        return f'\n\n\n    {description}' if description else None

    def _sort_attribute_fields_order(self, attribute: FormattedAttribute) -> SortedAttribute:
        """
        Sorts the attribute keys by the order in the priority list.
        This will also filter out any validation rule that is not supported (is in the priority list)

        Args:
             attribute (Attribute) Attribute to sort

        Returns:
            OrderedDict of the attributes keys ordered by the priority list
        """
        return OrderedDict(
            [(rule, attribute[rule]) for rule in self.validation_rule_priority_list if attribute.get(rule) is not None]
        )

    def _get_validation_rule_separator(self, validation_rule: str) -> str:
        """
        Returns the correct separator for the input validation rule. Defaults to a space if no explicit rule is found.

        Args:
             validation_rule (str) The validation rule to get the separator for
        """
        return self.validation_rule_separators.get(validation_rule, ' ')

    def _attribute_to_string(self, attribute: FormattedAttribute) -> str:
        """
        Takes an attribute and converts it to a string with separators between every validation rule.

        Args:
            attribute (Attribute): The attribute to convert to a string

        Returns:
            String representation of attribute
        """
        result: str = ''
        for i, key in enumerate(attribute.keys()):
            result += attribute[key]
            result += self._get_validation_rule_separator(key)
        result += '\n\n'
        return result

    def generate_header(self, title: str, level: Optional[int] = 1) -> None:
        """
        Generate a header in MarkDown format given a title and level and appends it to self.content.

        Args:
             title (str): Header title
             level (Optional[int]): Header level, 1 - 6 is allowed. Default is 1.
        """
        restricted_level: int = 6 if level > 6 else 1 if level < 1 else level
        header: str = f"\n{'#' * restricted_level} {title}\n\n"
        self._append_to_content(header)

    def _format_validation_rule(self, validation_rule: str, attribute: Attribute, schema_name: str) -> Optional[str]:
        """
        Takes a validation rule and returns the generated markdown string value of that rule.

        Args:
            validation_rule (str): The validation rule to generate a markdown string from.
            attribute: (Attribute): The attribute which the validation rule belongs to.
            schema_name (str): The schema name

        """
        if validation_rule == 'schema':
            return self._generate_schema(schema_name)
        return self.generator_map.get(validation_rule, lambda *args: None)(attribute[validation_rule])  # noqa: E501

    def _get_schema(self, validation_rule: str, attribute: Attribute) -> Optional[Schema]:
        """
        Returns a schema from an attribute depending on the attribute type.
        Used when saving schemas for later use, in order to recursively generate attributes with nested schemas.

        Args:
            validation_rule (str): A validation rule
            attribute (Attribute): The attribute which the validation rule belongs to.
        """
        rule_is_schema = validation_rule == 'schema'
        attribute_is_dict = attribute.get('type') == 'dict'
        attribute_is_list = attribute.get('type') == 'list'
        if rule_is_schema and attribute_is_dict:
            return attribute[validation_rule]
        elif rule_is_schema and attribute_is_list:
            if attribute[validation_rule].get('type') == 'dict':
                return attribute[validation_rule].get('schema', {})
            else:
                return {'_': attribute[validation_rule]}
        return None

    def generate_attributes(self, class_name: str, schema: Schema) -> None:
        """
        Takes a schema, generates MarkDown strings for every attribute -> validation rule and appends it to
        self.content. If the attribute contains a schema validation rule, the method will recursively generate
        MarkDown strings through the whole Schema.

        Args:
             class_name (str): The class name of the class the schema sent in was found.
             schema (Schema): The schema that the function should generate documentation from.
        """
        additional_schemas: Dict[str, Schema] = {}
        for attribute_name in schema.keys():
            self._append_to_content(self._generate_name(attribute_name))
            attribute: Attribute = schema[attribute_name]
            formatted_attribute: FormattedAttribute = {}
            for validation_rule in attribute:
                schema_name: str = f'{class_name}{attribute_name.capitalize()}'
                formatted_attribute[validation_rule] = self._format_validation_rule(validation_rule, attribute, schema_name)  # noqa: E501
                additional_schema = self._get_schema(validation_rule, attribute)
                if additional_schema:
                    additional_schemas[schema_name] = additional_schema
            sorted_attribute: SortedAttribute = self._sort_attribute_fields_order(formatted_attribute)
            self._append_to_content(self._attribute_to_string(sorted_attribute))
        for additional_schema_name in additional_schemas.keys():
            self.generate_header(level=2, title=additional_schema_name)
            self.generate_attributes(additional_schema_name, additional_schemas[additional_schema_name])

    def create_md_file(self) -> MarkDownFile:
        """
        Creates a MarkDown file and writes self.content to it.

        Returns:
            The created MarkDown file
        """
        md_file = MarkDownFile(self.file_name, self.file_mode, self.file_path)
        md_file.write(self.content)
        return md_file
