# -*- coding: utf-8 -*-

import unittest

from test.basetestcases import PluginLoadingMixin


class Export2HtmlLoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "../plugins/export2html"

    def getPluginName(self):
        """
        Должен возвращать имя плагина,
        по которому его можно найти в PluginsLoader
        """
        return "Export2Html"
