# -*- coding: UTF-8 -*-

from xml.etree import ElementTree

from outwiker.core.appinfo import AppInfo, AuthorInfo, VersionInfo
from version import Version, Status


class XmlVersionParser (object):
    """
    Class to read and write application info in XML format.
    """
    def __init__(self, langlist=[u'en'], skipHidden=True):
        """
        langlist - list of the languages name ("en", "ru_RU" etc)
        """
        self._langlist = langlist
        self._skipHidden = skipHidden

    def parse(self, text):
        """
        Return AppInfo instance
        """
        try:
            root = ElementTree.fromstring(text.encode('utf8'))
        except ElementTree.ParseError:
            appinfo = AppInfo(u'', None)
            return appinfo

        name = self._getTextValue(root, u'name')
        updatesUrl = self._getTextValue(root, u'updates')

        # Get data tag for selected language
        data_tag = self._getDataTag (root)
        appwebsite = self._getAppWebsite (data_tag)
        description = self._getDescription (data_tag)

        appinfo = AppInfo(name,
                          author=None,
                          appwebsite=appwebsite,
                          description=description,
                          updatesUrl=updatesUrl)
        return appinfo

    def _getDataTag(self, root):
        data_tag = None
        for lang in self._langlist:
            data_tag = root.find('./data[@lang="{}"]'.format(lang))
            if data_tag is not None:
                break
        return data_tag

    def _getAppWebsite(self, root):
        if root is None:
            return u''

        return self._getTextValue(root, u'website')

    def _getDescription(self, root):
        if root is None:
            return u''

        return self._getTextValue(root, u'description')

    def _getTextValue(self, root, tagname):
        """
        Return text inside tag with name tagname or empty string.
        """
        result = None
        result_tag = root.find(tagname)
        if result_tag is not None:
            result = result_tag.text

        if result is None:
            result = u''
        return result
