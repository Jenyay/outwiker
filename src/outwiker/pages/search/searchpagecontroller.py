# -*- coding: utf-8 -*-

from .searchpage import SearchPageFactory, SearchWikiPage
from .defines import PAGE_TYPE_STRING


class SearchPageController(object):
    """GUI controller for text page"""

    def __init__(self, application):
        self._application = application

    def initialize(self):
        self._application.onPageDialogPageFactoriesNeeded += (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageDialogPageTypeChanged += (
            self.__onPageDialogPageTypeChanged
        )

    def clear(self):
        self._application.onPageDialogPageFactoriesNeeded -= (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageDialogPageTypeChanged -= (
            self.__onPageDialogPageTypeChanged
        )

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(SearchPageFactory())

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == PAGE_TYPE_STRING:
            params.dialog.hideAppearancePanel()
