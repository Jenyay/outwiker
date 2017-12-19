# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class SnippetsLoadingTest (BasePluginLoadingTest):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return "../plugins/snippets"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "Snippets"
