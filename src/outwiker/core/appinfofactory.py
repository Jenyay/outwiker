# -*- coding: utf-8 -*-

from typing import List, Optional

from .xmlversionparser import (XmlVersionParser, XmlAppInfo, XmlDownload,
                               XmlRequirements, DataForLanguage, T)
from .appinfo import (AppInfo, AuthorInfo, VersionInfo, DownloadInfo,
                      Requirements)
from .version import Version


class AppInfoFactory:
    '''
    Class to create AppInfo instance
    '''
    DEFAULT_LANGUAGE = ''

    @classmethod
    def fromString(cls, text: str, language: str) -> AppInfo:
        xmlAppInfo = XmlVersionParser().parse(text)         # type: XmlAppInfo
        return cls.fromXmlAppInfo(xmlAppInfo, language)

    @classmethod
    def fromXmlAppInfo(cls,
                       xmlAppInfo: XmlAppInfo,
                       language: str) -> AppInfo:
        app_info_url = xmlAppInfo.app_info_url

        app_name = cls.extractDataForLanguage(
            xmlAppInfo.app_name, language, '')

        website = cls.extractDataForLanguage(xmlAppInfo.website, language, '')

        description = cls.extractDataForLanguage(
            xmlAppInfo.description, language, '')

        author = cls._getAuthor(xmlAppInfo, language)
        version = cls._getVersion(xmlAppInfo)
        versions = cls._getVersions(xmlAppInfo, language)
        requirements = cls._getRequirements(xmlAppInfo.requirements)

        result = AppInfo(app_info_url=app_info_url,
                         app_name=app_name,
                         website=website,
                         description=description,
                         author=author,
                         versions=versions,
                         requirements=requirements,
                         version=version
                         )
        return result

    @classmethod
    def extractDataForLanguage(cls,
                               data: DataForLanguage[T],
                               language: str,
                               default: T) -> T:
        # lang_list example: ['ru_RU', 'ru', '']
        lang_list = [language]
        underscore_pos = language.find('_')
        if underscore_pos != -1:
            lang_list.append(language[: underscore_pos])
        lang_list.append(cls.DEFAULT_LANGUAGE)

        for current_lang in lang_list:
            if current_lang in data:
                return data[current_lang]

        return default

    @classmethod
    def _getVersion(cls, xmlAppInfo: XmlAppInfo) -> Optional[Version]:
        if xmlAppInfo.version is None:
            return None

        return Version.parse(xmlAppInfo.version.number +
                             ' ' + xmlAppInfo.version.status)

    @classmethod
    def _getVersions(cls, xmlAppInfo: XmlAppInfo, language: str):
        versions = []
        for xmlversion in xmlAppInfo.versions:
            try:
                version = Version.parse('{} {}'.format(
                    xmlversion.number, xmlversion.status))
            except ValueError:
                continue

            date = xmlversion.date
            changes = cls.extractDataForLanguage(
                xmlversion.changes, language, [])[:]
            downloads = cls._getDownloads(xmlversion.downloads)

            versions.append(VersionInfo(version, date, downloads, changes))

        return versions

    @classmethod
    def _getDownloads(cls, xmldownloads: List[XmlDownload]) -> List[DownloadInfo]:
        downloads = []

        for xmldownload in xmldownloads:
            requirements = cls._getRequirements(xmldownload.requirements)
            download = DownloadInfo(xmldownload.href, requirements)
            downloads.append(download)

        return downloads

    @classmethod
    def _getRequirements(cls, requirements: XmlRequirements) -> Requirements:
        if requirements is None:
            return Requirements([], [])

        os_list = requirements.os_list[:]
        api_list = []
        for api_version_str in requirements.api_list:
            try:
                version = Version.parse(api_version_str)
                api_list.append(version)
            except ValueError:
                continue

        return Requirements(os_list, api_list)

    @classmethod
    def _getAuthor(cls, xmlAppInfo: XmlAppInfo, language: str):
        author_default = AuthorInfo()
        author_src = cls.extractDataForLanguage(
            xmlAppInfo.author, language, author_default)
        author = AuthorInfo(
            author_src.name, author_src.email, author_src.website)
        return author
