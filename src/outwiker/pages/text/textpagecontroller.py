# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController

from textpage import TextWikiPage
from textspellcontroller import TextSpellController


class TextPageController (BaseController):
    """GUI controller for text page"""
    def __init__(self, application):
        super(TextPageController, self).__init__()
        self._application = application
        self._spellController = TextSpellController (self._application)


    def initialize (self):
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy


    def clear (self):
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy


    def __onPageViewCreate (self, page):
        assert page is not None

        if page.getTypeString() == TextWikiPage.getTypeString():
            self._spellController.initialize()


    def __onPageViewDestroy (self, page):
        assert page is not None

        if page.getTypeString() == TextWikiPage.getTypeString():
            self._spellController.clear()
