# -*- coding: UTF-8 -*-

"""
Тесты для проверки фабрик страниц
"""

import unittest

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.text.textpanel import TextPanel
from outwiker.core.tree import WikiDocument, WikiPage
from outwiker.core.factory import PageFactory
from outwiker.core.factoryselector import FactorySelector


class FactorySelectorTest(unittest.TestCase):
    def setUp(self):
        self.path = u"../test/samplewiki"
        self.addEventsCount = 0
        self.removeEventCount = 0
        self.eventFactory = None


    def tearDown(self):
        FactorySelector.reset()


    def testSelection(self):
        wikiroot = WikiDocument.load(self.path)
        html_page = wikiroot[u"Типы страниц/HTML-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(html_page.getTypeString())),
            HtmlPageFactory)

        text_page = wikiroot[u"Типы страниц/Текстовая страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(text_page.getTypeString())),
            TextPageFactory)

        wiki_page = wikiroot[u"Типы страниц/wiki-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(wiki_page.getTypeString())),
            WikiPageFactory)

        search_page = wikiroot[u"Типы страниц/Страница поиска"]
        self.assertEqual(
            type(FactorySelector.getFactory(search_page.getTypeString())),
            SearchPageFactory)

        test_page = wikiroot[u"Типы страниц/TestPage"]
        self.assertEqual(
            type(FactorySelector.getFactory(test_page.getTypeString())),
            TextPageFactory)


    def testAddFactory(self):
        FactorySelector.addFactory(TestPageFactory())

        wikiroot = WikiDocument.load(self.path)

        test_page = wikiroot[u"Типы страниц/TestPage"]
        self.assertEqual(
            type(FactorySelector.getFactory(test_page.getTypeString())),
            TestPageFactory)


    def testRemoveFactory_01(self):
        FactorySelector.removeFactory(WikiPageFactory().getTypeString())

        wikiroot = WikiDocument.load(self.path)

        wiki_page = wikiroot[u"Типы страниц/wiki-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(wiki_page.getTypeString())),
            TextPageFactory)


    def testRemoveFactory_02(self):
        wikiroot = WikiDocument.load(self.path)

        FactorySelector.removeFactory(WikiPageFactory().getTypeString())

        wiki_page = wikiroot[u"Типы страниц/wiki-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(wiki_page.getTypeString())),
            TextPageFactory)



class TestPage(WikiPage):
    """
    Класс тестовых страниц
    """
    def __init__(self, path, title, parent, readonly=False):
        WikiPage.__init__(self, path, title, parent, readonly)


    @staticmethod
    def getTypeString():
        return u"testpage"


class TestPageFactory(PageFactory):
    """
    Класс фабрики для тестирования.
    Эта фабрика используется для создания типа страниц "testedPage",
    которая на самом деле является той же текстовой страницей,
    что и TextWikiPage.
    """
    def getPageType(self):
        return TestPage


    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return u"Test Page"


    def getPageView(self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return TextPanel(parent)


    def getPrefPanels(self, parent):
        return []
