# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
import outwiker.pages.wiki.gui.bulletstyledialog as bsd


class ListItemStyleAction(BaseAction):
    """
    Show dialog to select list item style (bullet)
    """
    stringId = "ListItemStyle"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("List item style...")

    @property
    def description(self):
        return _("Select list item style (bullet)")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None
        assert self._application.selectedPage is not None

        with bsd.BulletStyleDialog(self._application.mainWindow) as dlg:
            controller = bsd.BulletStyleDialogController(dlg)
            if controller.ShowModal() == wx.ID_OK:
                editor = self._application.mainWindow.pagePanel.pageView.codeEditor
