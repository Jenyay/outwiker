# -*- coding: utf-8 -*-

import unittest

from test.basetestcases import PluginLoadingMixin


class TexEquationLoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        return "../plugins/texequation"

    def getPluginName(self):
        """
        Должен возвращать имя плагина,
        по которому его можно найти в PluginsLoader
        """
        return "TeXEquation"
