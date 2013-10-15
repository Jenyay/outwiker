#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiEscapeHtmlAction (BaseAction):
    """
    Преобразовать некоторые символы в и их HTML-представление
    """
    stringId = u"EscapeHtml"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Convert HTML Symbols")


    @property
    def description (self):
        return _(u"Convert HTML Symbols for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        self._application.mainWindow.pagePanel.pageView.codeEditor.escapeHtml(None)
