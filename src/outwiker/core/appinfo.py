# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Tuple


class AppInfo (object):
    """
    Common for OutWiker and plug-ins items.

    Added in OutWiker 2.0.0.795.
    """
    def __init__(self,
                 appname: str,
                 author: 'AuthorInfo',
                 versionsList: List['VersionInfo']=[],
                 description: str=u"",
                 appwebsite: str=u"",
                 updatesUrl: str=u"",
                 requirements: Optional['RequirementsInfo']=None):
        """
        appname - application or plug-in name.
        author - author info. It is instance of the AuthorInfo class.
        versionsList - information about every version.
                       It is a list of the VersionInfo class.
        description - application's or plug-in's description.
        appwebsite - application or plug-in web site.
        updatesUrl - URL to XML file with updates information.
        """
        self.appname = appname
        self.author = author
        self.versionsList = versionsList[:]
        self.versionsList.sort(key=lambda v: v.version, reverse=True)
        self.description = description
        self.appwebsite = appwebsite
        self.updatesUrl = updatesUrl
        self.requirements = requirements

    @property
    def currentVersion(self):
        if len(self.versionsList) == 0:
            return None
        return self.versionsList[0].version

    @property
    def currentVersionStr(self):
        if self.currentVersion is None:
            return None

        return str(self.currentVersion)


class AuthorInfo (object):
    """
    Information about plug-in's author
    """
    def __init__(self, name: str=u"", email: str=u"", website: str=u""):
        self.name = name
        self.email = email
        self.website = website


class VersionInfo (object):
    """
    Information about single version (version, change log, URL to download)
    """
    def __init__(self,
                 version: 'outwiker.core.Version',
                 date_str: str=u"",
                 downloads: Dict[str, str]={},
                 changes: List[str]=[],
                 hidden: bool=False):
        """
        version   - instance of the Version class.
        date_str  - release date (string)
        downloads - dict with downloads links
                      (key - OS (name from the System class), value - URL)
        changes   - list of the string with changes in current version.
        hidden    - hide this version to users?
        """
        self.version = version
        self.date_str = date_str
        self.downloads = downloads.copy()
        self.changes = changes[:]
        self.hidden = hidden


class RequirementsInfo (object):
    """
    Plug-in's requirements
    """
    def __init__(self,
                 os_list: List[str],
                 api_version: List[Tuple[int, int]]):
        """
        os_list - list of the supported OS
        api_version - list of the tuples with supported API versions.
        """
        self.os = os_list[:]
        self.api_version = api_version[:]
