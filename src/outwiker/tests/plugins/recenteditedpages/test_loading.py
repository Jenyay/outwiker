# -*- coding: utf-8 -*-

import unittest

from outwiker.tests.basetestcases import PluginLoadingMixin


class PluginNameLoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return "plugins/recenteditedpages"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "RecentEditedPages"
