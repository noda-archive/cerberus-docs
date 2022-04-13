from collections import OrderedDict

from .markdown_file import MarkDownFile


class MarkDownUtils:
    def __init__(self, file_name, file_mode='w+', file_path=None):
        self.file_name = file_name
        self.file_path = file_path
        self.file_mode = file_mode
        self.content = ''
        self.generator_map = {
            'required': self._generate_required,
            'type': self._generate_type,
            'allowed': self._generate_allowed,
            'regex': self._generate_regex,
            'default': self._generate_default,
            'schema': self._generate_schema
        }
        self.validation_rule_priority_list = [
            'required',
            'type',
            'regex',
            'default',
            'schema',
            'allowed'
        ]
        self.validation_rule_separators = {
            'type': ', ',
            'regex': ', ',
            'default': ', '
        }

    def _is_last_item(self, index, iterable):
        return index == len(iterable) - 1

    def _append_to_content(self, data):
        self.content += data

    def _generate_name(self, name):
        return f'`{name}`: '

    def _generate_required(self, is_required):
        return '**[required]**' if is_required else '**[optional]**'

    def _generate_type(self, attribute_type):
        return attribute_type

    def _generate_allowed(self, allowed_values):
        if not allowed_values:
            return ''
        result = 'one of;\n'
        for i, value in enumerate(allowed_values):
            result += f'  - {value}'
            if not self._is_last_item(i, allowed_values):
                result += '\n'
        return result

    def _generate_regex(self, regex):
        return f'must match {regex}'

    def _generate_default(self, default_value):
        return f'defaults to {default_value}'

    def _generate_schema(self, class_name):
        return f'[{class_name}](#{class_name})'

    def _sort_attribute_fields_order(self, attribute):
        return OrderedDict(
            [(x, attribute[x]) for x in self.validation_rule_priority_list if attribute.get(x) is not None]
        )

    def _get_validation_rule_separator(self, validation_rule):
        return self.validation_rule_separators.get(validation_rule, ' ')

    def _attribute_to_string(self, attribute):
        res = ''
        for i, key in enumerate(attribute.keys()):
            res += attribute[key]
            res += self._get_validation_rule_separator(key)
        res += '\n\n'
        return res

    def generate_header(self, title, level=1):
        header = f"\n{'#' * level} {title}\n\n"
        self._append_to_content(header)

    def generate_attributes(self, class_name, schema):
        nested_schemas = {}
        for key in schema.keys():
            self._append_to_content(self._generate_name(key))
            attribute = schema[key]
            formatted_attribute = {}
            for i, validation_rule in enumerate(attribute):
                if validation_rule == 'schema':
                    nested_schema_name = f'{class_name}{key.capitalize()}'
                    nested_schemas[nested_schema_name] = attribute[validation_rule]
                    formatted_attribute[validation_rule] = self._generate_schema(nested_schema_name)
                else:
                    formatted_attribute[validation_rule] = self.generator_map.get(validation_rule, lambda *args: None)(attribute[validation_rule])  # noqa: E501
            sorted_attribute = self._sort_attribute_fields_order(formatted_attribute)
            self._append_to_content(self._attribute_to_string(sorted_attribute))
        for nested_schema_name in nested_schemas.keys():
            self.generate_header(level=2, title=nested_schema_name)
            self.generate_attributes(nested_schema_name, nested_schemas[nested_schema_name])

    def create_md_file(self):
        md_file = MarkDownFile(self.file_name, self.file_mode, self.file_path)
        md_file.write(self.content, self.file_mode)
        return md_file
