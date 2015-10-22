# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController

from searchpage import SearchWikiPage


class SearchPageController (BaseController):
    """GUI controller for search page"""
    def __init__(self, application):
        super(SearchPageController, self).__init__()
        self._application = application


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == SearchWikiPage.getTypeString():
            params.dialog.appearancePanel.Hide()
