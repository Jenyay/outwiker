#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.pagedialog import createSiblingPage


class AddSiblingPageAction (BaseAction):
    """
    Добавить страницу того же уровня, что и выбранная
    """
    stringId = u"AddSiblingPage"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Add Sibling Page…")


    @property
    def description (self):
        return _(u"Add sibling page")
    

    def run (self, params):
        createSiblingPage (self._application.mainWindow,
                self._application.selectedPage)
