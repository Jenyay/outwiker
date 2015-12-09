# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


class DownloaderTest (unittest.TestCase):
    def setUp (self):
        self.plugindirlist = [u"../plugins/webpage"]

        self.loader = PluginsLoader(Application)
        self.loader.load (self.plugindirlist)


    def tearDown (self):
        self.loader.clear()
