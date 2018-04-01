# -*- coding: utf-8 -*-

import datetime
import os.path
import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class TreeStatisticsTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """Тесты для плагина Statistics, относящиеся к статистике дерева"""

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.__pluginname = "Statistics"

        dirlist = ["../plugins/statistics"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png", "add.png", "anchor.png", "dir"]
        self.fullFilesPath = [
            os.path.join(
                filesPath,
                fname) for fname in self.files]

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPageCount1(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.pageCount, 1)

    def testPageCount2(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        testPage = self.wikiroot["Страница 1"]

        treeStat = TreeStat(testPage)

        self.assertEqual(treeStat.pageCount, 1)

    def testPageCount3(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        WikiPageFactory().create(self.wikiroot, "Страница 3", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.pageCount, 3)

    def testPageCount4(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.pageCount, 3)

    def testPageCount5(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 5", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.pageCount, 5)

    def testMaxDepth1(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.maxDepth), 1)

        self.assertEqual(treeStat.maxDepth[0][0], 1)
        self.assertEqual(treeStat.maxDepth[0][1], self.wikiroot["Страница 1"])

    def testMaxDepth2(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.maxDepth), 1)
        self.assertEqual(treeStat.maxDepth[0][0], 2)
        self.assertEqual(
            treeStat.maxDepth[0][1],
            self.wikiroot["Страница 1/Страница 2"])

    def testMaxDepth3(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.maxDepth), 2)
        self.assertEqual(treeStat.maxDepth[0][0], 1)

    def testMaxDepth4(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 5", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.maxDepth), 1)
        self.assertEqual(treeStat.maxDepth[0][0], 3)
        self.assertEqual(
            treeStat.maxDepth[0][1],
            self.wikiroot["Страница 1/Страница 2/Страница 3"])

    def testMaxDepth5(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.maxDepth), 0)

    def testTagsCount1(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.tagsCount, 0)

    def testTagsCount2(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", ["Тег 1"])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.tagsCount, 1)

    def testTagsCount3(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(
            self.wikiroot, "Страница 1", [
                "Тег 1", "Тег 2", "Тег 3"])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.tagsCount, 3)

    def testTagsCount4(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(
            self.wikiroot, "Страница 1", [
                "Тег 1", "Тег 2", "Тег 3"])
        WikiPageFactory().create(
            self.wikiroot["Страница 1"],
            "Страница 2",
            ["Тег 4"])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"],
            "Страница 3",
            ["Тег 1", "Тег 2"])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 5", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(treeStat.tagsCount, 4)

    def testFrequentTags1(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.frequentTags), 0)

    def testFrequentTags2(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", ["тег 1"])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.frequentTags), 1)
        self.assertEqual(treeStat.frequentTags[0][0], "тег 1")
        self.assertEqual(treeStat.frequentTags[0][1], 1)

    def testFrequentTags3(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(
            self.wikiroot, "Страница 1", [
                "тег 1", "тег2"])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.frequentTags), 2)

    def testFrequentTags4(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(
            self.wikiroot, "Страница 1", [
                "тег 1", "тег 2", "тег 3"])
        WikiPageFactory().create(
            self.wikiroot["Страница 1"], "Страница 2", [
                "тег 1", "тег 3"])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"],
            "Страница 3",
            ["тег 3"])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 5", [])

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.frequentTags), 3)
        self.assertEqual(treeStat.frequentTags[0][0], "тег 3")
        self.assertEqual(treeStat.frequentTags[0][1], 3)

        self.assertEqual(treeStat.frequentTags[1][0], "тег 1")
        self.assertEqual(treeStat.frequentTags[1][1], 2)

        self.assertEqual(treeStat.frequentTags[2][0], "тег 2")
        self.assertEqual(treeStat.frequentTags[2][1], 1)

    def testPageDate1(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)

        self.assertEqual(len(treeStat.pageDate), 0)

    def testPageDate2(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        self.assertEqual(len(treeStat.pageDate), 1)
        self.assertEqual(treeStat.pageDate[0], self.wikiroot["Страница 1"])

    def testPageDate3(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])

        self.wikiroot["Страница 1"].datetime = datetime.datetime(2013, 4, 23)
        self.wikiroot["Страница 1/Страница 2"].datetime = datetime.datetime(
            2013, 4, 20)
        self.wikiroot["Страница 1/Страница 2/Страница 3"].datetime = datetime.datetime(
            2013, 4, 30)

        self.assertEqual(len(treeStat.pageDate), 3)
        self.assertEqual(
            treeStat.pageDate[0],
            self.wikiroot["Страница 1/Страница 2/Страница 3"])
        self.assertEqual(treeStat.pageDate[1], self.wikiroot["Страница 1"])
        self.assertEqual(
            treeStat.pageDate[2],
            self.wikiroot["Страница 1/Страница 2"])

    def testPageDate4(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        WikiPageFactory().create(self.wikiroot["Страница 4"], "Страница 5", [])

        self.wikiroot["Страница 1"].datetime = datetime.datetime(2013, 4, 23)
        self.wikiroot["Страница 1/Страница 2"].datetime = datetime.datetime(
            2013, 4, 20)
        self.wikiroot["Страница 1/Страница 2/Страница 3"].datetime = datetime.datetime(2013, 4, 30)
        self.wikiroot["Страница 4"].datetime = datetime.datetime(2010, 1, 1)
        self.wikiroot["Страница 4/Страница 5"].datetime = datetime.datetime(
            2009, 1, 1)

        self.assertEqual(len(treeStat.pageDate), 5)
        self.assertEqual(
            treeStat.pageDate[0],
            self.wikiroot["Страница 1/Страница 2/Страница 3"])
        self.assertEqual(treeStat.pageDate[1], self.wikiroot["Страница 1"])
        self.assertEqual(
            treeStat.pageDate[2],
            self.wikiroot["Страница 1/Страница 2"])
        self.assertEqual(treeStat.pageDate[3], self.wikiroot["Страница 4"])
        self.assertEqual(
            treeStat.pageDate[4],
            self.wikiroot["Страница 4/Страница 5"])

    def testPageContentLength1(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)

        pagesList = treeStat.pageContentLength
        self.assertEqual(len(pagesList), 0)

    def testPageContentLength2(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.wikiroot["Страница 1"].content = "Бла"

        treeStat = TreeStat(self.wikiroot)

        pagesList = treeStat.pageContentLength

        self.assertEqual(len(pagesList), 1)
        self.assertEqual(pagesList[0][0], self.wikiroot["Страница 1"])
        self.assertEqual(pagesList[0][1], 3)

    def testPageContentLength3(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 1"].content = "Бла"
        self.wikiroot["Страница 1/Страница 2"].content = "   Бла-бла-бла   "
        self.wikiroot["Страница 1/Страница 2/Страница 3"].content = "Бла-"
        self.wikiroot["Страница 4"].content = " Бла-бла                                  "

        treeStat = TreeStat(self.wikiroot)

        pagesList = treeStat.pageContentLength

        self.assertEqual(len(pagesList), 4)

        self.assertEqual(
            pagesList[0][0],
            self.wikiroot["Страница 1/Страница 2"])
        self.assertEqual(pagesList[0][1], 11)

        self.assertEqual(pagesList[1][0], self.wikiroot["Страница 4"])
        self.assertEqual(pagesList[1][1], 7)

        self.assertEqual(
            pagesList[2][0],
            self.wikiroot["Страница 1/Страница 2/Страница 3"])
        self.assertEqual(pagesList[2][1], 4)

        self.assertEqual(pagesList[3][0], self.wikiroot["Страница 1"])
        self.assertEqual(pagesList[3][1], 3)

    def testPageContentLength4(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        SearchPageFactory().create(self.wikiroot, "Страница 5", [])

        self.wikiroot["Страница 1"].content = "Бла"
        self.wikiroot["Страница 1/Страница 2"].content = "   Бла-бла-бла   "
        self.wikiroot["Страница 1/Страница 2/Страница 3"].content = "Бла-"
        self.wikiroot["Страница 4"].content = " Бла-бла                                  "

        treeStat = TreeStat(self.wikiroot)

        pagesList = treeStat.pageContentLength

        self.assertEqual(len(pagesList), 5)

        self.assertEqual(pagesList[4][0], self.wikiroot["Страница 5"])
        self.assertEqual(pagesList[4][1], 0)

    def testAttachmentSize1(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)

        pagesList = treeStat.pageAttachmentsSize
        self.assertEqual(len(pagesList), 0)

    def testAttachmentSize2(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        pagesList = treeStat.pageAttachmentsSize

        self.assertEqual(len(pagesList), 1)
        self.assertEqual(pagesList[0][0], self.wikiroot["Страница 1"])
        self.assertEqual(pagesList[0][1], 0)

    def testAttachmentSize3(self):
        from statistics.treestat import TreeStat

        treeStat = TreeStat(self.wikiroot)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        Attachment(self.wikiroot["Страница 1"]).attach(self.fullFilesPath[0:1])

        pagesList = treeStat.pageAttachmentsSize

        self.assertEqual(len(pagesList), 1)
        self.assertEqual(pagesList[0][0], self.wikiroot["Страница 1"])
        self.assertEqual(pagesList[0][1], 781)

    def testAttachmentSize4(self):
        from statistics.treestat import TreeStat

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot["Страница 1"], "Страница 2", [])
        WikiPageFactory().create(
            self.wikiroot["Страница 1/Страница 2"], "Страница 3", [])
        WikiPageFactory().create(self.wikiroot, "Страница 4", [])
        SearchPageFactory().create(self.wikiroot, "Страница 5", [])

        Attachment(self.wikiroot["Страница 1"]).attach([])
        Attachment(self.wikiroot["Страница 1/Страница 2"]
                   ).attach(self.fullFilesPath[0:1])
        Attachment(
            self.wikiroot["Страница 1/Страница 2/Страница 3"]).attach(self.fullFilesPath[0:2])
        Attachment(self.wikiroot["Страница 4"]).attach(self.fullFilesPath[0:3])
        Attachment(self.wikiroot["Страница 5"]).attach(self.fullFilesPath)

        treeStat = TreeStat(self.wikiroot)

        pagesList = treeStat.pageAttachmentsSize

        self.assertEqual(len(pagesList), 5)

        self.assertEqual(pagesList[4][0], self.wikiroot["Страница 1"])
        self.assertEqual(pagesList[4][1], 0)

        self.assertEqual(pagesList[0][0], self.wikiroot["Страница 5"])
        self.assertAlmostEqual(pagesList[0][1], 11771, delta=300)

        self.assertEqual(pagesList[1][0], self.wikiroot["Страница 4"])
        self.assertEqual(pagesList[1][1], 2037)
