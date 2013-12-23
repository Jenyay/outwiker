#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import removePage


class RemovePageAction (BaseAction):
    """
    Удалить текущую страницу
    """
    stringId = u"RemovePage"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Remove Page…")


    @property
    def description (self):
        return _(u"Remove current page and all children")
    

    def run (self, params):
        if self._application.selectedPage != None:
            removePage (self._application.wikiroot.selectedPage)
