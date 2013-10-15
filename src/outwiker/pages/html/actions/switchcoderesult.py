#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class SwitchCodeResultAction (BaseAction):
    """
    Переключение между кодом (вики или HTML) и результатом рендеринга
    """
    stringId = u"SwitchCodeResult"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Code / Preview")


    @property
    def description (self):
        return _(u"Switch Code <--> Preview for HTML and wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.switchCodeResult()
