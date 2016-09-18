# -*- coding: UTF-8 -*-

from outwiker.core.factoryselector import FactorySelector
from outwiker.gui.pagedialogpanels.appearancepanel import(AppearancePanel,
                                                          AppearanceController)

from .markdownpage import MarkdownPageFactory, MarkdownPage
from .colorizercontroller import ColorizerController
from .i18n import get_


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._appearancePanel = None
        self._appearanceController = None

        self._colorizerController = ColorizerController(
            self._application,
            MarkdownPage.getTypeString())

    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        FactorySelector.addFactory(MarkdownPageFactory())
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy

    def clear (self):
        """
        Вызывается при отключении плагина
        """
        FactorySelector.removeFactory (MarkdownPageFactory().getTypeString())
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy

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

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == MarkdownPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController(self._appearanceController)
            params.dialog.removePanel(self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None

    def _addTab(self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel(dialog.getPanelsParent())
            dialog.addPanel(self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController(
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController(self._appearanceController)

    def __onPageDialogDestroy(self, page, params):
        self._appearancePanel = None
        self._appearanceController = None
