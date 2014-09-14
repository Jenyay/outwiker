# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.utils import removeWiki


class PageStatisticsTest (unittest.TestCase):
    """Тесты плагина Statistics применительно к статистике страницы"""
    def setUp (self):
        self.__pluginname = u"Statistics"

        self.__createWiki()

        dirlist = [u"../plugins/statistics"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        filesPath = u"../test/samplefiles/"
        self.files = [u"accept.png", u"add.png", u"anchor.png", u"dir"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]


    def tearDown (self):
        removeWiki (self.path)
        self.loader.clear()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testSymbolsCountWiki (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"Бла бла бла"
        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.symbols, 11)


    def testSymbolsCountHtml (self):
        HtmlPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"Бла бла бла"
        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.symbols, 11)


    def testSymbolsCountText (self):
        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"Бла бла бла"
        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.symbols, 11)


    def testSymbolsCountSearch (self):
        def runTest ():
            SearchPageFactory().create (self.wikiroot, u"Страница 1", [])
            testPage = self.wikiroot[u"Страница 1"]

            pageStat = self.loader[self.__pluginname].getPageStat (testPage)
            pageStat.symbols

        self.assertRaises (TypeError, runTest)


    def testSymbolsNotWhiteSpacesWiki (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"Бла бла бла\r\n\t\t\tАбырвалг  "
        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.symbolsNotWhiteSpaces, 17)


    def testSymbolsNotWhiteSpacesHtml (self):
        HtmlPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"Бла бла бла\r\n\t\t\tАбырвалг  "
        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.symbolsNotWhiteSpaces, 17)


    def testSymbolsNotWhiteSpacesText (self):
        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"Бла бла бла\r\n\t\t\tАбырвалг  "
        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.symbolsNotWhiteSpaces, 17)


    def testSymbolsNotWhiteSpacesSearch (self):
        def runTest ():
            SearchPageFactory().create (self.wikiroot, u"Страница 1", [])
            testPage = self.wikiroot[u"Страница 1"]

            pageStat = self.loader[self.__pluginname].getPageStat (testPage)
            pageStat.symbolsNotWhiteSpaces

        self.assertRaises (TypeError, runTest)


    def testLinesWiki1 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка
И еще строка
Последняя строка"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.lines, 4)


    def testLinesWiki2 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.lines, 4)


    def testLinesHtml1 (self):
        HtmlPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка
И еще строка
Последняя строка"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.lines, 4)


    def testLinesHtml2 (self):
        HtmlPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.lines, 4)


    def testLinesText1 (self):
        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка
И еще строка
Последняя строка"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.lines, 4)


    def testLinesText2 (self):
        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.lines, 4)


    def testWordsWiki1 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.words, 11)


    def testWordsWiki2 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла.
Еще одна строка111 222 333

И еще строка ... ... ;;; @#$%#$

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.words, 13)


    def testWordsHtml1 (self):
        HtmlPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.words, 11)


    def testWordsHtml2 (self):
        HtmlPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла.
Еще одна строка111 222 333

И еще строка ... ... ;;; @#$%#$

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.words, 13)


    def testWordsText1 (self):
        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла
Еще одна строка

И еще строка

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.words, 11)


    def testWordsText2 (self):
        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        testPage.content = u"""Бла бла бла.
Еще одна строка111 222 333

И еще строка ... ... ;;; @#$%#$

Последняя строка

"""

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.words, 13)


    def testWordsSearch (self):
        def runTest ():
            SearchPageFactory().create (self.wikiroot, u"Страница 1", [])
            testPage = self.wikiroot[u"Страница 1"]

            pageStat = self.loader[self.__pluginname].getPageStat (testPage)
            pageStat.words

        self.assertRaises (TypeError, runTest)


    def testAttachmentsCountWiki1 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsCount, 0)


    def testAttachmentsCountWiki2 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath[0:1])

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsCount, 1)


    def testAttachmentsCountWiki3 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath[0:3])

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsCount, 3)


    def testAttachmentsCountWiki4 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath)

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsCount, 6)


    def testAttachmentsCountSearch1 (self):
        SearchPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath)

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsCount, 6)


    def testAttachmentsSizeWiki1 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsSize, 0)


    def testAttachmentsSizeWiki2 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath[0:1])

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsSize, 781)


    def testAttachmentsSizeWiki3 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath[0:3])

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertEqual (pageStat.attachmentsSize, 2037)


    def testAttachmentsSizeWiki4 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath)

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertAlmostEqual (pageStat.attachmentsSize, 11771, delta=300)


    def testAttachmentsSizeSearch1 (self):
        SearchPageFactory().create (self.wikiroot, u"Страница 1", [])
        testPage = self.wikiroot[u"Страница 1"]
        Attachment (testPage).attach (self.fullFilesPath)

        pageStat = self.loader[self.__pluginname].getPageStat (testPage)

        self.assertAlmostEqual (pageStat.attachmentsSize, 11771, delta=300)
