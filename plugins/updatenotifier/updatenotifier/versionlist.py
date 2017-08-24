# -*- coding: utf-8 -*-

import urllib2
import logging
import os

from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile

from .i18n import get_
import loaders


logger = logging.getLogger('UpdateNotifierPlugin')


class VersionList(object):
    """Класс для получения последних версий плагинов
    и самой программы с сайтов"""
    def __init__(self, plugins):
        """
        plugins - экземпляр класса PluginsLoader
        """
        global _
        _ = get_()

        self._plugins = plugins

        self._loader = loaders.NormalLoader()

        # Номера версий OutWiker
        self._outwikerStableVersion = None
        # self._outwikerStablePage = _(u"http://jenyay.net/Outwiker/English")

        self._outwikerUnstableVersion = None
        # self._outwikerUnstablePage = _(u"http://jenyay.net/Outwiker/UnstableEn")

        # Без загрузки версий все версии равны None
        self._pluginsInfo = {plugin.name: None for plugin in self._plugins}
        self._pluginPages = self._getPluginPages()
        self._pluginsInfoList = self._getPluginsInfo()

    def _getPluginsInfo(self):
        result = {}

        for plugin in self._plugins:
            xmlPath = os.path.join(plugin._pluginPath,
                                   PLUGIN_VERSION_FILE_NAME)
            try:
                xmlText = readTextFile(xmlPath)
            except IOError:
                logger.warning(u"Can't read {}".format(xmlPath))
                continue

            try:
                result[plugin.name] = XmlVersionParser([_(u'__updateLang')]).parse(xmlText)
            except ValueError:
                logger.warning(u"Invalid format {}".format(xmlPath))
                continue

        return result

    def updateVersions(self):
        """
        Получить номера версий всех плагинов и самой программы из интернета
        """
        # self._outwikerStableVersion = self._getVersionFromPage(
        #     self._outwikerStablePage)
        #
        # self._outwikerUnstableVersion = self._getVersionFromPage(
        #     self._outwikerUnstablePage)

        for plugin in self._plugins:
            logger.info(u"Checking update for {}".format(plugin.name))
            appInfo = self._getAppInfoFromUrl(
                self._pluginsInfoList[plugin.name].updatesUrl)
            if appInfo is not None:
                self._pluginsInfo[plugin.name] = appInfo

    def setLoader(self, newloader):
        """
        Метод используется только для тестирования. Нужен для эмуляции отсутствия соединения с интернетом.
        """
        self._loader = newloader

    def _getPluginPages(self):
        """
        Составить словарь, где ключем будет имя плагина, а значением ссылка на страницу плагина. При этом учитывается, что в старых плагинах не было свойства url
        """
        oldPluginPages = {u"ExternalTools": _(u"http://jenyay.net/Outwiker/ExternalToolsEn"),
                          u"Lightbox": _(u"http://jenyay.net/Outwiker/LightboxEn"),
                          u"Livejournal": _(u"http://jenyay.net/Outwiker/LivejournalPluginEn"),
                          u"Spoiler": _(u"http://jenyay.net/Outwiker/SpoilerEn"),
                          u"Style": _(u"http://jenyay.net/Outwiker/StylePluginEn"),
                          u"ThumbGallery": _(u"http://jenyay.net/Outwiker/ThumbGalleryEn"),
                          }

        pluginPages = {}

        for plugin in self._plugins:
            if "url" in dir(plugin):
                url = plugin.url
            elif plugin.name in oldPluginPages:
                url = oldPluginPages[plugin.name]
            else:
                url = None

            pluginPages[plugin.name] = url

        return pluginPages

    def _getAppInfoFromUrl(self, url):
        """
        url - ссылка, откуда получается номер версии
        versionname - название версии(stable, unstable и т.п.)
        """
        if url is None:
            return None

        text = self._loadPage(url)
        if not text:
            logger.warning(u"Can't download {}".format(url))
            return None

        try:
            appinfo = XmlVersionParser([_(u'__updateLang')]).parse(text)
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

    def getPluginInfo(self, pluginname):
        return self._pluginsInfo[pluginname]

    @property
    def stableVersion(self):
        """
        Возвращает номер стабильной версии OutWiker, которая лежит на сайте программы
        """
        return self._outwikerStableVersion

    @property
    def unstableVersion(self):
        """
        Возвращает номер нестабильной версии OutWiker, которая лежит на сайте программы
        """
        return self._outwikerUnstableVersion
