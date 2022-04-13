import os


class MarkDownFile:
    def __init__(self, name, file_mode='w+', file_path=None):
        if not name:
            raise Exception('No name provided to MarkDownFile')

        self.file_name = name if name.endswith('.md') else f'{name}.md'
        self.file_path = os.path.join(file_path, name) if file_path else self.file_name
        self.file = open(self.file_path, file_mode, encoding='UTF-8')
        self.file.close()

    def write(self, data, file_mode='w+'):
        """
        :param str file_mode: Modes described here: https://docs.python.org/3/library/functions.html#open
        """
        with open(self.file_path, file_mode, encoding='utf-8') as self.file:
            self.file.write(data)
