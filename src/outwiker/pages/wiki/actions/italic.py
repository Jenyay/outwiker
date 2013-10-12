#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiItalicAction (BaseAction):
    """
    Выделение текста курсивным шрифтом
    """
    stringId = u"WikiItalic"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Italic")


    @property
    def description (self):
        return _(u"Italic for wiki pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"''", u"''")
