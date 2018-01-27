# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory

from .basemainwnd import BaseMainWndTest


class PageTabsTest(BaseMainWndTest):
    """
    Tests for the view tabs (Wiki / Preview)
    """
    def setUp(self):
        BaseMainWndTest.setUp(self)
        self.config = GeneralGuiConfig(Application.config)
        self.config.pageTab.remove_option()

        self.wikipage = WikiPageFactory().create(self.wikiroot,
                                                 'Викистраница',
                                                 [])
        self.htmlpage = HtmlPageFactory().create(self.wikiroot,
                                                 'HTML-страница',
                                                 [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

    def tearDown(self):
        BaseMainWndTest.tearDown(self)
        self.config.pageTab.remove_option()

    def testDefaultEmptyContent(self):
        # Page contents are empty. Code tab is selected.
        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentEmptyContent(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        # Page contents are empty. Code tab is selected.
        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testDefaultNotEmptyContent(self):
        # Page contents are not empty. Preview tab is selected.
        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentNotEmptyContent(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        # Page contents are not empty. Preview tab is selected.
        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testDefaultRecentUsedTab_wiki_01(self):
        self.wikipage.content = 'Бла-бла-бла'

        Application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentRecentUsedTab_wiki_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.wikipage.content = 'Бла-бла-бла'

        Application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testDefaultRecentUsedTab_html_01(self):
        self.htmlpage.content = 'Бла-бла-бла'

        Application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to wiki page and come back to HTML page
        Application.selectedPage = self.wikipage
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentRecentUsedTab_html_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.htmlpage.content = 'Бла-бла-бла'

        Application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to wiki page and come back to HTML page
        Application.selectedPage = self.wikipage
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testDefaultRecentUsedTab_wiki_02(self):
        self.wikipage.content = ''

        Application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentRecentUsedTab_wiki_02(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.wikipage.content = ''

        Application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testDefaultRecentUsedTab_html_02(self):
        self.htmlpage.content = 'Бла-бла-бла'

        Application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to wiki page and come back to HTML page
        Application.selectedPage = self.wikipage
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentRecentUsedTab_html_02(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.htmlpage.content = 'Бла-бла-бла'

        Application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to wiki page and come back to HTML page
        Application.selectedPage = self.wikipage
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testTabEditorAlways_code_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_CODE

        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testTabEditorAlways_code_not_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_CODE

        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testTabEditorAlways_preview_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RESULT

        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testTabEditorAlways_preview_not_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RESULT

        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        Application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentUsedTab_code_wiki(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_CODE
        self.wikipage.content = 'Бла-бла-бла'
        Application.selectedPage = self.wikipage

        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentUsedTab_preview_wiki(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RESULT
        self.wikipage.content = 'Бла-бла-бла'
        Application.selectedPage = self.wikipage

        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to HTML page and come back to wiki page
        Application.selectedPage = self.htmlpage
        Application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def _getPageMode(self):
        return Application.mainWindow.pagePanel.pageView.GetPageMode()

    def _setPageMode(self, index):
        Application.mainWindow.pagePanel.pageView.SetPageMode(index)
        wx.GetApp().Yield()
