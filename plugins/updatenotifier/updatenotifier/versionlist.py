# -*- coding: utf-8 -*-

import urllib.error
import logging

from outwiker.core.xmlversionparser import XmlVersionParser

from .i18n import get_
from .loaders import NormalLoader


logger = logging.getLogger('updatenotifier')


class VersionList(object):
    """Class to read latest versions information."""
    def __init__(self, loader=None):
        """
        loader - instance of the loader from loaders.py or other.
            Is used for tests only.
        """
        global _
        _ = get_()

        if loader is None:
            self._loader = NormalLoader()
        else:
            self._loader = loader

    def loadAppInfo(self, updateUrls):
        """
        Load latest versions information.
        updateUrls - dict which key is plugin name or other ID,
            value is update url
        :returns:
            dict {ID: AppInfo}
        """
        latestInfo = {}

        for name, url in updateUrls.items():
            logger.info(u"Checking update for {}".format(name))
            appInfo = self.getAppInfoFromUrl(url)
            if appInfo is not None:
                latestInfo[name] = appInfo

        return latestInfo

    def getAppInfoFromUrl(self, url):
        """
        Get a AppInfo object for url.

        :param url:
            URL of path to file to read versions information.
        :returns:
            AppInfo or None
        """
        if url is None:
            return None

        logger.info(u'Downloading {}'.format(url))

        try:
            text = self._loader.load(url)
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
            logger.warning(u"Can't download {}".format(url))
            return None

        try:
            appinfo = XmlVersionParser([_(u'__updateLang'), u'en']).parse(text)
        except ValueError:
            logger.warning(u'Invalid format of {}'.format(url))
            return None

        if not appinfo.appname.strip():
            return None

        return appinfo
