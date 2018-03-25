# -*- coding: utf-8 -*-

import wx

from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUITest


class PageTabsTest(BaseOutWikerGUITest):
    """
    Tests for the view tabs (Wiki / Preview)
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.config = GeneralGuiConfig(self.application.config)
        self.config.pageTab.remove_option()

        self.wikipage = WikiPageFactory().create(self.wikiroot,
                                                 'Викистраница',
                                                 [])
        self.htmlpage = HtmlPageFactory().create(self.wikiroot,
                                                 'HTML-страница',
                                                 [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        self.config.pageTab.remove_option()

    def testDefaultEmptyContent(self):
        # Page contents are empty. Code tab is selected.
        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentEmptyContent(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        # Page contents are empty. Code tab is selected.
        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testDefaultNotEmptyContent(self):
        # Page contents are not empty. Preview tab is selected.
        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentNotEmptyContent(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        # Page contents are not empty. Preview tab is selected.
        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testDefaultRecentUsedTab_wiki_01(self):
        self.wikipage.content = 'Бла-бла-бла'

        self.application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to HTML page and come back to wiki page
        self.application.selectedPage = self.htmlpage
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentRecentUsedTab_wiki_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.wikipage.content = 'Бла-бла-бла'

        self.application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to HTML page and come back to wiki page
        self.application.selectedPage = self.htmlpage
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testDefaultRecentUsedTab_html_01(self):
        self.htmlpage.content = 'Бла-бла-бла'

        self.application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to wiki page and come back to HTML page
        self.application.selectedPage = self.wikipage
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentRecentUsedTab_html_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.htmlpage.content = 'Бла-бла-бла'

        self.application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to wiki page and come back to HTML page
        self.application.selectedPage = self.wikipage
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testDefaultRecentUsedTab_wiki_02(self):
        self.wikipage.content = ''

        self.application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to HTML page and come back to wiki page
        self.application.selectedPage = self.htmlpage
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentRecentUsedTab_wiki_02(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.wikipage.content = ''

        self.application.selectedPage = self.wikipage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to HTML page and come back to wiki page
        self.application.selectedPage = self.htmlpage
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testDefaultRecentUsedTab_html_02(self):
        self.htmlpage.content = 'Бла-бла-бла'

        self.application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to wiki page and come back to HTML page
        self.application.selectedPage = self.wikipage
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentRecentUsedTab_html_02(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RECENT

        self.htmlpage.content = 'Бла-бла-бла'

        self.application.selectedPage = self.htmlpage
        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to wiki page and come back to HTML page
        self.application.selectedPage = self.wikipage
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testTabEditorAlways_code_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_CODE

        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testTabEditorAlways_code_not_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_CODE

        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testTabEditorAlways_preview_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RESULT

        self.wikipage.content = ''
        self.htmlpage.content = ''

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testTabEditorAlways_preview_not_empty_01(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RESULT

        self.wikipage.content = 'Бла-бла-бла'
        self.htmlpage.content = 'Бла-бла-бла'

        # Select wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to wiki page
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        # Switch to HTML page
        self.application.selectedPage = self.htmlpage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def testRecentUsedTab_code_wiki(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_CODE
        self.wikipage.content = 'Бла-бла-бла'
        self.application.selectedPage = self.wikipage

        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

        self._setPageMode(PAGE_MODE_PREVIEW)

        # Switch to HTML page and come back to wiki page
        self.application.selectedPage = self.htmlpage
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_TEXT)

    def testRecentUsedTab_preview_wiki(self):
        self.config.pageTab.value = GeneralGuiConfig.PAGE_TAB_RESULT
        self.wikipage.content = 'Бла-бла-бла'
        self.application.selectedPage = self.wikipage

        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

        self._setPageMode(PAGE_MODE_TEXT)

        # Switch to HTML page and come back to wiki page
        self.application.selectedPage = self.htmlpage
        self.application.selectedPage = self.wikipage
        self.assertEqual(self._getPageMode(), PAGE_MODE_PREVIEW)

    def _getPageMode(self):
        return self.application.mainWindow.pagePanel.pageView.GetPageMode()

    def _setPageMode(self, index):
        self.application.mainWindow.pagePanel.pageView.SetPageMode(index)
        wx.GetApp().Yield()
