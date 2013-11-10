#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlAlignCenterAction (BaseAction):
    """
    Выравнивание текста по левому краю
    """
    stringId = u"HtmlAlignCenter"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Center align")


    @property
    def description (self):
        return _(u"Center align for HTML pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u'<div align="center">', u'</div>')
