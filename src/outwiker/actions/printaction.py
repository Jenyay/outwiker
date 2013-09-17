#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class PrintAction (BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = u"Print"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Print")


    @property
    def description (self):
        return _(u"Print current page")
    

    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        self._application.mainWindow.pagePanel.panel.Print()
