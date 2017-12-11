# -*- coding: UTF-8 -*-

from .searchpage import SearchPageFactory


class SearchPageController (object):
    """GUI controller for text page"""
    def __init__(self, application):
        self._application = application


    def initialize (self):
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded


    def clear (self):
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded


    def __onPageDialogPageFactoriesNeeded (self, page, params):
        params.addPageFactory (SearchPageFactory())
