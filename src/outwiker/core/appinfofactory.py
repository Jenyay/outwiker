# -*- coding: utf-8 -*-

from typing import List, Optional

from .xmlappinfoparser import XmlAppInfoParser
from .xmlappinfo import XmlAppInfo
from .appinfo import AppInfo, AuthorInfo
from .version import Version
from .version_requirements_factory import RequirementsFactory


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
