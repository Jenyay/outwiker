#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import createNewWiki


class NewAction (BaseAction):
    """
    Создание нового дерева заметок
    """
    stringId = u"NewTree"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"New…")


    @property
    def description (self):
        return _(u"Create a new tree notes")
    

    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        createNewWiki (self._application.mainWindow)
