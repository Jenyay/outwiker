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
        controller = self._getTestController()
        downloader = Downloader (self._staticDirName)

        fname = self._path2url (u'../test/webpage/example0/example0.html')
        downloader.start (fname, controller)
        self.assertIn (u'<html>', downloader.content_src)
        self.assertEqual (downloader.pageTitle, None)


    def testExample1 (self):
        from webpage.downloader import Downloader
        controller = self._getTestController()
        downloader = Downloader (self._staticDirName)

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)
        self.assertEqual (downloader.pageTitle, u'Заголовок страницы')

        imagePath_01 = os.path.join (examplePath, u'image_01.png')
        self.assertEqual (controller.files[0][0], self._path2url (imagePath_01))

        imagePath_02 = u'file:///images/image_02.png'
        self.assertEqual (controller.files[1][0], imagePath_02)

        imagePath_03 = os.path.join (examplePath, u'images', u'image_03.png')
        self.assertEqual (controller.files[2][0], self._path2url (imagePath_03))

        imagePath_04 = os.path.join (examplePath,
                                     u'images',
                                     u'subfolder',
                                     u'image_04.png')
        self.assertEqual (controller.files[3][0], self._path2url (imagePath_04))


    def _getTestController (self):
        from webpage.downloader import BaseDownloadController

        class TestController (BaseDownloadController):
            def __init__ (self):
                self.files = []

            def process (self, url, node):
                self.files.append ((url, node))

        return TestController()


    @staticmethod
    def _path2url (path):
        path = os.path.abspath(path)
        path = path.encode('utf8')
        return 'file:' + urllib.pathname2url(path)
