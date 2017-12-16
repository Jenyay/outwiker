# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class DiagrammerLoadingTest (BasePluginLoadingTest):
    def getPluginDir (self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "../plugins/diagrammer"


    def getPluginName (self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        return "Diagrammer"
