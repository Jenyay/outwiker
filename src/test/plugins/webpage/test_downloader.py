# -*- coding: UTF-8 -*-

import os.path
from tempfile import mkdtemp
import urllib
import unittest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from test.utils import removeDir


class DownloaderTest (unittest.TestCase):
    def setUp (self):
        self.plugindirlist = [u'../plugins/webpage']
        self._staticDirName = u'__download'
        self._tempDir = mkdtemp (prefix=u'Абырвалг абыр')

        self.loader = PluginsLoader(Application)
        self.loader.load (self.plugindirlist)


    def tearDown (self):
        self.loader.clear()
        removeDir (self._tempDir)


    def testEmpty (self):
        from webpage.downloader import Downloader
        controller = self._getTestController()
        downloader = Downloader ()

        fname = self._path2url (u'../test/webpage/example0/example0.html')
        downloader.start (fname, controller)
        self.assertIn (u'<html>', downloader.contentSrc)
        self.assertEqual (downloader.pageTitle, None)


    def testExample1 (self):
        from webpage.downloader import Downloader
        controller = self._getTestController()
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)
        self.assertEqual (downloader.pageTitle, u'Заголовок страницы')

        self.assertEqual (controller.files[0][0], u'image_01.png')
        self.assertEqual (controller.files[1][0], u'/images/image_invalid.png')
        self.assertEqual (controller.files[2][0], u'images/image_02.png')
        self.assertEqual (controller.files[3][0],
                          u'images/subfolder/image_03.png')


    def testContentExample1 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertIn (self._staticDirName + u'/image_01.png',
                       downloader.contentResult)

        self.assertIn (self._staticDirName + u'/image_02.png',
                       downloader.contentResult)

        self.assertIn (self._staticDirName + u'/image_03.png',
                       downloader.contentResult)


    def testContentExample2 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example2/'
        exampleHtmlPath = os.path.join (examplePath, u'example2.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertIn (self._staticDirName + u'/image_01.png',
                       downloader.contentResult)

        self.assertIn (self._staticDirName + u'/image_02.png',
                       downloader.contentResult)

        self.assertIn (self._staticDirName + u'/image_03.png',
                       downloader.contentResult)


    def testDownloading_img_01 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        downloadDir = os.path.join (self._tempDir, self._staticDirName)

        fname1 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_01.png')

        fname2 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_02.png')

        fname3 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_03.png')

        fname4 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_01_1.png')

        self.assertTrue (os.path.exists (downloadDir))
        self.assertTrue (os.path.exists (fname1))
        self.assertTrue (os.path.exists (fname2))
        self.assertTrue (os.path.exists (fname3))
        self.assertTrue (os.path.exists (fname4))


    def testDownloading_img_02 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example2/'
        exampleHtmlPath = os.path.join (examplePath, u'example2.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        downloadDir = os.path.join (self._tempDir, self._staticDirName)

        fname1 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_01.png')

        fname2 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_02.png')

        fname3 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'image_03.png')

        self.assertTrue (os.path.exists (downloadDir))
        self.assertTrue (os.path.exists (fname1))
        self.assertTrue (os.path.exists (fname2))
        self.assertTrue (os.path.exists (fname3))


    def testDownloading_css_01 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        downloadDir = os.path.join (self._tempDir, self._staticDirName)

        fname1 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname1.css')

        fname2 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname2.css')

        fname3 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname3.css')

        fname4 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname4.css')

        fname5 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname1_1.css')

        self.assertTrue (os.path.exists (downloadDir))
        self.assertTrue (os.path.exists (fname1))
        self.assertTrue (os.path.exists (fname2))
        self.assertTrue (os.path.exists (fname3))
        self.assertTrue (os.path.exists (fname4))
        self.assertTrue (os.path.exists (fname5))


    def testDownloading_css_import_01 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic1.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic2.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic3.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic4.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic5.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic5_1.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'basic6.css'
                )
            )
        )


    def testDownloading_css_back_img_01 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'back_img_01.png'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'back_img_02.png'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'back_img_03.png'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'back_img_04.png'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'back_img_05.png'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'back_img_06.png'
                )
            )
        )


    def testDownloading_javascript_01 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        downloadDir = os.path.join (self._tempDir, self._staticDirName)

        fname1 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname1.js')

        fname2 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname2.js')

        fname3 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname3.js')

        fname4 = os.path.join (self._tempDir,
                               self._staticDirName,
                               u'fname4.js')

        self.assertTrue (os.path.exists (downloadDir))
        self.assertTrue (os.path.exists (fname1))
        self.assertTrue (os.path.exists (fname2))
        self.assertTrue (os.path.exists (fname3))
        self.assertTrue (os.path.exists (fname4))


    def _getTestController (self):
        from webpage.downloader import BaseDownloadController

        class TestController (BaseDownloadController):
            def __init__ (self):
                self.files = []


            def processImg (self, startUrl, url, node):
                self._process (startUrl, url, node)


            def processCSS (self, startUrl, url, node):
                self._process (startUrl, url, node)


            def processScript (self, startUrl, url, node):
                self._process (startUrl, url, node)


            def _process (self, startUrl, url, node):
                self.files.append ((url, node))

        return TestController()


    @staticmethod
    def _path2url (path):
        path = os.path.abspath(path)
        path = path.encode('utf8')
        return 'file:' + urllib.pathname2url(path)
