# -*- coding: utf-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class PluginNameLoadingTest(BasePluginLoadingTest):
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
