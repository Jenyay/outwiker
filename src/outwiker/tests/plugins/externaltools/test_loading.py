# -*- coding: utf-8 -*-

import unittest

from outwiker.tests.basetestcases import PluginLoadingMixin


class ExternalToolsLoadingTest(PluginLoadingMixin, unittest.TestCase):

    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "plugins/externaltools"

    def getPluginName(self):
        """
        Должен возвращать имя плагина, по которому его можно найти в PluginsLoader
        """
        return "ExternalTools"
