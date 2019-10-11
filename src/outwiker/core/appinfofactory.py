# -*- coding: utf-8 -*-

from typing import List, Optional

from .xmlappinfoparser import (XmlAppInfoParser, XmlAppInfo, XmlDownload,
                               XmlRequirements, XmlChangeLog,
                               XmlChangelogParser)
from .appinfo import (AppInfo, AuthorInfo, VersionInfo, DownloadInfo,
                      Requirements, ChangeLog)
from .version import Version


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
        app_name = xmlAppInfo.app_name.get(language, '')

        website = xmlAppInfo.website.get(language, '')

        description = xmlAppInfo.description.get(language, '')

        authors = cls._getAuthors(xmlAppInfo, language)
        version = cls._getVersion(xmlAppInfo)
        requirements = RequirementsFactory.fromXmlRequirements(
            xmlAppInfo.requirements)

        result = AppInfo(app_name=app_name,
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
                for author in xmlAppInfo.authors.get(language, [])]


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
            changes = xmlversion.changes.get(language, [])[:]
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
        api_list = requirements.api_list[:]
        return Requirements(os_list, api_list)
