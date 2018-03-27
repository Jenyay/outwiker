# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.basetestcases import BaseOutWikerGUITest


class PageStatisticsTest (BaseOutWikerGUITest):
    """Тесты плагина Statistics применительно к статистике страницы"""

    def setUp(self):
        self.__pluginname = "Statistics"
        self.initApplication()
        self.wikiroot = self.createWiki()

        dirlist = ["../plugins/statistics"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png", "add.png", "anchor.png", "dir"]
        self.fullFilesPath = [os.path.join(filesPath, fname)
                              for fname in self.files]

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testSymbolsCountWiki(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = "Бла бла бла"
        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.symbols, 11)

    def testSymbolsCountHtml(self):
        from statistics.pagestat import PageStat

        HtmlPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = "Бла бла бла"
        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.symbols, 11)

    def testSymbolsCountText(self):
        from statistics.pagestat import PageStat

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = "Бла бла бла"
        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.symbols, 11)

    def testSymbolsCountSearch(self):
        def runTest():
            from statistics.pagestat import PageStat

            SearchPageFactory().create(self.wikiroot, "Страница 1", [])
            testPage = self.wikiroot["Страница 1"]

            pageStat = PageStat(testPage)
            pageStat.symbols

        self.assertRaises(TypeError, runTest)

    def testSymbolsNotWhiteSpacesWiki(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = "Бла бла бла\r\n\t\t\tАбырвалг  "
        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.symbolsNotWhiteSpaces, 17)

    def testSymbolsNotWhiteSpacesHtml(self):
        from statistics.pagestat import PageStat

        HtmlPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = "Бла бла бла\r\n\t\t\tАбырвалг  "
        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.symbolsNotWhiteSpaces, 17)

    def testSymbolsNotWhiteSpacesText(self):
        from statistics.pagestat import PageStat

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = "Бла бла бла\r\n\t\t\tАбырвалг  "
        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.symbolsNotWhiteSpaces, 17)

    def testSymbolsNotWhiteSpacesSearch(self):
        def runTest():
            from statistics.pagestat import PageStat

            SearchPageFactory().create(self.wikiroot, "Страница 1", [])
            testPage = self.wikiroot["Страница 1"]

            pageStat = PageStat(testPage)
            pageStat.symbolsNotWhiteSpaces

        self.assertRaises(TypeError, runTest)

    def testLinesWiki1(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка
И еще строка
Последняя строка"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.lines, 4)

    def testLinesWiki2(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.lines, 4)

    def testLinesHtml1(self):
        from statistics.pagestat import PageStat

        HtmlPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка
И еще строка
Последняя строка"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.lines, 4)

    def testLinesHtml2(self):
        from statistics.pagestat import PageStat

        HtmlPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.lines, 4)

    def testLinesText1(self):
        from statistics.pagestat import PageStat

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка
И еще строка
Последняя строка"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.lines, 4)

    def testLinesText2(self):
        from statistics.pagestat import PageStat

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.lines, 4)

    def testWordsWiki1(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.words, 11)

    def testWordsWiki2(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла.
Еще одна строка111 222 333

И еще строка ... ... ;;; @#$%#$

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.words, 13)

    def testWordsHtml1(self):
        from statistics.pagestat import PageStat

        HtmlPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.words, 11)

    def testWordsHtml2(self):
        from statistics.pagestat import PageStat

        HtmlPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла.
Еще одна строка111 222 333

И еще строка ... ... ;;; @#$%#$

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.words, 13)

    def testWordsText1(self):
        from statistics.pagestat import PageStat

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.words, 11)

    def testWordsText2(self):
        from statistics.pagestat import PageStat

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        testPage.content = """Бла бла бла.
Еще одна строка111 222 333

И еще строка ... ... ;;; @#$%#$

Последняя строка

"""

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.words, 13)

    def testWordsSearch(self):
        def runTest():
            from statistics.pagestat import PageStat

            SearchPageFactory().create(self.wikiroot, "Страница 1", [])
            testPage = self.wikiroot["Страница 1"]

            pageStat = PageStat(testPage)
            pageStat.words

        self.assertRaises(TypeError, runTest)

    def testAttachmentsCountWiki1(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsCount, 0)

    def testAttachmentsCountWiki2(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath[0:1])

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsCount, 1)

    def testAttachmentsCountWiki3(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath[0:3])

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsCount, 3)

    def testAttachmentsCountWiki4(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath)

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsCount, 6)

    def testAttachmentsCountSearch1(self):
        from statistics.pagestat import PageStat

        SearchPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath)

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsCount, 6)

    def testAttachmentsSizeWiki1(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsSize, 0)

    def testAttachmentsSizeWiki2(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath[0:1])

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsSize, 781)

    def testAttachmentsSizeWiki3(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath[0:3])

        pageStat = PageStat(testPage)

        self.assertEqual(pageStat.attachmentsSize, 2037)

    def testAttachmentsSizeWiki4(self):
        from statistics.pagestat import PageStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath)

        pageStat = PageStat(testPage)

        self.assertAlmostEqual(pageStat.attachmentsSize, 11771, delta=300)

    def testAttachmentsSizeSearch1(self):
        from statistics.pagestat import PageStat

        SearchPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]
        Attachment(testPage).attach(self.fullFilesPath)

        pageStat = PageStat(testPage)

        self.assertAlmostEqual(pageStat.attachmentsSize, 11771, delta=300)
