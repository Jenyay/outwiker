# -*- coding: utf-8 -*-

from xml.etree import ElementTree
from typing import List, Tuple, Optional, Dict, TypeVar, Generic, Any


T = TypeVar('T')


class XmlVersionParser:
    """
    Class to read and write application info in XML format.
    """
    ATTRIBUTE_LANGUAGE = 'lang'

    TAG_APP_NAME = 'name'
    TAG_WEBSITE = 'website'
    TAG_DESCRIPTION = 'description'
    TAG_APP_INFO_URL = 'updates'
    TAG_AUTHOR = 'author'
    TAG_AUTHOR_NAME = 'name'
    TAG_AUTHOR_EMAIL = 'email'
    TAG_AUTHOR_WEBSITE = 'website'
    TAG_VERSIONS = 'versions'
    TAG_VERSIONS_VERSION = 'version[@number]'
    ATTRIBUTE_VERSION_NUMBER = 'number'
    ATTRIBUTE_VERSION_STATUS = 'status'
    ATTRIBUTE_VERSION_DATE = 'date'
    TAG_VERSION_CHANGES = 'changes'
    TAG_CHANGES_CHANGE = 'change'
    TAG_VERSION_DOWNLOAD = 'download[@href]'
    TAG_DOWNLOAD_REQUIREMENTS = 'requirements'
    ATTRIBUTE_DOWNLOAD_HREF = 'href'
    TAG_REQUIREMENTS_API = 'api'
    TAG_REQUIREMENTS_OS = 'os'

    def parse(self, text: str) -> 'XmlAppInfo':
        appinfo = XmlAppInfo()

        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError:
            return appinfo

        self._setAppInfoUrl(root, appinfo)
        self._setAppName(root, appinfo)
        self._setWebsite(root, appinfo)
        self._setDescription(root, appinfo)
        self._setAuthor(root, appinfo)
        self._setVersions(root, appinfo)

        return appinfo

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
        url = self._getTextValue(root, self.TAG_APP_INFO_URL)
        appinfo.app_info_url = url

    def _setAuthor(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        for tag in root.findall(self.TAG_AUTHOR):
            language = tag.get(self.ATTRIBUTE_LANGUAGE, '')

            name = self._getTextValue(tag, self.TAG_AUTHOR_NAME)
            email = self._getTextValue(tag, self.TAG_AUTHOR_EMAIL)
            website = self._getTextValue(tag, self.TAG_AUTHOR_WEBSITE)
            author_info = XmlAuthorInfo(name, email, website)

            appinfo.author.set_for_language(language, author_info)

    def _setVersions(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        tag_versions = root.find(self.TAG_VERSIONS)
        if tag_versions is None:
            return

        for tag_version in tag_versions.findall(self.TAG_VERSIONS_VERSION):
            number = tag_version.get(self.ATTRIBUTE_VERSION_NUMBER)
            assert number is not None

            status = tag_version.get(self.ATTRIBUTE_VERSION_STATUS, '')
            date = tag_version.get(self.ATTRIBUTE_VERSION_DATE, '')
            version_info = XmlVersionInfo(number, status, date)

            self._setChangeLog(tag_version, version_info.changes)
            self._addDownloads(tag_version, version_info.downloads)

            appinfo.versions.append(version_info)

    def _setChangeLog(self,
                      tag_version: ElementTree.Element,
                      changes: 'DataForLanguage[List[XmlChangeItem]]'):
        for tag_changes in tag_version.findall(self.TAG_VERSION_CHANGES):
            language = tag_changes.get(self.ATTRIBUTE_LANGUAGE, '')
            changes_list = []
            for tag_change in tag_changes.findall(self.TAG_CHANGES_CHANGE):
                change_text = tag_change.text if tag_change.text is not None else ''
                change_item = XmlChangeItem(change_text)
                changes_list.append(change_item)

            changes.set_for_language(language, changes_list)

    def _addDownloads(self,
                      tag_version: ElementTree.Element,
                      downloads: 'List[XmlDownload]'):
        for tag_download in tag_version.findall(self.TAG_VERSION_DOWNLOAD):
            href = tag_download.get(self.ATTRIBUTE_DOWNLOAD_HREF)
            assert href is not None

            requirements = self._getRequirements(tag_download)
            download = XmlDownload(href, requirements)
            downloads.append(download)

    def _getRequirements(self, tag_download: ElementTree.Element) -> 'XmlRequirements':
        os_list = []
        api_list = []

        tag_requirements = tag_download.find(self.TAG_DOWNLOAD_REQUIREMENTS)
        if tag_requirements is not None:
            os_list = self._getTextList(
                tag_requirements, self.TAG_REQUIREMENTS_OS)
            api_list = self._getTextList(
                tag_requirements, self.TAG_REQUIREMENTS_API)

        return XmlRequirements(os_list, api_list)

    def _getTextValue(self, root: ElementTree.Element, tag_name: str) -> str:
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

    def _getTextList(self, root: ElementTree.Element, tag_name: str) -> List[str]:
        """
        Return text list from tags with name tag_name
        """
        result = []

        for tag in root.findall(tag_name):
            text = tag.text if tag.text is not None else ''
            result.append(text)

        return result


class DataForLanguage(Generic[T]):
    def __init__(self):
        # Key - language, value - data
        self._data = {}             # type: Dict[str, T]

    def set_for_language(self, language: str, data: T) -> None:
        self._data[language] = data

    def __getitem__(self, language: str) -> T:
        return self._data[language]

    def __contains__(self, language: str) -> bool:
        return language in self._data

    def get(self, language: str, default: Any = None) -> Any:
        return self._data.get(language, default)

    def get_languages(self) -> List[str]:
        return list(self._data.keys())

    def is_empty(self) -> bool:
        return len(self._data) == 0


class XmlAppInfo:
    def __init__(self):
        self.app_info_url = ''                  # type: str

        # Key - language, value - apllication name
        self.app_name = DataForLanguage()       # type: DataForLanguage[str]

        # Key - language, value - URL
        self.website = DataForLanguage()        # type: DataForLanguage[str]

        # Key - language, value - description
        self.description = DataForLanguage()    # type: DataForLanguage[str]

        # Key - language, value - author information
        # type: DataForLanguage[XmlAuthorInfo]
        self.author = DataForLanguage()

        self.versions = []                      # type: List[XmlVersionInfo]


class XmlAuthorInfo:
    """
    Information about plug-in's author
    """

    def __init__(self,
                 name: str = u"",
                 email: str = u"",
                 website: str = u""):
        self.name = name
        self.email = email
        self.website = website


class XmlRequirements:
    """
    Plug-in's requirements
    """

    def __init__(self,
                 os_list: List[str],
                 api_list: List[Tuple[int, int]]):
        """
        os_list - list of the supported OS
        api_list - list of the tuples with supported API versions.
        """
        self.os_list = os_list[:]
        self.api_list = api_list[:]


class XmlChangeItem:
    def __init__(self, description: str):
        self.description = description


class XmlDownload:
    def __init__(self,
                 href: str,
                 requirements: Optional[XmlRequirements] = None):
        self.href = href
        self.requirements = requirements


class XmlVersionInfo:
    def __init__(self,
                 number: str,
                 status: str = '',
                 date: str = ''):
        self.number = number                # type: str
        self.status = status                # type: str
        self.date = date                    # type: str

        self.downloads = []                 # type: List[XmlDownload]

        # Key - language, value - list of XmlChangeItem
        # type: DataForLanguage[List[XmlChangeItem]]
        self.changes = DataForLanguage()
