# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, MessageBox


class MovePageDownAction (BaseAction):
    """
    Переместить страницу на одну позицию вниз
    """
    stringId = u"MovePageDown"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Move Page Down")


    @property
    def description (self):
        return _(u"Move page down")


    def run (self, params):
        self.moveCurrentPageDown ()


    @testreadonly
    def moveCurrentPageDown (self):
        """
        Переместить текущую страницу на одну позицию вниз
        """
        if self._application.wikiroot is None:
            MessageBox (_(u"Wiki is not open"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return

        if self._application.wikiroot.selectedPage is not None:
            tree = self._application.mainWindow.treePanel.panel.treeCtrl
            tree.Freeze()
            scrollPos = tree.GetScrollPos (wx.VERTICAL)
            self._application.wikiroot.selectedPage.order += 1
            tree.SetScrollPos (wx.VERTICAL, scrollPos)
            tree.Thaw()
