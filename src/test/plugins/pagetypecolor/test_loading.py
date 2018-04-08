# -*- coding: utf-8 -*-

import unittest

from test.basetestcases import PluginLoadingMixin


class PageTypeColor_LoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return "../plugins/pagetypecolor"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "PageTypeColor"
