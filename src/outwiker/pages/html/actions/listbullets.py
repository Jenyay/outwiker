#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlListBulletsAction (BaseAction):
    """
    Вставить таблицу
    """
    stringId = u"HtmlListBullets"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Bullets list")


    @property
    def description (self):
        return _(u"Insert a bullets list for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>')
