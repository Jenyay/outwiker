# -*- coding: utf-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class BulletStyleDialog(TestedDialog):
    def __init__(self, parent: wx.Window):
        title = _('List item style')
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, title=title)


class BulletStyleDialogController:
    def __init__(self, dialog: BulletStyleDialog):
        self._dialog = dialog
        self._isOk = False

    def ShowModal(self):
        result = self._dialog.ShowModal()
        self._isOk = (result == wx.ID_OK)
        return result
