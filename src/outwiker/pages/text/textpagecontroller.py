# -*- coding: UTF-8 -*-

from outwiker.core.event import pagetype
from outwiker.gui.simplespellcontroller import SimpleSpellController
from textpage import TextPageFactory, TextWikiPage


class TextPageController (object):
    """GUI controller for text page"""
    def __init__(self, application):
        self._application = application
        self._spellController = SimpleSpellController(
            self._application,
            TextWikiPage.getTypeString())

    def initialize(self):
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded

    def clear(self):
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded

        self._spellController.clear()

    @pagetype(TextWikiPage)
    def __onPageViewCreate(self, page):
        assert page is not None
        self._spellController.initialize(page)

    @pagetype(TextWikiPage)
    def __onPageViewDestroy(self, page):
        assert page is not None
        self._spellController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory (TextPageFactory())
