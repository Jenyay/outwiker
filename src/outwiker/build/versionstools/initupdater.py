# -*- coding: utf-8 -*-

import re
from typing import List, TextIO

from .baseupdater import BaseUpdater


class InitUpdater(BaseUpdater):
    """Add / edit __init__.py file to version update"""

    def __init__(self):
        self._version_prefix = re.compile(
            r'(?P<prefix>\s*__version__\s*=\s*).*')
        self._status_prefix = re.compile(r'(?P<prefix>\s*__status__\s*=\s*).*')

    def set_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        """Set new version number and status for outwiker/__init__.py file.
Returns a new content for the file."""
        version_str = '({})'.format(', '.join([str(item) for item in version]))
        status_str = "'{}'".format(status)

        new_lines = []
        for line in input_text.readlines():
            version_match = self._version_prefix.match(line)
            status_match = self._status_prefix.match(line)

            if version_match is not None:
                line = version_match.group('prefix') + version_str
            elif status_match is not None:
                line = status_match.group('prefix') + status_str

            new_lines.append(line.rstrip())

        return '\n'.join(new_lines)

    def add_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        return self.set_version(input_text, version, status)

    def set_release_date(self, input_text: TextIO, date_str: str) -> str:
        return input_text.read()
