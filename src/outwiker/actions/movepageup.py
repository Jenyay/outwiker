# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, MessageBox


class MovePageUpAction (BaseAction):
    """
    Переместить страницу на одну позицию вверх
    """
    stringId = u"MovePageUp"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Move Page Up")

    @property
    def description(self):
        return _(u"Move page up")

    def run(self, params):
        self.moveCurrentPageUp()

    @testreadonly
    def moveCurrentPageUp(self):
        """
        Переместить текущую страницу на одну позицию вверх
        """
        if self._application.wikiroot is None:
            MessageBox(_(u"Wiki is not open"),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)
            return

        if self._application.wikiroot.selectedPage is not None:
            tree = self._application.mainWindow.treePanel.panel.treeCtrl
            tree.Freeze()
            scrollPos = tree.GetScrollPos(wx.VERTICAL)
            self._application.wikiroot.selectedPage.order -= 1
            tree.SetScrollPos(wx.VERTICAL, scrollPos)
            tree.Thaw()
