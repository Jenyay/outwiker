# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class ChangePageUIDLoadingTest (BasePluginLoadingTest):
    def getPluginDir (self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return u"../plugins/changepageuid"


    def getPluginName (self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        return "ChangePageUID"
