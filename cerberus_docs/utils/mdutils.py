import os

from mdutils import MdUtils
from mdutils.fileutils import MarkDownFile


class ExtendedMarkDownFile(MarkDownFile):
    """
    Extended MarkDown file gives more customization in the constructor to choose file mode and file path.
    """
    def __init__(self, name='', file_mode='w+', file_path=None):
        """
        Creates a markdown file, if name is not empty.
        :param str name: file name
        :param str file_path: Path to file
        """

        if name:
            self.file_name = name if name.endswith('.md') else name + '.md'
            self.file_path = os.path.join(file_path, name) if file_path else self.file_name
            self.file = open(self.file_path, file_mode, encoding='UTF-8')
            self.file.close()

    def rewrite_all_file(self, data, file_mode='w'):
        """
        Rewrite all the data of a Markdown file by ``data``.

        :param str data: is a string containing all the data that is written in the markdown file.
        :param str file_mode: Modes described here: https://docs.python.org/3/library/functions.html#open
        """
        with open(self.file_path, file_mode, encoding='utf-8') as self.file:
            self.file.write(data)


class ExtendedMdutils(MdUtils):
    def __init__(self, file_name, file_mode='w+', file_path=None, title="", author=""):
        super().__init__(file_name, title, author)
        self.file_path = file_path
        self.file_mode = file_mode

    def create_md_file(self):
        """It creates a new Markdown file.
        :return: return an instance of a ExtendedMarkDownFile."""
        md_file = ExtendedMarkDownFile(self.file_name, self.file_mode, self.file_path)
        md_file.rewrite_all_file(
            self.title + self.table_of_contents + self.file_data_text + self.reference.get_references_as_markdown(),
            self.file_mode
        )
        return md_file
