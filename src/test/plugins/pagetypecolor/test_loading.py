# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class PageTypeColor_LoadingTest(BasePluginLoadingTest):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return u"../plugins/pagetypecolor"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "PageTypeColor"
