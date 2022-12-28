# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional

import wx

from outwiker.core.system import getImagesDir
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.safeimagelist import SafeImageList


class ListItemStyleDialog(TestedDialog):
    def __init__(self, parent: wx.Window):
        title = _('List item style')
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, title=title)
        self._styles_list = None
        self._create_gui()
        self.SetSize((300, 300))

    def ShowModal(self):
        self._styles_list.SetFocus()
        return super().ShowModal()

    def SetImageList(self, image_list):
        self._styles_list.SetImageList(image_list, wx.IMAGE_LIST_SMALL)

    def AddItem(self, title: str, image_index: Optional[int]):
        count = self._styles_list.GetItemCount()
        self._styles_list.InsertItem(count, title, image_index)

    def Clear(self):
        self._styles_list.ClearAll()

    def SetSelection(self, index):
        self._styles_list.Select(index)

    def GetSelection(self) -> int:
        return self._styles_list.GetFirstSelected()

    def _create_gui(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(0)

        self._styles_list = wx.ListView(self, style=wx.LC_LIST | wx.LC_SINGLE_SEL)
        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        main_sizer.Add(self._styles_list,
                flag=wx.ALL | wx.EXPAND,
                border=2)
        main_sizer.Add(okCancel,
                flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                border=4)

        self.SetSizer(main_sizer)


class ListItemStyleDialogController:
    def __init__(self, dialog: ListItemStyleDialog):
        self._dialog = dialog
        self._isOk = False

        self._width = 16
        self._height = 16
        bullets_dir = 'bullets'

        self._styles = [
            (None, 'bullet.svg', _('Default')),
            ('[ ]', 'todo.svg', _('List item')),
            ('[/]', 'incomplete.svg', _('List item')),
            ('[x]', 'complete.svg', _('List item')),
            ('[*]', 'star.svg', _('List item')),
            ('[+]', 'plus.svg', _('List item')),
            ('[-]', 'minus.svg', _('List item')),
            ('[o]', 'circle.svg', _('List item')),
            ('[v]', 'check.svg', _('List item')),
            ('[<]', 'lt.svg', _('List item')),
            ('[>]', 'gt.svg', _('List item')),
            ('[]', 'empty.svg', _('Invisible')),
            ]

        bullets_path = Path(getImagesDir(), bullets_dir)
        self._image_list = SafeImageList(self._width, self._height, dialog.GetDPIScaleFactor())
        self._dialog.SetImageList(self._image_list)
        self._dialog.Clear()

        for wiki, fname, title in self._styles:
            if fname is not None:
                index = self._image_list.AddFromFile(bullets_path / fname)
                self._dialog.AddItem(title, index)

        self._dialog.SetSelection(0)

    def ShowModal(self):
        result = self._dialog.ShowModal()
        self._isOk = (result == wx.ID_OK)
        return result

    def GetStyle(self) -> Optional[str]:
        if self._isOk:
            return self._styles[self._dialog.GetSelection()][0]
