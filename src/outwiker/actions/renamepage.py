#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class RenamePageAction (BaseAction):
    """
    Переименование страницы
    """
    stringId = u"RenamePage"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Rename Page")


    @property
    def description (self):
        return _(u"Rename current page")
    

    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        self._application.mainWindow.treePanel.beginRename()
