# -*- coding: utf-8 -*-

import os

from outwiker.api.core.events import pagetype
from outwiker.api.core.text import writeTextFile
from outwiker.api.core.pagecontentcache import PageContentCache, WikiHashCalculator
from outwiker.api.core.pagestyle import getPageStyle
from outwiker.api.core.tree import addPageFactory, getPageHtmlPath, removePageFactory

from .colorizercontroller import ColorizerController
from .markdownhtmlgenerator import MarkdownHtmlGenerator
from .markdownpage import MarkdownPageFactory, MarkdownPage
from .i18n import get_
from .defines import PAGE_TYPE_STRING


class Controller:
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        self._plugin = plugin
        self._application = application

        self._colorizerController = ColorizerController(
            self._application, PAGE_TYPE_STRING
        )

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        addPageFactory(MarkdownPageFactory())
        self._application.onPageDialogPageFactoriesNeeded += (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageTypeChanged += (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded

    def clear(self):
        """
        Вызывается при отключении плагина
        """
        removePageFactory(PAGE_TYPE_STRING)
        self._application.onPageDialogPageFactoriesNeeded -= (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageTypeChanged -= (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(MarkdownPageFactory())

    @pagetype(PAGE_TYPE_STRING)
    def __onPageViewCreate(self, page):
        self._colorizerController.initialize(page)

    @pagetype(PAGE_TYPE_STRING)
    def __onPageViewDestroy(self, page):
        self._colorizerController.clear()

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == PAGE_TYPE_STRING:
            params.dialog.showAppearancePanel()

    @pagetype(PAGE_TYPE_STRING)
    def __onPageUpdateNeeded(self, page, params):
        if page.readonly:
            return

        if not params.allowCache:
            self._getPageContentCache(page).resetHash()
        self._updatePage(page)

    def _updatePage(self, page):
        path = getPageHtmlPath(page)
        cache = self._getPageContentCache(page)

        # Проверим, можно ли прочитать уже готовый HTML
        if cache.canReadFromCache() and os.path.exists(path):
            return

        stylepath = getPageStyle(page)
        generator = MarkdownHtmlGenerator(page)

        html = generator.makeHtml(stylepath)
        writeTextFile(path, html)
        cache.saveHash()

    def _getPageContentCache(self, page) -> PageContentCache:
        return PageContentCache(
            page, WikiHashCalculator(self._application), self._application
        )
