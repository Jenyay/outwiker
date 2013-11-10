#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlListNumbersAction (BaseAction):
    """
    Вставить таблицу
    """
    stringId = u"HtmlListNumbers"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Numbers list")


    @property
    def description (self):
        return _(u"Insert a numbers list for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>')
