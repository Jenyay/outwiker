# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController

from textpage import TextWikiPage


class TextPageController (BaseController):
    """GUI controller for text page"""
    def __init__(self, application):
        super(TextPageController, self).__init__()
        self._application = application


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == TextWikiPage.getTypeString():
            params.dialog.appearancePanel.Hide()
