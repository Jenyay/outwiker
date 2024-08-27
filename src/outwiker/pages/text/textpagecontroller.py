# -*- coding: utf-8 -*-

from outwiker.core.event import pagetype
from outwiker.gui.simplespellcontroller import SimpleSpellController
from .textpage import TextPageFactory, TextWikiPage
from .defines import PAGE_TYPE_STRING


class TextPageController:
    """GUI controller for text page"""
    def __init__(self, application):
        self._application = application
        self._spellController = SimpleSpellController(
            self._application,
            PAGE_TYPE_STRING)

    def initialize(self):
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged

    def clear(self):
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged

        if not self._application.testMode:
            self._spellController.clear()

    @pagetype(TextWikiPage)
    def __onPageViewCreate(self, page):
        assert page is not None
        if not self._application.testMode:
            self._spellController.initialize(page)

    @pagetype(TextWikiPage)
    def __onPageViewDestroy(self, page):
        assert page is not None
        if not self._application.testMode:
            self._spellController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory (TextPageFactory())

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == PAGE_TYPE_STRING:
            params.dialog.hideAppearancePanel()
