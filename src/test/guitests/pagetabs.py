# -*- coding: UTF-8 -*-

import wx

from basemainwnd import BaseMainWndTest
from outwiker.core.application import Application

from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.html.htmlpageview import HtmlPageView

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipageview import WikiPageView
from outwiker.pages.wiki.wikiconfig import WikiConfig


class PageTabsTest (BaseMainWndTest):
    """
    Tests for the view tabs (Wiki / Preview)
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        WikiConfig (Application.config).showHtmlCodeOptions.value = False

        self.wikipage = WikiPageFactory().create (self.wikiroot, u'Викистраница', [])
        self.htmlpage = HtmlPageFactory().create (self.wikiroot, u'HTML-страница', [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None


    def tearDown (self):
        BaseMainWndTest.tearDown (self)


    def testDefaultEmptyContent (self):
        # Page contents are empty. Code tab is selected.
        self.wikipage.content = u''
        self.htmlpage.content = u''

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual (self._getSelectedTabIndex(), WikiPageView.CODE_PAGE_INDEX)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual (self._getSelectedTabIndex(), HtmlPageView.CODE_PAGE_INDEX)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual (self._getSelectedTabIndex(), WikiPageView.CODE_PAGE_INDEX)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual (self._getSelectedTabIndex(), HtmlPageView.CODE_PAGE_INDEX)


    def testDefaultNotEmptyContent (self):
        # Page contents are not empty. Preview tab is selected.
        self.wikipage.content = u'Бла-бла-бла'
        self.htmlpage.content = u'Бла-бла-бла'

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual (self._getSelectedTabIndex(), WikiPageView.RESULT_PAGE_INDEX)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual (self._getSelectedTabIndex(), HtmlPageView.RESULT_PAGE_INDEX)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual (self._getSelectedTabIndex(), WikiPageView.RESULT_PAGE_INDEX)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual (self._getSelectedTabIndex(), HtmlPageView.RESULT_PAGE_INDEX)


    def testDefaultRecentUsedTab_wiki_01 (self):
        self.wikipage.content = u'Бла-бла-бла'

        Application.selectedPage = self.wikipage
        self._setSelectedTabIndex (WikiPageView.CODE_PAGE_INDEX)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual (self._getSelectedTabIndex(), WikiPageView.CODE_PAGE_INDEX)


    def testDefaultRecentUsedTab_html_01 (self):
        self.wikipage.content = u'Бла-бла-бла'

        Application.selectedPage = self.htmlpage
        self._setSelectedTabIndex (HtmlPageView.CODE_PAGE_INDEX)

        # Switch to wiki page and come back to HTML page
        Application.selectedPage = self.wikipage
        Application.selectedPage = self.htmlpage
        self.assertEqual (self._getSelectedTabIndex(), HtmlPageView.CODE_PAGE_INDEX)


    def testDefaultRecentUsedTab_wiki_02 (self):
        self.wikipage.content = u''

        Application.selectedPage = self.wikipage
        self._setSelectedTabIndex (WikiPageView.RESULT_PAGE_INDEX)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual (self._getSelectedTabIndex(), WikiPageView.RESULT_PAGE_INDEX)


    def testDefaultRecentUsedTab_html_02 (self):
        self.wikipage.content = u'Бла-бла-бла'

        Application.selectedPage = self.htmlpage
        self._setSelectedTabIndex (HtmlPageView.RESULT_PAGE_INDEX)

        # Switch to wiki page and come back to HTML page
        Application.selectedPage = self.wikipage
        Application.selectedPage = self.htmlpage
        self.assertEqual (self._getSelectedTabIndex(), HtmlPageView.RESULT_PAGE_INDEX)


    def _getSelectedTabIndex (self):
        return Application.mainWindow.pagePanel.pageView.selectedPageIndex


    def _setSelectedTabIndex (self, index):
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = index
        wx.GetApp().Yield()
