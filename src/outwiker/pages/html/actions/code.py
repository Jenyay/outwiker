#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlCodeAction (BaseAction):
    """
    Выделение текста тегом <code>
    """
    stringId = u"HtmlCode"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Code")


    @property
    def description (self):
        return _(u"Insert code for HTML pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<code>", u"</code>")
