# -*- coding: utf-8 -*-

import os

import wx

from outwiker.core.style import Style
from outwiker.core.event import pagetype
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.utilites.textfile import writeTextFile

from .wikipage import WikiWikiPage, WikiPageFactory
from .wikipreferences import WikiPrefGeneralPanel
from .wikicolorizercontroller import WikiColorizerController
from .listautocomplete import listComplete_wiki
from .defines import PREF_PANEL_WIKI

# For type hints
import outwiker.core.tree
import outwiker.core.events


class WikiPageController:
    """GUI controller for wiki page"""

    def __init__(self, application):
        self._application = application
        self._colorizerController = WikiColorizerController(
            self._application, WikiWikiPage.getTypeString()
        )

    def initialize(self):
        self._application.onPageDialogPageTypeChanged += (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded
        self._application.onTextEditorKeyDown += self.__onTextEditorKeyDown

    def clear(self):
        self._application.onPageDialogPageTypeChanged -= (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded
        self._application.onTextEditorKeyDown -= self.__onTextEditorKeyDown
        if not self._application.testMode:
            self._colorizerController.clear()

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == WikiWikiPage.getTypeString():
            params.dialog.showAppearancePanel()

    def __onPreferencesDialogCreate(self, dialog):
        panel = WikiPrefGeneralPanel(dialog.treeBook)
        prefPanelInfo = PreferencePanelInfo(panel, _("General"))

        dialog.appendPreferenceGroup(_("Wiki Page"), [prefPanelInfo], PREF_PANEL_WIKI)

    @pagetype(WikiWikiPage)
    def __onPageViewCreate(self, page):
        if not self._application.testMode:
            self._colorizerController.initialize(page)
        self._application.mainWindow.pagePanel.pageView.SetFocus()

    @pagetype(WikiWikiPage)
    def __onPageViewDestroy(self, page):
        if not self._application.testMode:
            self._colorizerController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(WikiPageFactory())

    def __onPageUpdateNeeded(self, page, params):
        if (
            page is None
            or page.getTypeString() != WikiWikiPage.getTypeString()
            or page.readonly
        ):
            return

        if not params.allowCache:
            HtmlCache(page, self._application).resetHash()
        self._updatePage(page)

    @pagetype(WikiWikiPage)
    def __onTextEditorKeyDown(
        self,
        page: outwiker.core.tree.WikiPage,
        params: outwiker.core.events.TextEditorKeyDownParams,
    ) -> None:
        if params.keyCode == wx.WXK_RETURN and not params.hasModifiers():
            result = listComplete_wiki(params.editor)
            if result:
                params.processed = True
                params.disableOutput = True

    def _updatePage(self, page):
        path = page.getHtmlPath()
        cache = HtmlCache(page, self._application)

        # Проверим, можно ли прочитать уже готовый HTML
        if cache.canReadFromCache() and os.path.exists(path):
            return

        style = Style()
        stylepath = style.getPageStyle(page)
        generator = HtmlGenerator(page)

        html = generator.makeHtml(stylepath)
        writeTextFile(path, html)
        cache.saveHash()
