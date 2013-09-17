#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class SaveAction (BaseAction):
    """
    Сохранить заметку
    """
    stringId = u"SaveNote"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Save")


    @property
    def description (self):
        return _(u"Save current note")
    

    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        self._application.onForceSave()
