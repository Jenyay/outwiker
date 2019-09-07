# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from outwiker.core.version import Version


class AppInfo:
    def __init__(self,
                 app_name: str = '',
                 app_info_url: str = '',
                 website: str = '',
                 description: str = '',
                 author: 'Optional[AuthorInfo]' = None,
                 versions: 'Optional[List[VersionInfo]]' = None,
                 requirements: 'Optional[Requirements]' = None):
        self.app_name = app_name
        self.app_info_url = app_info_url
        self.website = website
        self.description = description

        self.author = author if author is not None else AuthorInfo()
        self.versions = versions if versions is not None else []
        self.requirements = (
            requirements if requirements is not None else Requirements([], []))

    @property
    def currentVersion(self) -> Optional[Version]:
        version_info = max(
            self.versions,
            key=lambda versioninfo: versioninfo.version, default=None)
        return version_info.version if version_info is not None else None


class AuthorInfo:
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


class Requirements:
    """
    Plug-in's requirements
    """

    def __init__(self,
                 os_list: List[str],
                 api_list: List[Version]):
        """
        os_list - list of the supported OS
        api_list - list of the tuples with supported API versions.
        """
        self.os_list = os_list[:]
        self.api_list = api_list[:]


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
