#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.application import Application
from test.utils import removeWiki

from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.html.htmlpageview import HtmlPageView


class HtmlPageViewTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        HtmlPageFactory.create (self.wikiroot, u"HTML-страница", [])
        HtmlPageFactory.create (self.wikiroot, u"HTML-страница 2", [])


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testType (self):
        Application.wikiroot = self.wikiroot
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot[u"HTML-страница"]
        self.assertEqual (HtmlPageView, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot[u"HTML-страница 2"]
        self.assertEqual (HtmlPageView, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)


    def testDefaultSelectedPage (self):
        """
        Тест на выбор вкладок по умолчанию
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)

        self.wikiroot[u"HTML-страница 2"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"HTML-страница 2"]
        
        # Т.к. страница НЕ пустая, то по умолчанию выбирается вкладка с просмотром
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)


    def testSelectedPage (self):
        """
        Тест на выбор вкладок
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)

        
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)


    def testInvalidPageIndex (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)

    
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = 100

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = -1

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = 1000

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = -1

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)


    def testSavePageIndex (self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        self.wikiroot[u"HTML-страница"].content = u"Бла-бла-бла"
        self.wikiroot[u"HTML-страница 2"].content = u"Бла-бла-бла 2"
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"HTML-страница"]

        # В начале по умолчанию выбирается вкладка с просмотром
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)

        # Переключимся на вкладку с кодом
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        Application.selectedPage = self.wikiroot[u"HTML-страница 2"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)

        # А при возврате на предыдущую страницу, должна быть выбана страница с кодом
        Application.selectedPage = self.wikiroot[u"HTML-страница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.CODE_PAGE_INDEX)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        Application.selectedPage = self.wikiroot[u"HTML-страница 2"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                HtmlPageView.RESULT_PAGE_INDEX)
