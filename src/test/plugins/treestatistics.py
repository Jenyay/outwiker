#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.utils import removeWiki


class TreeStatisticsTest (unittest.TestCase):
    """Тесты для плагина Statistics, относящиеся к статистике дерева"""
    def setUp (self):
        self.__pluginname = u"Statistics"

        self.__createWiki()

        dirlist = [u"../plugins/statistics"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        removeWiki (self.path)
        self.loader.clear()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)


    def testPageCount1 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.pageCount, 1)


    def testPageCount2 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        testPage = self.rootwiki[u"Страница 1"]

        treeStat = self.loader[self.__pluginname].getTreeStat (testPage)

        self.assertEqual (treeStat.pageCount, 1)


    def testPageCount3 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        WikiPageFactory.create (self.rootwiki, u"Страница 3", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.pageCount, 3)


    def testPageCount4 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1/Страница 2"], u"Страница 3", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.pageCount, 3)


    def testPageCount5 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1/Страница 2"], u"Страница 3", [])
        WikiPageFactory.create (self.rootwiki, u"Страница 4", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.pageCount, 5)


    def testMaxDepth1 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.maxDepth), 1)

        self.assertEqual (treeStat.maxDepth[0][0], 1)
        self.assertEqual (treeStat.maxDepth[0][1], self.rootwiki[u"Страница 1"])


    def testMaxDepth2 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.maxDepth), 1)
        self.assertEqual (treeStat.maxDepth[0][0], 2)
        self.assertEqual (treeStat.maxDepth[0][1], self.rootwiki[u"Страница 1/Страница 2"])


    def testMaxDepth3 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.maxDepth), 2)
        self.assertEqual (treeStat.maxDepth[0][0], 1)


    def testMaxDepth4 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1/Страница 2"], u"Страница 3", [])
        WikiPageFactory.create (self.rootwiki, u"Страница 4", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.maxDepth), 1)
        self.assertEqual (treeStat.maxDepth[0][0], 3)
        self.assertEqual (treeStat.maxDepth[0][1], self.rootwiki[u"Страница 1/Страница 2/Страница 3"])


    def testMaxDepth5 (self):
        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.maxDepth), 0)


    def testTagsCount1 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.tagsCount, 0)


    def testTagsCount2 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [u"Тег 1"])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.tagsCount, 1)


    def testTagsCount3 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [u"Тег 1", u"Тег 2", u"Тег 3"])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.tagsCount, 3)


    def testTagsCount4 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [u"Тег 1", u"Тег 2", u"Тег 3"])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [u"Тег 4"])
        WikiPageFactory.create (self.rootwiki[u"Страница 1/Страница 2"], u"Страница 3", [u"Тег 1", u"Тег 2"])
        WikiPageFactory.create (self.rootwiki, u"Страница 4", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (treeStat.tagsCount, 4)


    def testFrequentTags1 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.frequentTags), 0)


    def testFrequentTags2 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [u"тег 1"])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.frequentTags), 1)
        self.assertEqual (treeStat.frequentTags[0][0], u"тег 1")
        self.assertEqual (treeStat.frequentTags[0][1], 1)


    def testFrequentTags3 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [u"тег 1", u"тег2"])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.frequentTags), 2)


    def testFrequentTags4 (self):
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [u"тег 1", u"тег 2", u"тег 3"])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [u"тег 1", u"тег 3"])
        WikiPageFactory.create (self.rootwiki[u"Страница 1/Страница 2"], u"Страница 3", [u"тег 3"])
        WikiPageFactory.create (self.rootwiki, u"Страница 4", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

        treeStat = self.loader[self.__pluginname].getTreeStat (self.rootwiki)

        self.assertEqual (len (treeStat.frequentTags), 3)
        self.assertEqual (treeStat.frequentTags[0][0], u"тег 3")
        self.assertEqual (treeStat.frequentTags[0][1], 3)

        self.assertEqual (treeStat.frequentTags[1][0], u"тег 1")
        self.assertEqual (treeStat.frequentTags[1][1], 2)

        self.assertEqual (treeStat.frequentTags[2][0], u"тег 2")
        self.assertEqual (treeStat.frequentTags[2][1], 1)
