import os
from typing import Optional

from .exceptions import CerberusDocsException


class MarkDownFile:
    """
    MarkDownFile class creates a new file of MarkDown extension.
    """
    def __init__(self,
                 file_name: str,
                 file_mode: Optional[str] = 'w+',
                 file_path: Optional[str] = None
                 ) -> None:
        """
        Creates a markdown file

        Args:
            file_name (str): Name of the file.
            file_mode (Optional[str]): Modes described here: https://docs.python.org/3/library/functions.html#open
            file_path (Optional[str]): File path to save the file at.

        Raises:
            :class:`.CerberusDocsException`: No name provided to MarkDownFile
        """
        if not file_name:
            raise CerberusDocsException('No name provided to MarkDownFile')

        self.file_name = file_name if file_name.endswith('.md') else f'{file_name}.md'
        self.file_path = os.path.join(file_path, file_name) if file_path else self.file_name
        self.file_mode = file_mode
        self.file = open(self.file_path, self.file_mode, encoding='UTF-8')
        self.file.close()

    def write(self, data: str) -> None:
        """
        Write to file.

        Args:
            data (str): Content that should be written to the file.
        """
        with open(self.file_path, self.file_mode, encoding='utf-8') as self.file:
            self.file.write(data)
