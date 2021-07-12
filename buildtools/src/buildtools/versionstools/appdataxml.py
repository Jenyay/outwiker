# coding: utf-8

from typing import TextIO, List
import xml.etree.ElementTree as ET

from .baseupdater import BaseUpdater


class AppDataXmlUpdater(BaseUpdater):
    """Class for net.jenyay.Outwiker.appdata.xml file updating"""

    def set_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        tree = ET.parse(input_text)
        root = tree.getroot()
        version_tag = root.find('releases').find('release')

        version_str = '.'.join([str(item) for item in version])
        version_tag.set('version', version_str)

        return ET.tostring(root,
                           encoding='UTF-8',
                           xml_declaration=True).decode()

    def add_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        assert False

    def set_release_date(self, input_text: TextIO, date_str: str) -> str:
        assert False
