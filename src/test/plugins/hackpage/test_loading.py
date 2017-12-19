# -*- coding: UTF-8 -*-

from test.plugins.baseloading import BasePluginLoadingTest


class HackPage_LoadingTest (BasePluginLoadingTest):
    def getPluginDir(self):
        return "../plugins/hackpage"

    def getPluginName(self):
        return "HackPage"
