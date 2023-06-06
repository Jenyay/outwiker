# -*- coding: utf-8 -*-

import wx

from outwiker.core.treetools import testreadonly
from outwiker.app.services.messages import showError
from outwiker.gui.baseaction import BaseAction


class MovePageDownAction(BaseAction):
    """
    Переместить страницу на одну позицию вниз
    """
    stringId = "MovePageDown"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Move Page Down")

    @property
    def description(self):
        return _("Move page down")

    def run(self, params):
        self.moveCurrentPageDown()

    @testreadonly
    def moveCurrentPageDown(self):
        """
        Переместить текущую страницу на одну позицию вниз
        """
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _("Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            tree = self._application.mainWindow.treePanel.panel.treeCtrl
            tree.Freeze()
            scrollPos = tree.GetScrollPos(wx.VERTICAL)
            self._application.wikiroot.selectedPage.order += 1
            tree.SetScrollPos(wx.VERTICAL, scrollPos)
            tree.Thaw()
