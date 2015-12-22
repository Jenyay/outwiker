# -*- coding: UTF-8 -*-

import os.path
from tempfile import mkdtemp
import urllib
import unittest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from test.utils import removeDir


class RealTest (unittest.TestCase):
    def setUp (self):
        self.plugindirlist = [u'../plugins/webpage']
        self._staticDirName = u'__download'
        self._tempDir = mkdtemp (prefix=u'Абырвалг абыр')

        self.loader = PluginsLoader(Application)
        self.loader.load (self.plugindirlist)


    def tearDown (self):
        self.loader.clear()
        removeDir (self._tempDir)


    def testDownloading_beautifulsoup (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        url = u'http://www.crummy.com/software/BeautifulSoup/bs4/doc/'
        downloader.start (url, controller)

        self.assertTrue (downloader.success)

        downloadDir = os.path.join (self._tempDir, self._staticDirName)
        self.assertTrue (os.path.exists (downloadDir))

        self.assertTrue (os.path.join (
            self._tempDir,
            self._staticDirName,
            u'_static',
            u'default.css')
        )

        self.assertTrue (os.path.join (
            self._tempDir,
            self._staticDirName,
            u'_static',
            u'pygments.css')
        )

        self.assertTrue (os.path.join (
            self._tempDir,
            self._staticDirName,
            u'_static',
            u'jquery.js')
        )

        self.assertTrue (os.path.join (
            self._tempDir,
            self._staticDirName,
            u'_static',
            u'underscore.js')
        )

        self.assertTrue (os.path.join (
            self._tempDir,
            self._staticDirName,
            u'_static',
            u'doctools.js')
        )


    def testDownloading_toster (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        url = u'https://toster.ru/q/273244'
        downloader.start (url, controller)

        self.assertTrue (downloader.success)


    def testDownloading_stackoverflow (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        url = u'http://ru.stackoverflow.com/questions/476918/django-%D0%97%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8-%D0%BE%D1%82-%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B2-%D0%91%D0%94'
        downloader.start (url, controller)

        self.assertTrue (downloader.success)


    def _getTestController (self):
        from webpage.downloader import BaseDownloadController

        class TestController (BaseDownloadController):
            def __init__ (self):
                self.files = []

            def process (self, startUrl, url, node):
                self.files.append ((url, node))

        return TestController()


    @staticmethod
    def _path2url (path):
        path = os.path.abspath(path)
        path = path.encode('utf8')
        return 'file:' + urllib.pathname2url(path)
