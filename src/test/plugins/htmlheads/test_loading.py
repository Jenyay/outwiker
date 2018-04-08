# -*- coding: utf-8 -*-

import unittest

from test.basetestcases import PluginLoadingMixin


class HtmlHeadsLoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "../plugins/htmlheads"

    def getPluginName(self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        return "HtmlHeads"
