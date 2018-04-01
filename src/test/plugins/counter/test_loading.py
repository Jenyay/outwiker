# -*- coding: utf-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class CounterLoadingTest(BasePluginLoadingTest):
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "../plugins/counter"

    def getPluginName(self):
        """
        Должен возвращать имя плагина,
        по которому его можно найти в PluginsLoader
        """
        return "Counter"
