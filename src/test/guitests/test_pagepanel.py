# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest
from outwiker.core.application import Application

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.text.textpanel import TextPanel

from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.html.htmlpageview import HtmlPageView

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipageview import WikiPageView

from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.search.searchpanel import SearchPanel


class PagePanelTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        TextPageFactory().create (self.wikiroot, "Текстовая страница", [])
        TextPageFactory().create (self.wikiroot, "Текстовая страница 2", [])

        HtmlPageFactory().create (self.wikiroot, "HTML-страница", [])
        HtmlPageFactory().create (self.wikiroot, "HTML-страница 2", [])

        WikiPageFactory().create (self.wikiroot, "Викистраница", [])
        WikiPageFactory().create (self.wikiroot, "Викистраница 2", [])

        SearchPageFactory().create (self.wikiroot, "Поисковая страница", [])
        SearchPageFactory().create (self.wikiroot, "Поисковая страница 2", [])


    def testEmpty (self):
        Application.wikiroot = self.wikiroot
        self.assertNotEqual (None, self.wnd.pagePanel.panel)
        self.assertEqual (None, self.wnd.pagePanel.pageView)


    def testSelect (self):
        Application.wikiroot = self.wikiroot
        self.wikiroot.selectedPage = self.wikiroot["Текстовая страница"]
        self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))

        self.wikiroot.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual (HtmlPageView, type (self.wnd.pagePanel.pageView))

        self.wikiroot.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual (WikiPageView, type (self.wnd.pagePanel.pageView))

        self.wikiroot.selectedPage = self.wikiroot["Поисковая страница"]
        self.assertEqual (SearchPanel, type (self.wnd.pagePanel.pageView))

        self.wikiroot.selectedPage = None
        self.assertEqual (None, self.wnd.pagePanel.pageView)


    def testSelectTextTypes (self):
        """
        Проверка на то, что при выборе страницы того же типа контрол не пересоздается, а данные загружаются в старый
        """
        Application.wikiroot = self.wikiroot

        self.wikiroot.selectedPage = self.wikiroot["Текстовая страница"]
        currentView = self.wnd.pagePanel.pageView

        self.assertNotEqual (None, currentView)
        self.assertEqual (TextPanel, type (currentView))

        self.wikiroot.selectedPage = self.wikiroot["Текстовая страница 2"]
        self.assertEqual (currentView, self.wnd.pagePanel.pageView)


    def testSelectHtmlTypes (self):
        """
        Проверка на то, что при выборе страницы того же типа контрол не пересоздается, а данные загружаются в старый
        """
        Application.wikiroot = self.wikiroot

        self.wikiroot.selectedPage = self.wikiroot["HTML-страница"]
        currentView = self.wnd.pagePanel.pageView

        self.assertNotEqual (None, currentView)
        self.assertEqual (HtmlPageView, type (currentView))

        self.wikiroot.selectedPage = self.wikiroot["HTML-страница 2"]
        self.assertEqual (currentView, self.wnd.pagePanel.pageView)


    def testSelectWikiTypes (self):
        """
        Проверка на то, что при выборе страницы того же типа контрол не пересоздается, а данные загружаются в старый
        """
        Application.wikiroot = self.wikiroot

        self.wikiroot.selectedPage = self.wikiroot["Викистраница"]
        currentView = self.wnd.pagePanel.pageView

        self.assertNotEqual (None, currentView)
        self.assertEqual (WikiPageView, type (currentView))

        self.wikiroot.selectedPage = self.wikiroot["Викистраница 2"]
        self.assertEqual (currentView, self.wnd.pagePanel.pageView)


    def testSelectSearchTypes (self):
        """
        Проверка на то, что при выборе страницы того же типа контрол не пересоздается, а данные загружаются в старый
        """
        Application.wikiroot = self.wikiroot

        self.wikiroot.selectedPage = self.wikiroot["Поисковая страница"]
        currentView = self.wnd.pagePanel.pageView

        self.assertNotEqual (None, currentView)
        self.assertEqual (SearchPanel, type (currentView))

        self.wikiroot.selectedPage = self.wikiroot["Поисковая страница 2"]
        self.assertEqual (currentView, self.wnd.pagePanel.pageView)


    def testLoadSelected (self):
        # Открытие вики с уже выбранной страницей
        self.wikiroot.selectedPage = self.wikiroot["Текстовая страница"]

        Application.wikiroot = self.wikiroot
        self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))


    def testReload (self):
        Application.wikiroot = self.wikiroot
        self.wikiroot.selectedPage = self.wikiroot["Текстовая страница"]
        self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))

        # "Закроем" вики
        Application.wikiroot = None
        self.assertEqual (None, self.wnd.pagePanel.pageView)

        # Откроем ее еще раз
        Application.wikiroot = self.wikiroot
        self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))
