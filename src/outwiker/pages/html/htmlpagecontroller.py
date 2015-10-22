# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController

from htmlpage import HtmlWikiPage


class HtmlPageController (BaseController):
    """GUI controller for HTML page"""
    def __init__(self, application):
        super(HtmlPageController, self).__init__()
        self._application = application


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == HtmlWikiPage.getTypeString():
            params.dialog.appearancePanel.Show()
