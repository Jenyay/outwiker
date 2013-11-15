#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiChildListAction (BaseAction):
    """
    Вставка команды для показа списка дочерних страниц
    """
    stringId = u"WikiChildList"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Children (:childlist:)")


    @property
    def description (self):
        return _(u"Insert (:childlist:) command")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.replaceText (u"(:childlist:)")
