#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.pagedialog import createChildPage


class AddChildPageAction (BaseAction):
    """
    Добавить страницу того же уровня, что и выбранная
    """
    stringId = u"AddChildPage"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Add Child Page…")


    @property
    def description (self):
        return _(u"Add child page")
    

    def run (self, params):
        createChildPage (self._application.mainWindow,
                self._application.selectedPage)
