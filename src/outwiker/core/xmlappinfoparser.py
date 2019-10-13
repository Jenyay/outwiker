# -*- coding: utf-8 -*-

from xml.etree import ElementTree

from .dataforlanguage import DataForLanguage
from .xmlappinfo import XmlAppInfo, XmlAuthorInfo, XmlVersionInfo
from .version_xmlrequirements_factory import XmlRequirementsFactory


class XmlAppInfoParser:
    """
    Class to read and write application info in XML format.
    """
    ATTRIBUTE_LANGUAGE = 'lang'

    TAG_APP_NAME = 'name'
    TAG_WEBSITE = 'website'
    TAG_DESCRIPTION = 'description'
    TAG_AUTHOR = 'author'
    TAG_AUTHOR_NAME = 'name'
    TAG_AUTHOR_EMAIL = 'email'
    TAG_AUTHOR_WEBSITE = 'website'
    TAG_VERSION = 'version'
    ATTRIBUTE_VERSION_NUMBER = 'number'
    ATTRIBUTE_VERSION_STATUS = 'status'

    def parse(self, text: str) -> 'XmlAppInfo':
        appinfo = XmlAppInfo()

        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError:
            return appinfo

        self._setAppName(root, appinfo)
        self._setWebsite(root, appinfo)
        self._setDescription(root, appinfo)
        self._setAuthor(root, appinfo)
        self._setVersion(root, appinfo)
        self._setRequirements(root, appinfo)

        return appinfo

    def _setRequirements(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        requirements = XmlRequirementsFactory.fromXml(root)
        appinfo.requirements.os_list = requirements.os_list[:]
        appinfo.requirements.api_list = requirements.api_list[:]

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

    def _setAuthor(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        for tag in root.findall(self.TAG_AUTHOR):
            language = tag.get(self.ATTRIBUTE_LANGUAGE, '')

            name = self._getTextValue(tag, self.TAG_AUTHOR_NAME)
            email = self._getTextValue(tag, self.TAG_AUTHOR_EMAIL)
            website = self._getTextValue(tag, self.TAG_AUTHOR_WEBSITE)
            author_info = XmlAuthorInfo(name, email, website)

            if language not in appinfo.authors:
                appinfo.authors.set_for_language(language, [])

            appinfo.authors[language].append(author_info)

    def _setVersion(self, root: ElementTree.Element, appinfo: 'XmlAppInfo'):
        tag_version = root.find(self.TAG_VERSION)
        if tag_version is None:
            return

        number = tag_version.get(self.ATTRIBUTE_VERSION_NUMBER)
        status = tag_version.get(self.ATTRIBUTE_VERSION_STATUS, '')

        if number is not None:
            appinfo.version = XmlVersionInfo(number, status)

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
