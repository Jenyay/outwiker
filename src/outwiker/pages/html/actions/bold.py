#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlBoldAction (BaseAction):
    """
    Выделение текста полужирным шрифтом (добавление тега <B>)
    """
    stringId = u"HtmlBold"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Bold")


    @property
    def description (self):
        return _(u"Bold for HTML pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<b>", u"</b>")
