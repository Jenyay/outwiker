# -*- coding: utf-8 -*-

import unittest

from outwiker.tests.basetestcases import PluginLoadingMixin


class HackPage_LoadingTest (PluginLoadingMixin, unittest.TestCase):
    def getPluginDir(self):
        return "plugins/hackpage"

    def getPluginName(self):
        return "HackPage"
