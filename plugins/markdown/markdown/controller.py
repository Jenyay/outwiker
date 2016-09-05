# -*- coding: UTF-8 -*-

from outwiker.core.factoryselector import FactorySelector

from .markdownpage import MarkdownPageFactory, MarkdownPage
from .colorizercontroller import ColorizerController


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application
        self._colorizerController = ColorizerController(
            self._application,
            MarkdownPage.getTypeString())

    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        FactorySelector.addFactory(MarkdownPageFactory())
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

    def clear (self):
        """
        Вызывается при отключении плагина
        """
        FactorySelector.removeFactory (MarkdownPageFactory().getTypeString())
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

    def __onPageDialogPageFactoriesNeeded (self, page, params):
        params.addPageFactory (MarkdownPageFactory())

    def __onPageViewCreate(self, page):
        assert page is not None
        if page.getTypeString() == MarkdownPage.getTypeString():
            self._colorizerController.initialize(page)

    def __onPageViewDestroy(self, page):
        assert page is not None
        if page.getTypeString() == MarkdownPage.getTypeString():
            self._colorizerController.clear()
