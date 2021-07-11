# coding: utf-8

from typing import TextIO, List

from .baseupdater import BaseUpdater


class AppDataXmlUpdater(BaseUpdater):
    """Class for net.jenyay.Outwiker.appdata.xml file updating"""

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
