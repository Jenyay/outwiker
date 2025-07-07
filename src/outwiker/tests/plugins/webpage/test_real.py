# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class RealTest(BaseOutWikerGUIMixin, unittest.TestCase):
    def setUp(self):
        self.initApplication()
        self.plugindirlist = ['plugins/webpage']
        self._staticDirName = '__download'
        self._tempDir = mkdtemp(prefix='Абырвалг абыр')

        self.loader = PluginsLoader(self.application)
        self.loader.load(self.plugindirlist)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        removeDir(self._tempDir)

    @unittest.skip("Too slow")
    def testDownloading_beautifulsoup(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        url = 'http://www.crummy.com/software/BeautifulSoup/bs4/doc/'
        downloader.start(url, controller)

        self.assertTrue(downloader.success)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)
        self.assertTrue(os.path.exists(downloadDir))

        self.assertTrue(os.path.join(
            self._tempDir,
            self._staticDirName,
            'default.css')
        )

        self.assertTrue(os.path.join(
            self._tempDir,
            self._staticDirName,
            'pygments.css')
        )

        self.assertTrue(os.path.join(
            self._tempDir,
            self._staticDirName,
            'jquery.js')
        )

        self.assertTrue(os.path.join(
            self._tempDir,
            self._staticDirName,
            'underscore.js')
        )

        self.assertTrue(os.path.join(
            self._tempDir,
            self._staticDirName,
            'doctools.js')
        )

    @unittest.skip("Too slow")
    def testDownloading_toster(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        url = 'https://toster.ru/q/273244'
        downloader.start(url, controller)

        self.assertTrue(downloader.success)

    @unittest.skip("Too slow")
    def testDownloading_stackoverflow_01(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        url = 'http://ru.stackoverflow.com/questions/476918/django-%D0%97%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8-%D0%BE%D1%82-%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B2-%D0%91%D0%94'
        downloader.start(url, controller)

        self.assertTrue(downloader.success)

    @unittest.skip("Too slow")
    def testDownloading_stackoverflow_2(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        url = 'https://ru.stackoverflow.com/questions/241337/Как-обработать-кириллические-символы-в-urllib-request-urlopen'
        downloader.start(url, controller)

        self.assertTrue(downloader.success)
