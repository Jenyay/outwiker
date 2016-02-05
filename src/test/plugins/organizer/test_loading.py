# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class OrganizerLoadingTest (BasePluginLoadingTest):
    def getPluginDir (self):
        """
        Must return path to plugin
        """
        return u"../plugins/organizer"


    def getPluginName (self):
        """
        Must return plugin name
        """
        return "Organizer"
