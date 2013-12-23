#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.actions.showhidebase import ShowHideBaseAction


class ShowHideTreeAction (ShowHideBaseAction):
    """
    Показать / скрыть панель с деревом заметок
    """
    stringId = u"ShowHideTree"

    def __init__ (self, application):
        super (ShowHideTreeAction, self).__init__ (application)


    @property
    def title (self):
        return _(u"Notes Tree")


    @property
    def description (self):
        return _(u"Show / hide a notes tree panel")
    

    def getPanel (self):
        return self._application.mainWindow.treePanel
