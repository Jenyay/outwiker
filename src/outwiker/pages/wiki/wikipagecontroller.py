# -*- coding: utf-8 -*-

import os

import wx

from outwiker.core.event import pagetype
import outwiker.core.events
from outwiker.core.style import Style
import outwiker.core.tree
from outwiker.core.treetools import getPageHtmlPath
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.utilites.textfile import writeTextFile

from .defines import PAGE_TYPE_STRING, PREF_PANEL_WIKI
from .listautocomplete import listComplete_wiki
from .wikicolorizercontroller import WikiColorizerController
from .wikipage import WikiPageFactory
from .wikipreferences import WikiPrefGeneralPanel


class WikiPageController:
    """GUI controller for wiki page"""

    def __init__(self, application):
        self._application = application
        self._colorizerController = WikiColorizerController(
            self._application, PAGE_TYPE_STRING
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
        if params.pageType == PAGE_TYPE_STRING:
            params.dialog.showAppearancePanel()

    def __onPreferencesDialogCreate(self, dialog):
        panel = WikiPrefGeneralPanel(dialog.treeBook, self._application)
        prefPanelInfo = PreferencePanelInfo(panel, _("General"))

        dialog.appendPreferenceGroup(_("Wiki Page"), [prefPanelInfo], PREF_PANEL_WIKI)

    @pagetype(PAGE_TYPE_STRING)
    def __onPageViewCreate(self, page):
        if not self._application.testMode:
            self._colorizerController.initialize(page)
        self._application.mainWindow.pagePanel.pageView.SetFocus()

    @pagetype(PAGE_TYPE_STRING)
    def __onPageViewDestroy(self, page):
        if not self._application.testMode:
            self._colorizerController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(WikiPageFactory())

    def __onPageUpdateNeeded(self, page, params):
        if page is None or page.getTypeString() != PAGE_TYPE_STRING or page.readonly:
            return

        if not params.allowCache:
            HtmlCache(page, self._application).resetHash()
        self._updatePage(page)

    @pagetype(PAGE_TYPE_STRING)
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
        path = getPageHtmlPath(page)
        cache = HtmlCache(page, self._application)

        # Проверим, можно ли прочитать уже готовый HTML
        if cache.canReadFromCache() and os.path.exists(path):
            return

        style = Style()
        stylepath = style.getPageStyle(page)
        generator = HtmlGenerator(page, self._application)

        html = generator.makeHtml(stylepath)
        writeTextFile(path, html)
        cache.saveHash()
