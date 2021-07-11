# coding: utf-8

from typing import List, TextIO

from .baseupdater import BaseUpdater


class VersionsXmlUpdater(BaseUpdater):
    """Update version information in versions.xml file."""

    def __init__(self):
        self._versions_tag = '<versions>\n'
        self._new_version_tpl = """<versions>
    <version number="{version}"{status}>
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>

"""

    def set_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        assert False

    def add_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        version_str = '.'.join([str(item) for item in version])
        status_str = ' status="{}"'.format(status) if status else ''

        new_version_tag = self._new_version_tpl.format(version=version_str,
                                                       status=status_str)
        return input_text.read().replace(self._versions_tag, new_version_tag)

    def set_release_date(self, input_text: TextIO, date_str: str) -> str:
        assert False
