#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlTableRowAction (BaseAction):
    """
    Вставить таблицу
    """
    stringId = u"HtmlTableRow"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Table row")


    @property
    def description (self):
        return _(u"Insert a table row for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u'<tr>', u'</tr>')
