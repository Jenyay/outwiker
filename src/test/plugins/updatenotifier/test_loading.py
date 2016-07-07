# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class UpdateNotifierLoadingTest (BasePluginLoadingTest):
    def getPluginDir (self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return u"../plugins/updatenotifier"


    def getPluginName (self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        return "UpdateNotifier"
