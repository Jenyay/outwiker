# -*- coding: utf-8 -*-

from datetime import datetime
from xml.etree import ElementTree
from typing import List, Optional, Iterable

from .dataforlanguage import DataForLanguage


def _getTextValue(root: ElementTree.Element, tag_name: str) -> str:
    """
    Return text from tag with name tag_name or empty string.
    """
    result = None
    result_tag = root.find(tag_name)
    if result_tag is not None:
        result = result_tag.text

    if result is None:
        result = ''
    return result


def _getTextList(root: ElementTree.Element, tag_name: str) -> List[str]:
    """
    Return text list from tags with name tag_name
    """
    result = []

    for tag in root.findall(tag_name):
        text = tag.text if tag.text is not None else ''
        result.append(text)

    return result


class XmlAppInfoParser:
    """
    Class to read and write application info in XML format.
    """
    ATTRIBUTE_LANGUAGE = 'lang'

    TAG_APP_NAME = 'name'
    TAG_WEBSITE = 'website'
    TAG_DESCRIPTION = 'description'
    TAG_APP_INFO_URL = 'info_url'
    TAG_APP_UPDATES_URL = 'updates_url'
    TAG_AUTHOR = 'author'
    TAG_AUTHOR_NAME = 'name'
    TAG_AUTHOR_EMAIL = 'email'
    TAG_AUTHOR_WEBSITE = 'website'
    TAG_VERSION = 'version'
    ATTRIBUTE_VERSION_NUMBER = 'number'
    ATTRIBUTE_VERSION_STATUS = 'status'

    def parse(self, text: str) -> 'XmlAppInfo':
        appinfo = XmlAppInfo()

        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError:
            return appinfo

        self._setAppInfoUrl(root, appinfo)
        self._setAppUpdatesUrl(root, appinfo)
        self._setAppName(root, appinfo)
        self._setWebsite(root, appinfo)
        self._setDescription(root, appinfo)
        self._setAuthor(root, appinfo)
        self._setVersion(root, appinfo)
        self._setRequirements(root, appinfo)

        return appinfo

    def _setRequirements(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        requirements = XmlRequirementsFactory.fromXml(root)
        appinfo.requirements.os_list = requirements.os_list[:]
        appinfo.requirements.api_list = requirements.api_list[:]

    def _setTextForLanguage(self,
                            root: ElementTree.Element,
                            tag_name: str,
                            data_for_language: 'DataForLanguage'):
        '''
        Fill data_for_language with text from tag with name tag_name
        '''
        for tag in root.findall(tag_name):
            language = tag.get(self.ATTRIBUTE_LANGUAGE, '')
            text = tag.text if tag.text is not None else ''
            data_for_language.set_for_language(language, text)

    def _setAppName(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        self._setTextForLanguage(root, self.TAG_APP_NAME, appinfo.app_name)

    def _setWebsite(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        self._setTextForLanguage(root, self.TAG_WEBSITE, appinfo.website)

    def _setDescription(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        self._setTextForLanguage(
            root, self.TAG_DESCRIPTION, appinfo.description)

    def _setAppInfoUrl(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        url = _getTextValue(root, self.TAG_APP_INFO_URL)
        appinfo.app_info_url = url

    def _setAppUpdatesUrl(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        url = _getTextValue(root, self.TAG_APP_UPDATES_URL)
        appinfo.app_updates_url = url

    def _setAuthor(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        for tag in root.findall(self.TAG_AUTHOR):
            language = tag.get(self.ATTRIBUTE_LANGUAGE, '')

            name = _getTextValue(tag, self.TAG_AUTHOR_NAME)
            email = _getTextValue(tag, self.TAG_AUTHOR_EMAIL)
            website = _getTextValue(tag, self.TAG_AUTHOR_WEBSITE)
            author_info = XmlAuthorInfo(name, email, website)

            if language not in appinfo.authors:
                appinfo.authors.set_for_language(language, [])

            appinfo.authors[language].append(author_info)

    def _setVersion(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        tag_version = root.find(self.TAG_VERSION)
        if tag_version is None:
            return

        number = tag_version.get(self.ATTRIBUTE_VERSION_NUMBER)
        status = tag_version.get(self.ATTRIBUTE_VERSION_STATUS, '')

        if number is not None:
            appinfo.version = XmlVersionInfo(number, status)


class XmlAppInfo:
    def __init__(self):
        self.app_info_url = ''                  # type: str
        self.app_updates_url = ''               # type: str

        # Key - language, value - apllication name
        self.app_name = DataForLanguage()       # type: DataForLanguage[str]

        # Key - language, value - URL
        self.website = DataForLanguage()        # type: DataForLanguage[str]

        # Key - language, value - description
        self.description = DataForLanguage()    # type: DataForLanguage[str]

        # Key - language, value - list of authors information
        # type: DataForLanguage[List[XmlAuthorInfo]]
        self.authors = DataForLanguage()

        self.requirements = XmlRequirements([], [])

        # type: Optional[XmlVersionInfo]
        self.version = None


class XmlAuthorInfo:
    """
    Information about plug-in's author
    """

    def __init__(self,
                 name: str = '',
                 email: str = '',
                 website: str = ''):
        self.name = name
        self.email = email
        self.website = website


class XmlRequirements:
    """
    Plug-in's requirements
    """

    def __init__(self, os_list: List[str], api_list: List[Iterable[int]]):
        """
        os_list - list of the supported OS
        api_list - list of the list of the int with supported API versions.
        """
        self.os_list = os_list[:]
        self.api_list = api_list[:]


class XmlRequirementsFactory:
    TAG_REQUIREMENTS = 'requirements'
    TAG_REQUIREMENTS_API = 'api'
    TAG_REQUIREMENTS_OS = 'os'

    @classmethod
    def fromXml(cls, tag_parent: ElementTree.Element) -> 'XmlRequirements':
        os_list = []
        api_list = []

        tag_requirements = tag_parent.find(cls.TAG_REQUIREMENTS)

        if tag_requirements is not None:
            os_list = _getTextList(tag_requirements, cls.TAG_REQUIREMENTS_OS)
            api_list_str = _getTextList(tag_requirements, cls.TAG_REQUIREMENTS_API)
            api_list = []
            for version_str in api_list_str:
                version = cls._parseVersion(version_str)
                if version:
                    api_list.append(version)

        return XmlRequirements(os_list, api_list)

    @classmethod
    def _parseVersion(cls, version_str: str) -> Optional[Iterable[int]]:
        try:
            return tuple((int(item) for item in version_str.split('.')))
        except ValueError:
            return None


class XmlVersionInfo:
    def __init__(self, number: str, status: str = ''):
        self.number = number                # type: str
        self.status = status                # type: str


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
                date = datetime.strptime(date_str, '%d.%m.%Y')
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


class XmlChangeItem:
    def __init__(self, description: str):
        self.description = description


class XmlDownload:
    def __init__(self,
                 href: str,
                 requirements: Optional[XmlRequirements] = None):
        self.href = href
        self.requirements = requirements


class XmlChangeLog:
    def __init__(self):
        self.versions = []                      # type: List[XmlChangeLogVersionInfo]


class XmlChangeLogVersionInfo:
    def __init__(self,
                 number: str,
                 status: str = '',
                 date: Optional[datetime] = None):
        self.number = number                # type: str
        self.status = status                # type: str
        self.date = date                    # type: Optional[datetime]
        self.downloads = []                 # type: List[XmlDownload]

        # Key - language, value - list of XmlChangeItem
        # type: DataForLanguage[List[XmlChangeItem]]
        self.changes = DataForLanguage()
