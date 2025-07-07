# -*- coding: utf-8 -*-

import os
import os.path
from tempfile import mkdtemp
import urllib.request
import urllib.parse
import urllib.error
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.utilites.textfile import readTextFile
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class DownloaderTest(BaseOutWikerGUIMixin, unittest.TestCase):
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

    def testContentImgExample1(self):
        from webpage.downloader import Downloader, DownloadController

        template = '<img src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_01.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/картинка.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_01_1.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_02.png'),
            downloader.contentResult)

        self.assertNotIn(
            template.format(path=self._staticDirName + '/image_02_1.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_03.png'),
            downloader.contentResult)

        self.assertNotIn(
            template.format(path=self._staticDirName + '/image_03_1.png'),
            downloader.contentResult)

    def testContentCSSExample1_01(self):
        from webpage.downloader import Downloader, DownloadController

        template = '<link href="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname1.css'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname2.css'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname3.css'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname4.css'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname1_1.css'),
            downloader.contentResult)

        self.assertNotIn(
            template.format(path=self._staticDirName + '/fname2_1.css'),
            downloader.contentResult)

    def testContentScriptExample1(self):
        from webpage.downloader import Downloader, DownloadController

        template = '<script src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname1.js'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname2.js'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname2_1.js'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname3.js'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/fname4.js'),
            downloader.contentResult)

        self.assertNotIn(
            template.format(path=self._staticDirName + '/fname1_1.js'),
            downloader.contentResult)

    def testTitleExample1(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertTrue(downloader.success)
        self.assertEqual(downloader.pageTitle, 'Заголовок страницы')

    def testNoTitle(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example_no_title/'
        exampleHtmlPath = os.path.join(examplePath, 'example_no_title.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertTrue(downloader.success)
        self.assertIsNone(downloader.pageTitle)

    def testContentExample2(self):
        from webpage.downloader import Downloader, DownloadController

        template = '<img src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example2/'
        exampleHtmlPath = os.path.join(examplePath, 'example2.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_01.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_01_1.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/image_02.png'),
            downloader.contentResult)

        self.assertNotIn(
            template.format(path=self._staticDirName + '/image_02_1.png'),
            downloader.contentResult)

    def testDownloading_img_01(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_01.png')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_02.png')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_03.png')

        fname4 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_01_1.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))
        self.assertTrue(os.path.exists(fname4))

    def testDownloading_img_02(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example2/'
        exampleHtmlPath = os.path.join(examplePath, 'example2.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_01.png')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_02.png')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_03.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))

    def testDownloading_img_03(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/Пример 3/'
        exampleHtmlPath = os.path.join(examplePath, 'пример 3.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_01.png')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_02.png')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_03.png')

        fname4 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_01_1.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))
        self.assertTrue(os.path.exists(fname4))

    def testDownloading_img_urlquote(self):
        from webpage.downloader import Downloader, DownloadController

        template = '<img src="{path}"'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example_urlquote/'
        exampleHtmlPath = os.path.join(examplePath, 'example_urlquote.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname = os.path.join(self._tempDir, self._staticDirName, 'рисунок.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname))

        self.assertIn(
            template.format(path=self._staticDirName + '/рисунок.png'),
            downloader.contentResult)

    def testDownloading_favicon_01(self):
        from webpage.downloader import Downloader, DownloadController

        template = 'href="{path}"'
        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example_favicon_01/'
        exampleHtmlPath = os.path.join(examplePath, 'example.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        fname_1 = os.path.join(
            self._tempDir, self._staticDirName, 'favicon_1.png')
        fname_2 = os.path.join(
            self._tempDir, self._staticDirName, 'favicon_2.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname_1))
        self.assertTrue(os.path.exists(fname_2))

        self.assertIn(
            template.format(path=self._staticDirName + '/favicon_1.png'),
            downloader.contentResult)

        self.assertIn(
            template.format(path=self._staticDirName + '/favicon_2.png'),
            downloader.contentResult)

        self.assertEqual(controller.favicon,
                         os.path.join(self._tempDir, self._staticDirName) + '/favicon_1.png')

    def testDownloading_favicon_02(self):
        from webpage.downloader import Downloader, DownloadController

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example_favicon_02/'
        exampleHtmlPath = os.path.join(examplePath, 'example.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        favicon_fname = os.path.join(
            self._tempDir, self._staticDirName, 'favicon.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertEqual(controller.favicon,
                         os.path.join(self._tempDir, self._staticDirName) + '/favicon.png')
        self.assertTrue(os.path.exists(favicon_fname))

    def testDownloading_favicon_03(self):
        from webpage.downloader import Downloader, DownloadController

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example_favicon_03/'
        exampleHtmlPath = os.path.join(examplePath, 'example.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        favicon_fname = os.path.join(
            self._tempDir, self._staticDirName, 'favicon.ico')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertEqual(controller.favicon,
                         os.path.join(self._tempDir, self._staticDirName) + '/favicon.ico')
        self.assertTrue(os.path.exists(favicon_fname))

    def testDownloading_css_rename(self):
        from webpage.downloader import Downloader, DownloadController

        template = 'href="{path}"'
        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example_css_rename/'
        exampleHtmlPath = os.path.join(examplePath, 'example.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        fname = os.path.join(
            self._tempDir, self._staticDirName, 'style.php.css')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname))

        self.assertIn(
            template.format(path=self._staticDirName + '/style.php.css'),
            downloader.contentResult)

    def testDownloading_img_srcset_files(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example3/'
        exampleHtmlPath = os.path.join(examplePath, 'example3.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_01.png')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_02.png')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_03.png')

        fname4 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'image_04.png')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))
        self.assertTrue(os.path.exists(fname4))

    def testDownloading_img_srcset_content(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example3/'
        exampleHtmlPath = os.path.join(examplePath, 'example3.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)
        downloadDir = os.path.join(self._tempDir, self._staticDirName)
        content = downloader.contentResult

        sample = 'srcset="{path}/image_02.png 2x, {path}/image_03.png w600, {path}/image_04.png"'.format(path=self._staticDirName)

        self.assertIn(sample, content)

    def testDownloading_css_01(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname1.css')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname2.css')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname3.css')

        fname4 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname4.css')

        fname5 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname1_1.css')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))
        self.assertTrue(os.path.exists(fname4))
        self.assertTrue(os.path.exists(fname5))

    def testDownloading_css_import_01(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'import1.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'import2.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'import3.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'import4.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'basic2.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'basic3.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'basic4.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'basic5.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'basic5_1.css'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'basic6.css'
                )
            )
        )

    def testDownloading_css_back_img_01(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'back_img_01.png'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'back_img_02.png'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'back_img_03.png'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'back_img_04.png'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'back_img_05.png'
                )
            )
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self._tempDir,
                    self._staticDirName,
                    'back_img_06.png'
                )
            )
        )

    def testDownloading_css_url_01(self):
        from webpage.downloader import Downloader, DownloadController

        template = 'url("{url}")'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        fname1_text = readTextFile(os.path.join(self._tempDir,
                                                self._staticDirName,
                                                'fname1.css'))

        self.assertIn(template.format(url='import1.css'), fname1_text)
        self.assertIn(template.format(url='back_img_01.png'), fname1_text)
        self.assertIn(template.format(url='back_img_02.png'), fname1_text)
        self.assertIn(template.format(url='back_img_03.png'), fname1_text)
        self.assertIn(template.format(url='back_img_04.png'), fname1_text)
        self.assertIn(template.format(url='back_img_05.png'), fname1_text)
        self.assertIn(template.format(url='back_img_06.png'), fname1_text)

    def testDownloading_css_url_02(self):
        from webpage.downloader import Downloader, DownloadController

        template = 'url("{url}")'

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        fname2_text = readTextFile(os.path.join(self._tempDir,
                                                self._staticDirName,
                                                'fname2.css'))

        self.assertIn(template.format(url='basic2.css'), fname2_text)
        self.assertIn(template.format(url='basic4.css'), fname2_text)
        self.assertIn(template.format(url='basic5.css'), fname2_text)
        self.assertIn(template.format(url='basic6.css'), fname2_text)
        self.assertIn('basic3.css', fname2_text)
        self.assertIn('basic5.css', fname2_text)

    def testDownloading_css_03(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/Пример 3/'
        exampleHtmlPath = os.path.join(examplePath, 'пример 3.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname1.css')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname2.css')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname3.css')

        fname4 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname4.css')

        fname5 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname1_1.css')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))
        self.assertTrue(os.path.exists(fname4))
        self.assertTrue(os.path.exists(fname5))

    def testDownloading_javascript_01(self):
        from webpage.downloader import Downloader, DownloadController

        controller = DownloadController(self._tempDir, self._staticDirName)
        downloader = Downloader()

        examplePath = 'testdata/webpage/example1/'
        exampleHtmlPath = os.path.join(examplePath, 'example1.html')

        downloader.start(self._path2url(exampleHtmlPath), controller)

        downloadDir = os.path.join(self._tempDir, self._staticDirName)

        fname1 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname1.js')

        fname2 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname2.js')

        fname3 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname3.js')

        fname4 = os.path.join(self._tempDir,
                              self._staticDirName,
                              'fname4.js')

        self.assertTrue(os.path.exists(downloadDir))
        self.assertTrue(os.path.exists(fname1))
        self.assertTrue(os.path.exists(fname2))
        self.assertTrue(os.path.exists(fname3))
        self.assertTrue(os.path.exists(fname4))

    @staticmethod
    def _path2url(path):
        path = os.path.abspath(path)
        return 'file:' + urllib.request.pathname2url(path)
