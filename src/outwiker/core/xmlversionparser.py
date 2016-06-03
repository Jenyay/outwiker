# -*- coding: UTF-8 -*-

from xml.etree import ElementTree

from outwiker.core.appinfo import AppInfo, AuthorInfo, VersionInfo
from version import Version, Status


class XmlVersionParser (object):
    """
    Class to read and write application info in XML format.
    """
    def __init__(self, language=u'en', langDefault=u'en'):
        """
        language - language name ("en", "ru_RU" etc)
        """
        self._language = language
        self._langDefault = langDefault

    def parse(self, text):
        """
        Return AppInfo instance
        """
        try:
            root = ElementTree.fromstring(text.encode('utf8'))
        except ElementTree.ParseError:
            appinfo = AppInfo(u'', None)
            return appinfo

        name = self._getAppName(root)
        appinfo = AppInfo(name, None)
        return appinfo

    def _getAppName(self, root):
        """
        Return name of application or plug-in
        """
        name = None
        name_tag = root.find('name')
        if name_tag is not None:
            name = name_tag.text

        if name is None:
            name = u''
        return name
