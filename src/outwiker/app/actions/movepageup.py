# -*- coding: utf-8 -*-

import wx

from outwiker.api.core.tree import testreadonly
from outwiker.api.services.messages import showError
from outwiker.gui.baseaction import BaseAction


class MovePageUpAction (BaseAction):
    """
    Переместить страницу на одну позицию вверх
    """
    stringId = "MovePageUp"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Move Page Up")

    @property
    def description(self):
        return _("Move page up")

    def run(self, params):
        self.moveCurrentPageUp()

    @testreadonly
    def moveCurrentPageUp(self):
        """
        Переместить текущую страницу на одну позицию вверх
        """
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _("Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            tree = self._application.mainWindow.treePanel.panel.treeCtrl
            tree.Freeze()
            scrollPos = tree.GetScrollPos(wx.VERTICAL)
            self._application.wikiroot.selectedPage.order -= 1
            tree.SetScrollPos(wx.VERTICAL, scrollPos)
            tree.Thaw()
