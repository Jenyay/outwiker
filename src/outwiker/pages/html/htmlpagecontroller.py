# -*- coding: UTF-8 -*-

import wx

from outwiker.core.commands import MessageBox
from outwiker.gui.pagedialogpanels.appearancepanel import(
    AppearancePanel,
    AppearanceController)

from outwiker.gui.simplespellcontroller import SimpleSpellController
from htmlpage import HtmlWikiPage, HtmlPageFactory


class HtmlPageController(object):
    """GUI controller for HTML page"""
    def __init__(self, application):
        self._application = application
        self._appearancePanel = None
        self._appearanceController = None
        self._spellController = SimpleSpellController(
            self._application,
            HtmlWikiPage.getTypeString())

    def initialize(self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded

    def clear(self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded

        self._spellController.clear()

    def _addTab(self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel(dialog.getPanelsParent())
            dialog.addPanel(self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController(
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController(self._appearanceController)

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == HtmlWikiPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController(self._appearanceController)
            params.dialog.removePanel(self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None

    def __onPageDialogDestroy(self, page, params):
        self._appearancePanel = None
        self._appearanceController = None

    def __onPageViewCreate(self, page):
        assert page is not None
        self._spellController.initialize(page)

    def __onPageViewDestroy(self, page):
        assert page is not None
        self._spellController.clear()


    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(HtmlPageFactory())

    def __onPageUpdateNeeded(self, page, params):
        if (page is None or
                page.getTypeString() != HtmlWikiPage.getTypeString() or
                page.readonly):
            return

        try:
            page.update()
        except EnvironmentError:
            MessageBox (_(u'Page update error: {}').format(page.title),
                        _(u'Error'),
                        wx.ICON_ERROR | wx.OK)
