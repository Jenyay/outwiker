# coding: utf-8

from typing import TextIO, List
import xml.etree.ElementTree as ET

from .baseupdater import BaseUpdater


class AppDataXmlUpdater(BaseUpdater):
    """Class for net.jenyay.Outwiker.appdata.xml file updating"""

    def __init__(self):
        self._releases_tag = '<releases>\n'
        self._new_release_tpl = """<releases>
    <release version="{version}" />
"""

    def set_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        tree = ET.parse(input_text)
        root = tree.getroot()
        release_tag = root.find('releases').find('release')

        version_str = '.'.join([str(item) for item in version])
        release_tag.set('version', version_str)

        return ET.tostring(root,
                           encoding='UTF-8',
                           xml_declaration=True).decode()

    def add_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        version_str = '.'.join([str(item) for item in version])
        new_release_tag = self._new_release_tpl.format(version=version_str)
        return input_text.read().replace(self._releases_tag, new_release_tag)

    def set_release_date(self, input_text: TextIO, date_str: str) -> str:
        tree = ET.parse(input_text)
        root = tree.getroot()
        release_tag = root.find('releases').find('release')

        release_tag.set('date', date_str)

        return ET.tostring(root,
                           encoding='UTF-8',
                           xml_declaration=True).decode()
