# -*- coding: utf-8 -*-

import os.path
import unittest

from outwiker.core.tree import WikiDocument
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.utilites.textfile import readTextFile
from outwiker.core.defines import PAGE_RESULT_HTML

from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUIMixin


class Export2HtmlTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.outputdir = "../test/temp"
        self.pluginname = "Export2Html"

        self.path = "../test/samplewiki"
        self.root = WikiDocument.load(self.path)

        dirlist = ["../plugins/export2html"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        removeDir(self.outputdir)

        os.mkdir(self.outputdir)

        Application.wikiroot = None

    def tearDown(self):
        Application.wikiroot = None
        removeDir(self.outputdir)
        self.destroyApplication()

    def testLoading(self):
        self.assertEqual(len(self.loader), 1)
        self.loader[self.pluginname]

    def testExporterPage(self):
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"
        exporter = ExporterFactory.getExporter(self.root[pagename])

        self.assertEqual(exporter.page, self.root[pagename])

    def testExportSinglePage(self):
        """
        Тест на создание файлов и страниц
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"

        exporter = ExporterFactory.getExporter(self.root[pagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=False,
                        alwaysOverwrite=False)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename +
                    ".html")))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    pagename +
                    ".html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir, pagename)))
        self.assertTrue(os.path.isdir(os.path.join(self.outputdir, pagename)))

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "__icon.png")))

        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    "__index.html")))
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    PAGE_RESULT_HTML)))

    def testExportWithName(self):
        """
        Тест на то, что мы можем изменять имя файла и папки для экспорта
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"
        exportname = "Бла-бла-бла"

        exporter = ExporterFactory.getExporter(self.root[pagename])
        exporter.export(outdir=self.outputdir,
                        exportname=exportname,
                        imagesonly=False,
                        alwaysOverwrite=False)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    exportname +
                    ".html")))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    exportname +
                    ".html")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    exportname)))
        self.assertTrue(
            os.path.isdir(
                os.path.join(
                    self.outputdir,
                    exportname)))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    exportname,
                    "__icon.png")))

    def testAttachesSinglePage(self):
        """
        Тест на то, что прикрепленные файлы копируются
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"
        exporter = ExporterFactory.getExporter(self.root[pagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=False,
                        alwaysOverwrite=False)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "__init__.py")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "source.py")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "add.png")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "memorial.gif")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "wall.gif")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "image.tif")))

    def testAttachesImagesSinglePage(self):
        """
        Тест на то, что копируются только прикрепленные картинки
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"

        exporter = ExporterFactory.getExporter(self.root[pagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "__init__.py")))
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "source.py")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "add.png")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "memorial.gif")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "wall.gif")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "image.tif")))

    def testLinkToFilesHtml(self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на HTML-странице
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"

        exporter = ExporterFactory.getExporter(self.root[pagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        text = readTextFile(os.path.join(self.outputdir, pagename + ".html"))

        self.assertTrue(
            '<img src="{pagename}/add.png">'.format(pagename=pagename) in text)

        self.assertTrue(
            '<img alt="Картинка" src="{pagename}/add.png" border="1">'.format(pagename=pagename) in text)

        self.assertTrue(
            '<a href="{pagename}/wall1.gif">ссылка на файл</a>.'.format(pagename=pagename) in text)

        self.assertTrue(
            '<a title="Это title" href="{pagename}/wall1.gif">ссылка на файл</a>.'.format(
                pagename=pagename) in text)

        self.assertTrue(
            '<a href="{pagename}/wall1.gif" title="Это title">ссылка на файл</a>.'.format(
                pagename=pagename) in text)

        self.assertTrue('А этот __attach/ содержится в тексте' in text)

        self.assertFalse('<img src="__attach/add.png">' in text)

    def testLinkToFilesHtmlWithName(self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на HTML-странице
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"
        exportname = "Бла-бла-бла"

        exporter = ExporterFactory.getExporter(self.root[pagename])
        exporter.export(outdir=self.outputdir,
                        exportname=exportname,
                        imagesonly=True,
                        alwaysOverwrite=False)

        text = readTextFile(os.path.join(self.outputdir, exportname + ".html"))

        self.assertTrue(
            '<img src="{pagename}/add.png">'.format(pagename=exportname) in text)
        self.assertTrue(
            '<a href="{pagename}/wall1.gif">ссылка на файл</a>.'.format(pagename=exportname) in text)
        self.assertTrue('А этот __attach/ содержится в тексте' in text)

    def testLinkToFilesWiki(self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/wiki-страница"
        pagename = "wiki-страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        text = readTextFile(os.path.join(self.outputdir, pagename + ".html"))

        self.assertTrue(
            '<img src="{pagename}/add.png"/>'.format(pagename=pagename) in text)
        self.assertTrue(
            '<a href="{pagename}/wall1.gif">ссылка на файл</a>'.format(pagename=pagename) in text)
        self.assertTrue('А этот __attach/ содержится в тексте' in text)
        self.assertTrue(
            '<a href="{pagename}/image.jpg"><img src="{pagename}/__thumb/th_maxsize_250_image.jpg"/></a>'.format(
                pagename=pagename) in text)

    def testLinkToFilesWikiWithName(self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/wiki-страница"
        exportname = "Бла-бла-бла"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=exportname,
                        imagesonly=True,
                        alwaysOverwrite=False)

        text = ""

        with open(os.path.join(self.outputdir, exportname + ".html"), encoding='utf8') as fp:
            text = fp.read()

        self.assertTrue(
            '<img src="{pagename}/add.png"/>'.format(pagename=exportname) in text)
        self.assertTrue(
            '<a href="{pagename}/wall1.gif">ссылка на файл</a>'.format(pagename=exportname) in text)
        self.assertTrue('А этот __attach/ содержится в тексте' in text)
        self.assertTrue(
            '<a href="{pagename}/image.jpg"><img src="{pagename}/__thumb/th_maxsize_250_image.jpg"/></a>'.format(
                pagename=exportname) in text)

    def testWikiPageThumb(self):
        """
        Проверка на то, что сохраняется папка __thumb
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/wiki-страница"
        pagename = "wiki-страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "image.jpg")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "__thumb")))

    def testFilesExportTextPage(self):
        """
        Экспорт текстовой страницы
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/Текстовая страница"
        pagename = "Текстовая страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=False,
                        alwaysOverwrite=False)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename +
                    ".html")))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    pagename +
                    ".html")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir, pagename)))
        self.assertTrue(os.path.isdir(os.path.join(self.outputdir, pagename)))

    def testAttachesExportTextPage(self):
        """
        Экспорт текстовой страницы
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/Текстовая страница"
        pagename = "Текстовая страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=False,
                        alwaysOverwrite=False)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "__init__.py")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "source.py")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "anchor.png")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "application.png")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "box.png")))

    def testHtmlFromTextPage(self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/Текстовая страница"
        pagename = "Текстовая страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        text = ""

        with open(os.path.join(self.outputdir, pagename + ".html"), encoding='utf8') as fp:
            text = fp.read()

        self.assertTrue(
            '&lt;a href=&quot;http://jenyay.net&quot;&gt;bla-bla-bla&lt;/a&gt;' in text)

    def testTextTemplate(self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/Текстовая страница"
        pagename = "Текстовая страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])

        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        text = ""

        with open(os.path.join(self.outputdir, pagename + ".html"), encoding='utf8') as fp:
            text = fp.read()

        self.assertTrue('<head>' in text)
        self.assertTrue('</head>' in text)
        self.assertTrue('<body>' in text)
        self.assertTrue('</body>' in text)
        self.assertTrue('<pre>' in text)
        self.assertTrue('</pre>' in text)
        self.assertTrue('<title>Текстовая страница</title>' in text)

    def testAttachesImagesExportTextPage(self):
        """
        Экспорт текстовой страницы
        """
        from export2html.exporterfactory import ExporterFactory

        fullpagename = "Типы страниц/Текстовая страница"
        pagename = "Текстовая страница"

        exporter = ExporterFactory.getExporter(self.root[fullpagename])
        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=True,
                        alwaysOverwrite=False)

        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "__init__.py")))
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "source.py")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "anchor.png")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "application.png")))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    pagename,
                    "box.png")))

    def testFileExists(self):
        """
        Тест на то, что создаваемый файл уже может существовать
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Страница 1"
        exporter = ExporterFactory.getExporter(self.root[pagename])

        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=False,
                        alwaysOverwrite=False)

        self.assertRaises(BaseException,
                          exporter.export,
                          outdir=self.outputdir,
                          exportname=pagename,
                          imagesonly=False,
                          alwaysOverwrite=False)

        exporter.export(outdir=self.outputdir,
                        exportname=pagename,
                        imagesonly=False,
                        alwaysOverwrite=True)

    def testInvalidFormat(self):
        """
        Проверка на попытку экспортировать страницу, которая не может быть сохранена в HTML (страница поиска)
        """
        from export2html.exporterfactory import ExporterFactory

        pagename = "Типы страниц/Страница поиска"

        self.assertRaises(BaseException,
                          ExporterFactory.getExporter,
                          page=self.root[pagename])

    def testExportBranchFiles(self):
        """
        Экспорт дерева
        """
        from export2html.longnamegenerator import LongNameGenerator
        from export2html.branchexporter import BranchExporter

        pagename = "Страница 1"
        namegenerator = LongNameGenerator(self.root[pagename])
        branchExporter = BranchExporter(
            self.root[pagename], namegenerator, Application)

        result = branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        self.assertEqual(len(result), 0)

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename)))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + ".html")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename, "__icon.png")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2.html")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2", "__icon.gif")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 5")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 5.html")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 5", "__icon.gif")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 6")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 6.html")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 6", "__icon.png")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 6_Страница 7")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 6_Страница 7.html")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + "_Страница 2_Страница 6_Страница 7", "__icon.png")))

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    "__index.html")))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    "__index.html")))

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    PAGE_RESULT_HTML)))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    PAGE_RESULT_HTML)))

    def testExportBranchRoot(self):
        """
        Экспорт, начиная с корня дерева
        """
        from export2html.longnamegenerator import LongNameGenerator
        from export2html.branchexporter import BranchExporter

        wikiname = "samplewiki"
        namegenerator = LongNameGenerator(self.root)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        result = branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        self.assertEqual(len(result), 1)
        self.assertTrue("Страница поиска" in result[0])

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2_Страница 5")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2_Страница 5.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2_Страница 6")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2_Страница 6.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2_Страница 6_Страница 7")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    wikiname + "_Страница 1_Страница 2_Страница 6_Страница 7.html")))

    def testExportBranchFilesTitleNames(self):
        """
        Экспорт дерева с короткими именами
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        pagename = "Страница 1"
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(
            self.root[pagename], namegenerator, Application)

        result = branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        self.assertEqual(len(result), 0, str(result))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename)))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    pagename + ".html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 2")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 2.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 2 (1)")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 2 (1).html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 2 (2)")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 2 (2).html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 5")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 5.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 6")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 6.html")))

        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 7")))
        self.assertTrue(os.path.exists(os.path.join(self.outputdir,
                                                    "Страница 7.html")))

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    "__index.html")))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    "__index.html")))

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.outputdir,
                    PAGE_RESULT_HTML)))
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.outputdir,
                    PAGE_RESULT_HTML)))

    def testBranchContentTitleNames1(self):
        """
        Экспорт дерева с короткими именами
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        pagename = "Страница 1"
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(
            self.root[pagename], namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (1).html"))

        self.assertTrue('<img src="Страница 2 (1)/cake.png"/>' in text)
        self.assertTrue(
            '<a href="Страница 2 (1)/calendar.png">calendar.png</a>' in text)

    def testBranchContentTitleNames2(self):
        """
        Экспорт дерева с короткими именами
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        pagename = "Страница 1"
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(
            self.root[pagename], namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (2).html"))

        self.assertTrue('<img src="Страница 2 (2)/cd.png"/>' in text)
        self.assertTrue(
            '<a href="Страница 2 (2)/cd_go.png">cd_go.png</a>' in text)

    def testLinkToPagesHtmlLongNames(self):
        """
        Тест для проверки того, как исправляются ссылки на страницы
        """
        from export2html.longnamegenerator import LongNameGenerator
        from export2html.branchexporter import BranchExporter

        pagename = "Страница 1"
        namegenerator = LongNameGenerator(self.root[pagename])
        branchExporter = BranchExporter(
            self.root[pagename], namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 1_Страница 2_Страница 6.html"))

        self.assertTrue('<A HREF="/Типы страниц">/Типы страниц</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 1_Страница 2_Страница 6_Страница 7_Страница 2.html">/Страница 1/Страница 2/Страница 6/Страница 7/Страница 2</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 1_Страница 2_Страница 6_Страница 7_Страница 2.html">Страница 7/Страница 2</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 1_Страница 2_Страница 6_Страница 7_Страница 2.html">Еще одна ссылка</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 1_Страница 2_Страница 6_Страница 7.html">Страница 7</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 1_Страница 2_Страница 6_Страница 7_Страница 2.html" title="бла-бла-бла">Ссылка на /Страница 1/Страница 2/Страница 6/Страница 7/Страница 2</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 1_Страница 2_Страница 6_Страница 7.html" title="бла-бла-бла">Ссылка на Страницу 7</A>' in text)

    def testLinkToPagesHtmlTitleNames(self):
        """
        Тест для проверки того, как исправляются ссылки на страницы
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        pagename = "Страница 1"
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(
            self.root[pagename], namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(os.path.join(self.outputdir, "Страница 6.html"))

        self.assertTrue('<A HREF="/Типы страниц">/Типы страниц</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 2 (2).html">/Страница 1/Страница 2/Страница 6/Страница 7/Страница 2</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 2 (2).html">Страница 7/Страница 2</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 2 (2).html">Еще одна ссылка</A>' in text)

        self.assertTrue('<A HREF="Страница 7.html">Страница 7</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 2 (2).html" title="бла-бла-бла">Ссылка на /Страница 1/Страница 2/Страница 6/Страница 7/Страница 2</A>' in text)

        self.assertTrue(
            '<A HREF="Страница 7.html" title="бла-бла-бла">Ссылка на Страницу 7</A>' in text)

    def testLinkToPageByProticolLongNames(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.longnamegenerator import LongNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = LongNameGenerator(self.root)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "samplewiki_Страница 1.html"))

        self.assertIn(
            '<a href="samplewiki_Страница 1_Страница 2_Страница 6_Страница 7_Страница 2.html">',
            text)

    def testLinkToPageByProticolTitleNames_01(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(os.path.join(self.outputdir, "Страница 1.html"))

        self.assertIn('<a href="Страница 2 (2).html">', text)

    def testLinkToPageByProticolTitleNames_02(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (2).html"))

        self.assertIn('<a href="Страница 2 (1).html">', text)

    def testLinkToPageByProticolTitleNames_03(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (2).html"))

        self.assertIn('<a href="Страница 3.html">', text)

    def testLinkToAnchorByProticolTitleNames_01(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (2).html"))

        self.assertIn('<a href="Страница 7.html#anchor">', text)

    def testRelativeLinkTitleNames_01(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (2).html"))

        self.assertIn('<a href="Страница 2 (1).html">', text)

    def testRelativeLinkTitleNames_02(self):
        """
        Тест на проверку того, что заменяются ссылки вида page://...
        """
        from export2html.titlenamegenerator import TitleNameGenerator
        from export2html.branchexporter import BranchExporter

        Application.wikiroot = self.root
        namegenerator = TitleNameGenerator(self.outputdir)
        branchExporter = BranchExporter(self.root, namegenerator, Application)

        branchExporter.export(
            outdir=self.outputdir,
            imagesonly=False,
            alwaysOverwrite=False
        )

        text = readTextFile(
            os.path.join(
                self.outputdir,
                "Страница 2 (2).html"))

        self.assertIn('<a href="Страница 7.html">', text)
