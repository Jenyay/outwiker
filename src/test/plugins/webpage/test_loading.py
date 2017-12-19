# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class WebPageLoadingTest (BasePluginLoadingTest):
    def getPluginDir (self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "../plugins/webpage"


    def getPluginName (self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        return "WebPage"
