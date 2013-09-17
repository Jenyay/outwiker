#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import closeWiki


class CloseAction (BaseAction):
    """
    Закрытие дерева заметок
    """
    stringId = u"CloseTree"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Close")


    @property
    def description (self):
        return _(u"Close a tree notes")
    

    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        closeWiki (self._application)
