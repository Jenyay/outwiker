# -*- coding: utf-8 -*-

import urllib2
import logging

from outwiker.core.xmlversionparser import XmlVersionParser

from .i18n import get_
from .loaders import NormalLoader


logger = logging.getLogger('UpdateNotifierPlugin')


class VersionList(object):
    """Класс для получения последних версий плагинов
    и самой программы с сайтов"""
    def __init__(self, updateUrls):
        """
        updateUrls - dict which key is plugin name or other ID,
            value is update url
        """
        global _
        _ = get_()

        self._updateUrls = updateUrls
        self._loader = NormalLoader()
        self._latestInfo = {}

    def updateVersions(self):
        """
        Получить номера версий всех плагинов и самой программы из интернета
        """
        for name, url in self._updateUrls.iteritems():
            logger.info(u"Checking update for {}".format(name))
            appInfo = self._getAppInfoFromUrl(url)
            if appInfo is not None:
                self._latestInfo[name] = appInfo

    def setLoader(self, newloader):
        """
        Метод используется только для тестирования.
        Нужен для эмуляции отсутствия соединения с интернетом.
        """
        self._loader = newloader

    def _getAppInfoFromUrl(self, url):
        """
        url - ссылка, откуда получается номер версии
        """
        if url is None:
            return None

        text = self._loadPage(url)
        if not text:
            logger.warning(u"Can't download {}".format(url))
            return None

        try:
            appinfo = XmlVersionParser([_(u'__updateLang'), u'en']).parse(text)
        except ValueError:
            logger.warning(u'Invalid format of {}'.format(url))
            return None

        return appinfo

    def _loadPage(self, url):
        """
        Загрузка страницы.
        Возвращает текст страницы или пустую строку в случае ошибки
        """
        logger.info(u'Downloading {}'.format(url))
        try:
            text = self._loader.load(url)
        except urllib2.HTTPError:
            text = u""
        except urllib2.URLError:
            text = u""
        except ValueError:
            text = u""

        return text

    def __getitem__(self, key):
        return self._latestInfo.get(key)
