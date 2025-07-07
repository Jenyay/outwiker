# -*- coding: utf-8 -*-

import unittest

from outwiker.tests.basetestcases import PluginLoadingMixin


class WebPageLoadingTest (PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "plugins/webpage"

    def getPluginName(self):
        """
        Должен возвращать имя плагина,
        по которому его можно найти в PluginsLoader
        """
        return "WebPage"

    def getInitApplicationParams(self):
        return {"createTreePanel": True}
