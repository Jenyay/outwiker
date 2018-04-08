# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.search import (Searcher,
                                  AllTagsSearchStrategy,
                                  AnyTagSearchStrategy)
from outwiker.pages.search.searchpage import GlobalSearch
from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.attachment import Attachment


class SearcherTest(unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "page 1", ["метка 1", "Метка 2"])
        factory.create(self.wikiroot, "Страница 2", ["Метка 1", "Метка 3"])
        factory.create(self.wikiroot["Страница 2"],
                       "Страница 3",
                       ["Метка 2"])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       ["Метка 1"])
        factory.create(self.wikiroot["page 1"],
                       "page 5",
                       ["Метка 1", "метка 2"])

        self.wikiroot["page 1"].content = r"1  декабря.(Перечеркнуто, поправлено) 1 января 1925 г. Фотографирован \
            утром. Счастливо лает 'абыр', повторяя это слово громко и как бы радостно."

        self.wikiroot["page 1/page 5"].content = r"Сегодня после того, как у него отвалился хвост, он  произнес совершенно\
            отчетливо слово 'пивная'"

        self.wikiroot["Страница 2"].content = r"30  Декабря. Выпадение  шерсти  приняло  характер  общего  облысения.\
            Взвешивание  дало неожиданный  результат - 30 кг  за счет роста(удлинение)\
            костей. Пес по-прежнему лежит."

        self.wikiroot["Страница 2/Страница 3"].content = r"29 Декабря. Внезапно обнаружено выпадение  шерсти на лбу  \
            и на боках туловища."

        self.wikiroot["Страница 2/Страница 3/Страница 4"].content = r"2 Января. Фотографирован во время  улыбки при магнии. \
            Встал с постели и уверенно держался полчаса на задних лапах. Моего почти роста."

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png",
                      "add.png",
                      "anchor.png",
                      "файл с пробелами.tmp",
                      "dir"]
        self.fullFilesPath = [os.path.join(filesPath, fname)
                              for fname in self.files]

        Attachment(self.wikiroot["page 1"]).attach(self.fullFilesPath)
        Attachment(self.wikiroot["Страница 2/Страница 3"]).attach(self.fullFilesPath[0:3])
        Attachment(self.wikiroot["Страница 2"]).attach([self.fullFilesPath[0]])

    def testSearchContentAll(self):
        phrase = "Декабря"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 3)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3"] in pages)

    def testSearchAttach1(self):
        phrase = "accept"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 3)

        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)

    def testSearchAttach2(self):
        phrase = "anchor"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 2)

        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3"] in pages)

    def tearDown(self):
        removeDir(self.path)

    def testSearchAttach3(self):
        phrase = "файл с пробелами"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 1)

        self.assertTrue(self.wikiroot["page 1"] in pages)

    def testSearchAttach4(self):
        phrase = "dir.xxx"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 1)

        self.assertTrue(self.wikiroot["page 1"] in pages)

    def testSearchAttach5(self):
        phrase = "SubdIr2"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 1)

        self.assertTrue(self.wikiroot["page 1"] in pages)

    def testSearchAttach6(self):
        phrase = "ApplicAtiOn.pY"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 1)

        self.assertTrue(self.wikiroot["page 1"] in pages)

    def testSearchTagsContent1(self):
        phrase = "метка"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 5)

    def testSearchTagsContent2(self):
        phrase = "МеТкА 1"
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 4)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue(self.wikiroot["page 1/page 5"] in pages)

    def testSearchContentAny(self):
        phrase = "Декабря"
        tags = []

        searcher = Searcher(phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 3)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3"] in pages)

    def testSearchAllAll(self):
        phrase = ""
        tags = []

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 5)

    def testSearchAllAny(self):
        phrase = ""
        tags = []

        searcher = Searcher(phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 5)

    def testSearchSingleTagAll(self):
        phrase = ""
        tags = ["Метка 1"]

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 4)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue(self.wikiroot["page 1/page 5"] in pages)

    def testSearchSingleTagAny(self):
        phrase = ""
        tags = ["Метка 1"]

        searcher = Searcher(phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 4)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue(self.wikiroot["page 1/page 5"] in pages)

    def testSearchTag2All(self):
        phrase = ""
        tags = ["МеткА 1", "МетКа 2"]

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 2)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["page 1/page 5"] in pages)

    def testSearchTag2Any(self):
        phrase = ""
        tags = ["МеткА 1", "МетКа 3"]

        searcher = Searcher(phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 4)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue(self.wikiroot["page 1/page 5"] in pages)

    def testSearchFullAll(self):
        phrase = "Декабря"
        tags = ["Метка 2"]

        searcher = Searcher(phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 2)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3"] in pages)

    def testSearchFullAny(self):
        phrase = "Декабря"
        tags = ["Метка 2"]

        searcher = Searcher(phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find(self.wikiroot)

        self.assertEqual(len(pages), 2)
        self.assertTrue(self.wikiroot["page 1"] in pages)
        self.assertTrue(self.wikiroot["Страница 2/Страница 3"] in pages)


class SearchPageTest(unittest.TestCase):
    """
    Тест на создание страниц с поиском
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "page 1", ["Метка 1", "Метка 2"])
        factory.create(self.wikiroot, "Страница 2", ["Метка 1", "Метка 3"])
        factory.create(self.wikiroot["Страница 2"],
                       "Страница 3",
                       ["Метка 2"])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       ["Метка 1"])
        factory.create(self.wikiroot["page 1"], "page 5", ["Метка 4"])

        self.wikiroot["page 1"].content = r"1  декабря.(Перечеркнуто, поправлено) 1 января 1925 г. Фотографирован \
            утром. Счастливо лает 'абыр', повторяя это слово громко и как бы радостно."

        self.wikiroot["page 1/page 5"].content = r"Сегодня после того, как у него отвалился хвост, он  произнес совершенно\
            отчетливо слово 'пивная'"

        self.wikiroot["Страница 2"].content = r"30  Декабря. Выпадение  шерсти  приняло  характер  общего  облысения.\
            Взвешивание  дало неожиданный  результат - 30 кг  за счет роста(удлинение)\
            костей. Пес по-прежнему лежит."

        self.wikiroot["Страница 2/Страница 3"].content = r"29 Декабря. Внезапно обнаружено выпадение  шерсти на лбу  \
            и на боках туловища."

        self.wikiroot["Страница 2/Страница 3/Страница 4"].content = r"2 Января. Фотографирован во время  улыбки при магнии. \
            Встал с постели и уверенно держался полчаса на задних лапах. Моего почти роста."

    def tearDown(self):
        removeDir(self.path)

    def testCreateDefaultPage(self):
        GlobalSearch.create(self.wikiroot)
        page = self.wikiroot[GlobalSearch.pageTitle]

        self.assertNotEqual(page, None)
        self.assertEqual(self.wikiroot.selectedPage, page)
        self.assertEqual(page.phrase, "")
        self.assertEqual(len(page.searchTags), 0)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testCreateSearchTagsPage(self):
        GlobalSearch.create(self.wikiroot, tags=["Метка 1", "Метка 2"])
        page = self.wikiroot[GlobalSearch.pageTitle]

        self.assertNotEqual(page, None)
        self.assertEqual(self.wikiroot.selectedPage, page)
        self.assertEqual(page.phrase, "")
        self.assertEqual(len(page.searchTags), 2)
        self.assertTrue("Метка 1" in page.searchTags)
        self.assertTrue("Метка 2" in page.searchTags)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testCreateSearchPhrasePage(self):
        GlobalSearch.create(self.wikiroot, phrase="декабрь")
        page = self.wikiroot[GlobalSearch.pageTitle]

        self.assertNotEqual(page, None)
        self.assertEqual(self.wikiroot.selectedPage, page)
        self.assertEqual(page.phrase, "декабрь")
        self.assertEqual(len(page.searchTags), 0)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testCreateSearchAllPage(self):
        GlobalSearch.create(self.wikiroot,
                            phrase="декабрь",
                            tags=["Метка 1", "Метка 2"],
                            strategy=AllTagsSearchStrategy)

        page = self.wikiroot[GlobalSearch.pageTitle]

        self.assertNotEqual(page, None)
        self.assertEqual(self.wikiroot.selectedPage, page)
        self.assertEqual(page.phrase, "декабрь")
        self.assertEqual(len(page.searchTags), 2)
        self.assertTrue("Метка 1" in page.searchTags)
        self.assertTrue("Метка 2" in page.searchTags)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testLoadSearchPage(self):
        GlobalSearch.create(self.wikiroot,
                            phrase="декабрь",
                            tags=["Метка 1", "Метка 2"],
                            strategy=AllTagsSearchStrategy)

        wiki = WikiDocument.load(self.path)
        page = wiki[GlobalSearch.pageTitle]

        self.assertNotEqual(page, None)
        self.assertEqual(page.phrase, "декабрь")
        self.assertEqual(len(page.searchTags), 2)
        self.assertTrue("Метка 1" in page.searchTags)
        self.assertTrue("Метка 2" in page.searchTags)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testManySearchPages1(self):
        GlobalSearch.create(self.wikiroot)

        GlobalSearch.create(self.wikiroot,
                            phrase="декабрь",
                            tags=["Метка 1", "Метка 2"],
                            strategy=AllTagsSearchStrategy)

        wiki = WikiDocument.load(self.path)
        page = wiki[GlobalSearch.pageTitle]

        self.assertEqual(wiki[GlobalSearch.pageTitle + " 2"], None)
        self.assertNotEqual(page, None)
        self.assertEqual(page.phrase, "декабрь")
        self.assertEqual(len(page.searchTags), 2)
        self.assertTrue("Метка 1" in page.searchTags)
        self.assertTrue("Метка 2" in page.searchTags)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testManySearchPages2(self):
        TextPageFactory().create(self.wikiroot, GlobalSearch.pageTitle, [])

        GlobalSearch.create(self.wikiroot,
                            phrase="декабрь",
                            tags=["Метка 1", "Метка 2"],
                            strategy=AllTagsSearchStrategy)

        wiki = WikiDocument.load(self.path)
        page = wiki[GlobalSearch.pageTitle + " 2"]

        self.assertNotEqual(page, None)
        self.assertEqual(page.phrase, "декабрь")
        self.assertEqual(len(page.searchTags), 2)
        self.assertTrue("Метка 1" in page.searchTags)
        self.assertTrue("Метка 2" in page.searchTags)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testManySearchPages3(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, GlobalSearch.pageTitle, [])
        factory.create(self.wikiroot, GlobalSearch.pageTitle + " 2", [])
        factory.create(self.wikiroot, GlobalSearch.pageTitle + " 3", [])
        factory.create(self.wikiroot, GlobalSearch.pageTitle + " 4", [])

        GlobalSearch.create(self.wikiroot,
                            phrase="декабрь",
                            tags=["Метка 1", "Метка 2"],
                            strategy=AllTagsSearchStrategy)

        wiki = WikiDocument.load(self.path)
        page = wiki[GlobalSearch.pageTitle + " 5"]

        self.assertNotEqual(page, None)
        self.assertEqual(page.phrase, "декабрь")
        self.assertEqual(len(page.searchTags), 2)
        self.assertTrue("Метка 1" in page.searchTags)
        self.assertTrue("Метка 2" in page.searchTags)
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

    def testSetPhrase(self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create(self.wikiroot)

        self.assertEqual(page.phrase, "")
        self.assertEqual(page.searchTags, [])

        # Поменяем параметры через свойства
        page.phrase = "Абырвалг"
        self.assertEqual(page.phrase, "Абырвалг")

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load(self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertNotEqual(searchPage, None)
        self.assertEqual(searchPage.phrase, "Абырвалг")

    def testSetTags(self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create(self.wikiroot)

        self.assertEqual(page.phrase, "")
        self.assertEqual(page.searchTags, [])

        # Поменяем параметры через свойства
        page.searchTags = ["тег1", "тег2"]
        self.assertEqual(page.searchTags, ["тег1", "тег2"])

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load(self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertNotEqual(searchPage, None)
        self.assertEqual(searchPage.searchTags, ["тег1", "тег2"])

    def testSetStrategy1(self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create(self.wikiroot)

        self.assertEqual(page.phrase, "")
        self.assertEqual(page.searchTags, [])

        # Поменяем параметры через свойства
        page.strategy = AllTagsSearchStrategy
        self.assertEqual(page.strategy, AllTagsSearchStrategy)

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load(self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertNotEqual(searchPage, None)
        self.assertEqual(searchPage.strategy, AllTagsSearchStrategy)

    def testSetStrategy2(self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create(self.wikiroot)

        self.assertEqual(page.phrase, "")
        self.assertEqual(page.searchTags, [])

        # Поменяем параметры через свойства
        page.strategy = AnyTagSearchStrategy
        self.assertEqual(page.strategy, AnyTagSearchStrategy)

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load(self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertNotEqual(searchPage, None)
        self.assertEqual(searchPage.strategy, AnyTagSearchStrategy)
