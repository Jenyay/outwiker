# -*- coding: UTF-8 -*-

from textspellcontroller import TextSpellController


class TextPageController (object):
    """GUI controller for text page"""
    def __init__(self, application):
        self._application = application
        self._spellController = TextSpellController (self._application)


    def initialize (self):
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy


    def clear (self):
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._spellController.clear()


    def __onPageViewCreate (self, page):
        assert page is not None
        self._spellController.initialize(page)


    def __onPageViewDestroy (self, page):
        assert page is not None
        self._spellController.clear()
