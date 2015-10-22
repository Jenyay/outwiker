# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController

from wikipage import WikiWikiPage


class WikiPageController (BaseController):
    """GUI controller for wiki page"""
    def __init__(self, application):
        super(WikiPageController, self).__init__()
        self._application = application


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == WikiWikiPage.getTypeString():
            params.dialog.appearancePanel.Show()
