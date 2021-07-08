# coding: utf-8

from typing import List, TextIO

from .baseupdater import BaseUpdater


class VersionsXmlUpdater(BaseUpdater):
    """Update version information in versions.xml file."""

    def __init__(self):
        self._version_tpl = """<version number="{version}"{status}{date}>
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>"""

    def set_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        assert False

    def add_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        assert False

    def set_release_date(self, input_text: TextIO, date_str: str) -> str:
        assert False
