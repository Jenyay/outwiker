# -*- coding: utf-8 -*-

import unittest

from outwiker.tests.basetestcases import PluginLoadingMixin


class MarkdownLoadingTest (PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return "plugins/markdown"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "Markdown"
