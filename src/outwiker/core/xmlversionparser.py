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
    TAG_VERSION_DOWNLOAD = 'download'
    TAG_DOWNLOAD_URL = 'url'
    TAG_DOWNLOAD_REQUIREMENTS = 'requirements'
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

    #
    # def _getRequirements(self, root):
    #     assert root is not None
    #     requirements_tag = root.find(u'requirements')
    #     if requirements_tag is None:
    #         return None
    #
    #     os_str = self._getTextValue(requirements_tag, u'os')
    #     if os_str is None:
    #         os_str = u''
    #
    #     os_list = [current_os.strip()
    #                for current_os
    #                in os_str.split(u',')
    #                if len(current_os.strip()) != 0]
    #
    #     api_str = self._getTextValue(requirements_tag, u'api')
    #     if api_str is None:
    #         api_str = u''
    #
    #     api_versions = self._parsePackageVersions(api_str)
    #     return RequirementsInfo(os_list, api_versions)
    #
    # def _parsePackageVersions(self, text):
    #     if text is None:
    #         return []
    #     result = []
    #     items = [item.strip()
    #              for item
    #              in text.split(',')
    #              if len(item.strip()) != 0]
    #     for item in items:
    #         elements = item.split('.')
    #         if len(elements) != 2:
    #             continue
    #         try:
    #             version = (int(elements[0]), int(elements[1]))
    #             result.append(version)
    #         except ValueError:
    #             continue
    #
    #     return result
    #
    # def _getVersionsList(self, data_tag):
    #     """
    #     Return list of VersionInfo instance.
    #     List sorted by version (last version is first)
    #     """
    #     result = []
    #     if data_tag is None:
    #         return result
    #
    #     changelog_tag = data_tag.find(u'changelog')
    #     if changelog_tag is None:
    #         return result
    #
    #     for version_tag in changelog_tag.findall(u'version[@number]'):
    #         version = self._getVersionInfo(version_tag)
    #         if version is not None:
    #             result.append(version)
    #
    #     result.sort(key=lambda x: x.version, reverse=True)
    #
    #     return result
    #
    # def _getVersionInfo(self, version_tag):
    #     assert version_tag is not None
    #     version = self._getVersion(version_tag)
    #     if version is None:
    #         return None
    #
    #     date = version_tag.get(u'date', u'')
    #     changes = self._getChanges(version_tag)
    #     downloads = self._getDownloads(version_tag)
    #     requirements = self._getRequirements(version_tag)
    #
    #     return VersionInfo(version,
    #                        date_str=date,
    #                        downloads=downloads,
    #                        changes=changes,
    #                        requirements=requirements)
    #
    # def _getDownloads(self, version_tag):
    #     assert version_tag is not None
    #     downloads = {}
    #     for download in version_tag.findall(u'download'):
    #         os = download.get(u'os', u'all')
    #         url = download.text
    #         if url is not None:
    #             downloads[os] = url
    #     return downloads
    #
    # def _getChanges(self, version_tag):
    #     assert version_tag is not None
    #     changes = []
    #     for change_tag in version_tag.findall(u'change'):
    #         text = change_tag.text
    #         if text is None:
    #             text = u''
    #         changes.append(text)
    #     return changes
    #
    # def _getVersion(self, version_tag):
    #     """
    #     Return Version instance or None if version number is not exists.
    #     """
    #     assert version_tag is not None
    #     try:
    #         number = version_tag.get(u'number')
    #         status = version_tag.get(u'status')
    #         if number is None:
    #             raise ValueError
    #         full_number = (u' '.join([number, status]) if status is not None
    #                        else number)
    #         version = Version.parse(full_number)
    #     except ValueError:
    #         return None
    #     return version
    #
    # def _getAuthorInfo(self, data_tag):
    #     """
    #     Return information about author or None if 'author' tag not exists
    #     """
    #     if data_tag is None:
    #         return None
    #
    #     author_tag = data_tag.find(u'author')
    #     if author_tag is None:
    #         return None
    #
    #     name = self._getTextValue(author_tag, u'name')
    #     email = self._getTextValue(author_tag, u'email')
    #     website = self._getTextValue(author_tag, u'website')
    #     return AuthorInfo(name, email, website)
    #
    # def _getAppWebsite(self, root):
    #     if root is None:
    #         return u''
    #
    #     return self._getTextValue(root, u'website')
    #
    # def _getDescription(self, root):
    #     if root is None:
    #         return u''
    #
    #     return self._getTextValue(root, u'description')

    def _getTextValue(self, root: ElementTree.Element, tag_name: str):
        """
        Return text inside tag with name tag_name or empty string.
        """
        result = None
        result_tag = root.find(tag_name)
        if result_tag is not None and result_tag.text is not None:
            result = result_tag.text

        if result is None:
            result = u''
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
                 api_versions: List[Tuple[int, int]]):
        """
        os_list - list of the supported OS
        api_version - list of the tuples with supported API versions.
        """
        self.os_list = os_list[:]
        self.api_versions = api_versions[:]


class XmlChangeItem:
    def __init__(self, description: str):
        self.description = description


class XmlDownload:
    def __init__(self,
                 url: str,
                 requirements: Optional[XmlRequirements] = None):
        self.url = url
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
