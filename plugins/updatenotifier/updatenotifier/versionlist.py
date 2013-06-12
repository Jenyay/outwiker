#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.version import Version

from .i18n import get_


class VersionList (object):
    """Класс для получения последних версий плагинов и самой программы с сайтов"""
    def __init__(self, plugins):
        """
        plugins - экземпляр класса PluginsLoader
        """
        global _
        _ = get_()

        self._plugins = plugins

        # Номера версий OutWiker
        self._outwikerStableVersion = None
        self._outwikerStablePage = _(u"http://jenyay.net/Outwiker/English")

        self._outwikerUnstableVersion = None
        self._outwikerUnstablePage = _(u"http://jenyay.net/Outwiker/UnstableEn")

        # Без загрузки версий все версии равны None
        self._pluginsVersion = {plugin.name: None for plugin in self._plugins}
        self._pluginPages = self._getPluginPages ()


    def _getPluginPages (self):
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
            if "url" in dir (plugin):
                url = plugin.url
            elif plugin.name in oldPluginPages:
                url = oldPluginPages[plugin.name]
            else:
                url = None

            pluginPages[plugin.name] = url

        return pluginPages


    def updateVersions (self):
        """
        Получить номера версий всех плагинов и самой программы из интернета
        """
        self._outwikerStableVersion = self._getVersionFromPage (self._outwikerStablePage)
        self._outwikerUnstableVersion = self._getVersionFromPage (self._outwikerUnstablePage)

        for plugin in self._plugins:
            self._pluginsVersion[plugin.name] = self._getVersionFromPage (self._pluginPages[plugin.name])


    def _getVersionFromPage (self, url):
        if url == None:
            return None
        

    def getPluginVersion (self, pluginname):
        return self._pluginsVersion[pluginname]


    def getStableVersion (self):
        return self._outwikerStableVersion


    def getUnstableVersion (self):
        return self._outwikerUnstableVersion
