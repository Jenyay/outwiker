# -*- coding: utf-8 -*-

"""
Тесты для проверки фабрик страниц
"""

import unittest

from outwiker.api.core.tree import loadNotesTree
from outwiker.core.init import init_page_factories
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.text.textpanel import TextPanel
from outwiker.core.tree import PageAdapter
from outwiker.core.factory import PageFactory
from outwiker.core.factoryselector import FactorySelector
from outwiker.gui.unknownpagetype import UnknownPageTypeFactory


TEST_PAGE_TYPE_STRING = "testpage"


class FactorySelectorTest(unittest.TestCase):
    def setUp(self):
        self.path = "testdata/samplewiki"
        self.addEventsCount = 0
        self.removeEventCount = 0
        self.eventFactory = None
        init_page_factories()

    def tearDown(self):
        FactorySelector.reset()

    def testSelection(self):
        wikiroot = loadNotesTree(self.path)
        html_page = wikiroot["Типы страниц/HTML-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(html_page.getTypeString())),
            HtmlPageFactory)

        text_page = wikiroot["Типы страниц/Текстовая страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(text_page.getTypeString())),
            TextPageFactory)

        wiki_page = wikiroot["Типы страниц/wiki-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(wiki_page.getTypeString())),
            WikiPageFactory)

        search_page = wikiroot["Типы страниц/Страница поиска"]
        self.assertEqual(
            type(FactorySelector.getFactory(search_page.getTypeString())),
            SearchPageFactory)

        test_page = wikiroot["Типы страниц/TestPage"]
        self.assertEqual(
            type(FactorySelector.getFactory(test_page.getTypeString())),
            UnknownPageTypeFactory)

    def testAddFactory(self):
        FactorySelector.addFactory(ExamplePageFactory())

        wikiroot = loadNotesTree(self.path)

        test_page = wikiroot["Типы страниц/TestPage"]
        self.assertEqual(
            type(FactorySelector.getFactory(test_page.getTypeString())),
            ExamplePageFactory)

    def testRemoveFactory_01(self):
        FactorySelector.removeFactory(WikiPageFactory().getPageTypeString())

        wikiroot = loadNotesTree(self.path)

        wiki_page = wikiroot["Типы страниц/wiki-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(wiki_page.getTypeString())),
            UnknownPageTypeFactory)

    def testRemoveFactory_02(self):
        wikiroot = loadNotesTree(self.path)

        FactorySelector.removeFactory(WikiPageFactory().getPageTypeString())

        wiki_page = wikiroot["Типы страниц/wiki-страница"]
        self.assertEqual(
            type(FactorySelector.getFactory(wiki_page.getTypeString())),
            UnknownPageTypeFactory)


class ExamplePageAdapter(PageAdapter):
    """
    Класс тестовых страниц
    """
    def getTypeString(self):
        return TEST_PAGE_TYPE_STRING


class ExamplePageFactory(PageFactory):
    """
    Класс фабрики для тестирования.
    Эта фабрика используется для создания типа страниц "testedPage",
    которая на самом деле является той же текстовой страницей,
    что и TextWikiPage.
    """
    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return "Test Page"

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return TextPanel(parent, application)

    def getPrefPanels(self, parent):
        return []

    def getPageTypeString(self):
        return TEST_PAGE_TYPE_STRING

    def createPageAdapter(self, page):
        return ExamplePageAdapter(page)
