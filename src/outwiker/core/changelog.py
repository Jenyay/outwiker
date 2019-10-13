# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from .version import Version
from .version_requirements import Requirements


class ChangeItem:
    def __init__(self, description: str):
        self.description = description


class DownloadInfo:
    def __init__(self,
                 href: str,
                 requirements: Optional[Requirements] = None):
        self.href = href
        self.requirements = requirements


class VersionInfo:
    def __init__(self,
                 version: Version,
                 date: Optional[datetime],
                 downloads: 'List[DownloadInfo]',
                 changes: 'List[ChangeItem]'):
        self.version = version
        self.date = date
        self.downloads = downloads
        self.changes = changes


class ChangeLog:
    def __init__(self, versions: List[VersionInfo]):
        self.versions = versions

    @property
    def latestVersion(self) -> Optional[VersionInfo]:
        '''
        Return self.versions item with biggest version number
        '''
        if len(self.versions) == 0:
            return None

        return max(self.versions, key=lambda x: x.version)
