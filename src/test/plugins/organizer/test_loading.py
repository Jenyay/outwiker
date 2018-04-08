# -*- coding: utf-8 -*-

import unittest

from test.basetestcases import PluginLoadingMixin


class OrganizerLoadingTest(PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        """
        Must return path to plugin
        """
        return "../plugins/organizer"

    def getPluginName(self):
        """
        Must return plugin name
        """
        return "Organizer"
