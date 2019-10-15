from datetime import datetime
from xml.etree import ElementTree
from typing import List, Optional

from .dataforlanguage import DataForLanguage
from .xmlchangelog import (XmlChangeLog, XmlChangeItem,
                           XmlDownload, XmlChangeLogVersionInfo)
from .version_xmlrequirements_factory import XmlRequirementsFactory


class XmlChangelogParser:
    ATTRIBUTE_LANGUAGE = 'lang'
    TAG_VERSIONS_VERSION = 'version[@number]'
    ATTRIBUTE_VERSION_NUMBER = 'number'
    ATTRIBUTE_VERSION_STATUS = 'status'
    ATTRIBUTE_VERSION_DATE = 'date'
    TAG_VERSION_CHANGES = 'changes'
    TAG_CHANGES_CHANGE = 'change'
    TAG_VERSION_DOWNLOAD = 'download[@href]'
    ATTRIBUTE_DOWNLOAD_HREF = 'href'

    @classmethod
    def parse(cls, text: str) -> 'XmlChangeLog':
        changelog = XmlChangeLog()

        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError:
            return changelog

        cls._setChangelogVersions(root, changelog)
        return changelog

    @classmethod
    def _setChangelogVersions(cls, root: ElementTree.Element, changelog: 'XmlChangeLog'):
        for tag_version in root.findall(cls.TAG_VERSIONS_VERSION):
            number = tag_version.get(cls.ATTRIBUTE_VERSION_NUMBER)
            assert number is not None

            status = tag_version.get(cls.ATTRIBUTE_VERSION_STATUS, '')
            date_str = tag_version.get(cls.ATTRIBUTE_VERSION_DATE, '')

            try:
                date = datetime.strptime(date_str, '%d.%m.%Y')      # type: Optional[datetime]
            except ValueError:
                date = None

            version_info = XmlChangeLogVersionInfo(number, status, date)

            cls._setChangeLog(tag_version, version_info.changes)
            cls._addDownloads(tag_version, version_info.downloads)

            changelog.versions.append(version_info)

    @classmethod
    def _setChangeLog(cls,
                      tag_version: ElementTree.Element,
                      changes: 'DataForLanguage[List[XmlChangeItem]]'):
        for tag_changes in tag_version.findall(cls.TAG_VERSION_CHANGES):
            language = tag_changes.get(cls.ATTRIBUTE_LANGUAGE, '')
            changes_list = []
            for tag_change in tag_changes.findall(cls.TAG_CHANGES_CHANGE):
                change_text = tag_change.text if tag_change.text is not None else ''
                change_item = XmlChangeItem(change_text)
                changes_list.append(change_item)

            changes.set_for_language(language, changes_list)

    @classmethod
    def _addDownloads(cls,
                      tag_version: ElementTree.Element,
                      downloads: 'List[XmlDownload]'):
        for tag_download in tag_version.findall(cls.TAG_VERSION_DOWNLOAD):
            href = tag_download.get(cls.ATTRIBUTE_DOWNLOAD_HREF)
            assert href is not None

            requirements = XmlRequirementsFactory.fromXml(tag_download)
            download = XmlDownload(href, requirements)
            downloads.append(download)
