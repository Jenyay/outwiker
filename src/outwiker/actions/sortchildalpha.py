#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, MessageBox


class SortChildAlphabeticalAction (BaseAction):
    """
    Отсортировать дочерние страницы по алфавиту
    """
    stringId = u"SortChildAlphabetically"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Sort Children Pages Alphabetically")


    @property
    def description (self):
        return _(u"Sort children pages alphabetically")
    

    def run (self, params):
        self.sortChildren()


    @testreadonly
    def sortChildren (self):
        if self._application.wikiroot == None:
            MessageBox (_(u"Wiki is not open"), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
            return

        if self._application.wikiroot.selectedPage != None:
            self._application.wikiroot.selectedPage.sortChildrenAlphabetical ()
        else:
            self._application.wikiroot.sortChildrenAlphabetical ()
