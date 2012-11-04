#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.application import Application
from test.utils import removeWiki

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipanel import WikiPagePanel
from outwiker.pages.wiki.wikiconfig import WikiConfig


class WikiPagePanelTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory.create (self.wikiroot, u"Викистраница", [])
        WikiPageFactory.create (self.wikiroot, u"Викистраница 2", [])


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testType (self):
        Application.wikiroot = self.wikiroot
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (WikiPagePanel, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot[u"Викистраница 2"]
        self.assertEqual (WikiPagePanel, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)


    def testDefaultSelectedPage (self):
        """
        Тест на выбор вкладок по умолчанию
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.CODE_PAGE_INDEX)

        self.wikiroot[u"Викистраница 2"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Викистраница 2"]
        
        # Т.к. страница НЕ пустая, то по умолчанию выбирается вкладка с просмотром
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.RESULT_PAGE_INDEX)


    def testSelectedPage (self):
        """
        Тест на выбор вкладок
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.CODE_PAGE_INDEX)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPagePanel.RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.RESULT_PAGE_INDEX)

        
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPagePanel.CODE_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.CODE_PAGE_INDEX)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPagePanel.HTML_RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.HTML_RESULT_PAGE_INDEX)


    def testResultHtmlPage1 (self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = False

        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 2)

        Application.selectedPage = None
        config.showHtmlCodeOptions.value = True

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 3)


    def testResultHtmlPage2 (self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = False

        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 2)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPagePanel.HTML_RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.HTML_RESULT_PAGE_INDEX)
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 3)


    def testInvalidPageIndex (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.CODE_PAGE_INDEX)

    
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = 100

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = -1

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPagePanel.RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = 1000

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = -1

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                WikiPagePanel.RESULT_PAGE_INDEX)
