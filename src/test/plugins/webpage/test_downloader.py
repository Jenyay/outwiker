# -*- coding: UTF-8 -*-

import os.path
import urllib
import unittest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


class DownloaderTest (unittest.TestCase):
    def setUp (self):
        self.plugindirlist = [u'../plugins/webpage']
        self._staticDirName = u'download'

        self.loader = PluginsLoader(Application)
        self.loader.load (self.plugindirlist)


    def tearDown (self):
        self.loader.clear()


    def testEmpty (self):
        from webpage.downloader import Downloader
        downloader = Downloader (self._staticDirName)

        fname = self._path2url (u'../test/webpage/empty.html')
        downloader.start (fname)


    @staticmethod
    def _path2url (path):
        path = os.path.abspath(path)
        path = path.encode('utf8')
        return 'file:' + urllib.pathname2url(path)
