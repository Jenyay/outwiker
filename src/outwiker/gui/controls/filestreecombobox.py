# -*- coding=utf-8 -*-

from pathlib import Path
from typing import Callable, Optional, Union

import wx

from .filestreectrl import FilesTreeCtrl


class FilesTreeComboBox(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY):
        super().__init__(parent, id=id)
        self._combo_popup = FilesTreeComboPopup()
        self._combo_ctrl = wx.ComboCtrl(self)
        self._combo_ctrl.SetPopupControl(self._combo_popup)
        self._layout()

    def _layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(0)
        main_sizer.Add(self._combo_ctrl, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(main_sizer)

    def Clear(self):
        self._combo_popup.Clear()

    def SetFilterFunc(self, filter: Optional[Callable[[Path], bool]] = None):
        self._combo_popup.SetFilterFunc(filter)

    def SetRootDir(self, root_dir: Union[Path, str]):
        self._combo_popup.SetRootDir(root_dir)


class FilesTreeComboPopup(wx.ComboPopup):
    def __init__(self):
        super().__init__()
        self._tree_ctrl = None

    def Clear(self):
        self._tree_ctrl.Clear()

    def SetFilterFunc(self, filter: Optional[Callable[[Path], bool]] = None):
        self._tree_ctrl.SetFilterFunc(filter)

    def SetRootDir(self, root_dir: Union[Path, str]):
        self._tree_ctrl.SetRootDir(root_dir)

    # The following methods are those that are overridable from the
    # ComboPopup base class.
    def Create(self, parent):
        self._tree_ctrl = FilesTreeCtrl(parent)
        return True

    def Init(self):
        pass

    def GetControl(self):
        return self._tree_ctrl

    def SetStringValue(self, val):
        pass

    def GetStringValue(self):
        return ''
