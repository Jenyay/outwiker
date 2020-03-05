# -*- coding: utf-8 -*-

from typing import List

from .changelog import ChangeItem, ChangeLog, DownloadInfo, VersionInfo
from .version import Version
from .version_requirements_factory import RequirementsFactory
from .xmlchangelog import XmlChangeItem, XmlChangeLog, XmlDownload
from .xmlchangelogparser import XmlChangelogParser


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
            changes_xml = xmlversion.changes.get(language, [])[:]
            changes = cls._getChanges(changes_xml)
            downloads = cls._getDownloads(xmlversion.downloads)

            versions.append(VersionInfo(version, date, downloads, changes))

        return versions

    @classmethod
    def _getChanges(cls, changes_xml: List[XmlChangeItem]) -> List[ChangeItem]:
        return [ChangeItem(change.description) for change in changes_xml]

    @classmethod
    def _getDownloads(cls, xmldownloads: List[XmlDownload]) -> List[DownloadInfo]:
        downloads = []

        for xmldownload in xmldownloads:
            requirements = RequirementsFactory.fromXmlRequirements(
                xmldownload.requirements)
            download = DownloadInfo(xmldownload.href, requirements)
            downloads.append(download)

        return downloads
