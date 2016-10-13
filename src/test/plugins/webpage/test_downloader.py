# -*- coding: UTF-8 -*-

import os
import os.path
from tempfile import mkdtemp
import urllib
import unittest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.utilites.textfile import readTextFile
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


    def testContentImgExample1 (self):
        from webpage.downloader import Downloader, DownloadController

        template = u'<img src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_01.png'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/картинка.png'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_01_1.png'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_02.png'),
            downloader.contentResult)

        self.assertNotIn (
            template.format (path = self._staticDirName + u'/image_02_1.png'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_03.png'),
            downloader.contentResult)

        self.assertNotIn (
            template.format (path = self._staticDirName + u'/image_03_1.png'),
            downloader.contentResult)


    def testContentCSSExample1_01 (self):
        from webpage.downloader import Downloader, DownloadController

        template = u'<link href="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname1.css'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname2.css'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname3.css'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname4.css'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname1_1.css'),
            downloader.contentResult)

        self.assertNotIn (
            template.format (path = self._staticDirName + u'/fname2_1.css'),
            downloader.contentResult)


    def testContentScriptExample1 (self):
        from webpage.downloader import Downloader, DownloadController

        template = u'<script src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname1.js'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname2.js'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname2_1.js'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname3.js'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/fname4.js'),
            downloader.contentResult)

        self.assertNotIn (
            template.format (path = self._staticDirName + u'/fname1_1.js'),
            downloader.contentResult)


    def testTitleExample1 (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertTrue (downloader.success)
        self.assertEqual (downloader.pageTitle, u'Заголовок страницы')


    def testNoTitle (self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example_no_title/'
        exampleHtmlPath = os.path.join (examplePath, u'example_no_title.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertTrue (downloader.success)
        self.assertIsNone (downloader.pageTitle)


    def testContentExample2 (self):
        from webpage.downloader import Downloader, DownloadController

        template = u'<img src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example2/'
        exampleHtmlPath = os.path.join (examplePath, u'example2.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_01.png'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_01_1.png'),
            downloader.contentResult)

        self.assertIn (
            template.format (path = self._staticDirName + u'/image_02.png'),
            downloader.contentResult)

        self.assertNotIn (
            template.format (path = self._staticDirName + u'/image_02_1.png'),
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
                    u'import1.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'import2.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'import3.css'
                )
            )
        )

        self.assertTrue (
            os.path.exists (
                os.path.join (
                    self._tempDir,
                    self._staticDirName,
                    u'import4.css'
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

        # print os.listdir (os.path.join (self._tempDir, self._staticDirName))

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


    def testDownloading_css_url_01 (self):
        from webpage.downloader import Downloader, DownloadController

        template = u'url("{url}")'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        fname1_text = readTextFile (os.path.join (self._tempDir,
                                                  self._staticDirName,
                                                  u'fname1.css'))

        self.assertIn (template.format (url = u'import1.css'), fname1_text)
        self.assertIn (template.format (url = u'back_img_01.png'), fname1_text)
        self.assertIn (template.format (url = u'back_img_02.png'), fname1_text)
        self.assertIn (template.format (url = u'back_img_03.png'), fname1_text)
        self.assertIn (template.format (url = u'back_img_04.png'), fname1_text)
        self.assertIn (template.format (url = u'back_img_05.png'), fname1_text)
        self.assertIn (template.format (url = u'back_img_06.png'), fname1_text)


    def testDownloading_css_url_02 (self):
        from webpage.downloader import Downloader, DownloadController

        template = u'url("{url}")'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader ()

        examplePath = u'../test/webpage/example1/'
        exampleHtmlPath = os.path.join (examplePath, u'example1.html')

        downloader.start (self._path2url (exampleHtmlPath), controller)

        fname2_text = readTextFile (os.path.join (self._tempDir,
                                                  self._staticDirName,
                                                  u'fname2.css'))

        self.assertIn (template.format (url = u'basic2.css'), fname2_text)
        self.assertIn (template.format (url = u'basic4.css'), fname2_text)
        self.assertIn (template.format (url = u'basic5.css'), fname2_text)
        self.assertIn (template.format (url = u'basic6.css'), fname2_text)
        self.assertIn ('basic3.css', fname2_text)
        self.assertIn ('basic5.css', fname2_text)



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


    @staticmethod
    def _path2url (path):
        path = os.path.abspath(path)
        path = path.encode('utf8')
        return 'file:' + urllib.pathname2url(path)
