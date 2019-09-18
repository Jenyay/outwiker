# -*- coding: utf-8 -*-

from typing import List, Optional

from .xmlappinfoparser import (XmlAppInfoParser, XmlAppInfo, XmlDownload,
                               XmlRequirements, DataForLanguage, XmlChangeLog,
                               XmlChangelogParser, T)
from .appinfo import (AppInfo, AuthorInfo, VersionInfo, DownloadInfo,
                      Requirements, ChangeLog)
from .version import Version


def extractDataForLanguage(data: DataForLanguage[T],
                           language: str,
                           default: T) -> T:
    DEFAULT_LANGUAGE = ''
    # lang_list example: ['ru_RU', 'ru', '']
    lang_list = [language]
    underscore_pos = language.find('_')
    if underscore_pos != -1:
        lang_list.append(language[: underscore_pos])
    lang_list.append(DEFAULT_LANGUAGE)

    for current_lang in lang_list:
        if current_lang in data:
            return data[current_lang]

    return default


class AppInfoFactory:
    '''
    Class to create AppInfo instance
    '''

    @classmethod
    def fromString(cls, text: str, language: str) -> AppInfo:
        xmlAppInfo = XmlAppInfoParser().parse(text)         # type: XmlAppInfo
        return cls.fromXmlAppInfo(xmlAppInfo, language)

    @classmethod
    def fromXmlAppInfo(cls,
                       xmlAppInfo: XmlAppInfo,
                       language: str) -> AppInfo:
        app_info_url = xmlAppInfo.app_info_url

        app_name = extractDataForLanguage(
            xmlAppInfo.app_name, language, '')

        website = extractDataForLanguage(xmlAppInfo.website, language, '')

        description = extractDataForLanguage(
            xmlAppInfo.description, language, '')

        authors = cls._getAuthors(xmlAppInfo, language)
        version = cls._getVersion(xmlAppInfo)
        requirements = RequirementsFactory.fromXmlRequirements(
            xmlAppInfo.requirements)

        result = AppInfo(app_info_url=app_info_url,
                         app_name=app_name,
                         website=website,
                         description=description,
                         authors=authors,
                         requirements=requirements,
                         version=version
                         )
        return result

    @classmethod
    def _getVersion(cls, xmlAppInfo: XmlAppInfo) -> Optional[Version]:
        if xmlAppInfo.version is None:
            return None

        return Version.parse(xmlAppInfo.version.number +
                             ' ' + xmlAppInfo.version.status)

    @classmethod
    def _getAuthors(cls, xmlAppInfo: XmlAppInfo, language: str) -> List[AuthorInfo]:
        return [AuthorInfo(author.name, author.email, author.website)
                for author in extractDataForLanguage(xmlAppInfo.authors,
                                                     language, [])]


class ChangeLogFactory:
    @classmethod
    def fromXmlChangeLog(cls,
                         xmlChangeLog: XmlChangeLog,
                         language: str) -> ChangeLog:
        versions = cls._getVersions(xmlChangeLog, language)
        return ChangeLog(versions)

    @classmethod
    def fromString(cls, text: str, language: str) -> ChangeLog:
        xmlChangeLog = XmlChangelogParser.parse(text)     # type: XmlChangeLog
        return cls.fromXmlChangeLog(xmlChangeLog, language)

    @classmethod
    def _getVersions(cls,
                     xmlChangeLog: XmlChangeLog,
                     language: str) -> List[VersionInfo]:
        versions = []
        for xmlversion in xmlChangeLog.versions:
            try:
                version = Version.parse('{} {}'.format(
                    xmlversion.number, xmlversion.status))
            except ValueError:
                continue

            date = xmlversion.date
            changes = extractDataForLanguage(
                xmlversion.changes, language, [])[:]
            downloads = cls._getDownloads(xmlversion.downloads)

            versions.append(VersionInfo(version, date, downloads, changes))

        return versions

    @classmethod
    def _getDownloads(cls, xmldownloads: List[XmlDownload]) -> List[DownloadInfo]:
        downloads = []

        for xmldownload in xmldownloads:
            requirements = RequirementsFactory.fromXmlRequirements(
                xmldownload.requirements)
            download = DownloadInfo(xmldownload.href, requirements)
            downloads.append(download)

        return downloads


class RequirementsFactory:
    @classmethod
    def fromXmlRequirements(cls, requirements: XmlRequirements) -> Requirements:
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
