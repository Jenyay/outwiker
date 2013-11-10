#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlUnderlineAction (BaseAction):
    """
    Выделение текста подчеркнутым шрифтом (добавление тега <u>)
    """
    stringId = u"HtmlUnderline"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Underline")


    @property
    def description (self):
        return _(u"Undeline for HTML pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<u>", u"</u>")
