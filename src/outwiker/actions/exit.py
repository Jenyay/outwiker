#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class ExitAction (BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = u"Exit"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Exit…")


    @property
    def description (self):
        return _(u"Close OutWiker")
    

    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        self._application.mainWindow.Close()
