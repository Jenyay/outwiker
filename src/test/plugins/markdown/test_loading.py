# -*- coding: utf-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class MarkdownLoadingTest (BasePluginLoadingTest):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return "../plugins/markdown"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "Markdown"
