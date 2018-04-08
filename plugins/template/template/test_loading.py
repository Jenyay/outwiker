# -*- coding: utf-8 -*-

import unittest

from test.basetestcases import PluginLoadingMixin


class PluginNameLoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return u"../plugins/pluginname"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "PluginName"
