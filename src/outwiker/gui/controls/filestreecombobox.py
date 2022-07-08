# -*- coding=utf-8 -*-

from pathlib import Path
from typing import Callable, Optional, Union

import wx

from .filestreectrl import FilesTreeCtrl, EVT_FILES_TREE_SEL_CHANGED


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

    def GetRootDir(self) -> Union[Path, str]:
        return self._combo_popup.GetRootDir()

    def GetValue(self):
        return self._combo_ctrl.GetValue()

    def SetValue(self, path_relative: str):
        return self._combo_ctrl.SetValue(path_relative)


class FilesTreeComboPopup(wx.ComboPopup):
    def __init__(self):
        super().__init__()
        self._tree_ctrl = None
        self._skip_dismiss = False

    def _onFileSelected(self, event):
        if not self._skip_dismiss:
            self.Dismiss()

        self._skip_dismiss = False

    def Clear(self):
        self._tree_ctrl.Clear()

    def SetFilterFunc(self, filter: Optional[Callable[[Path], bool]] = None):
        self._tree_ctrl.SetFilterFunc(filter)

    def SetRootDir(self, root_dir: Union[Path, str]):
        self._tree_ctrl.SetRootDir(root_dir)

    def GetRootDir(self) -> Union[Path, str]:
        return self._tree_ctrl.GetRootDir()

    # The following methods are those that are overridable from the
    # ComboPopup base class.
    def Create(self, parent):
        self._tree_ctrl = FilesTreeCtrl(parent)
        self._tree_ctrl.Bind(EVT_FILES_TREE_SEL_CHANGED,
                             handler=self._onFileSelected)
        return True

    def GetControl(self):
        return self._tree_ctrl

    def SetStringValue(self, path_relative):
        self._skip_dismiss = self._tree_ctrl.SetSelectionRelative(path_relative)

    def GetStringValue(self):
        return self._tree_ctrl.GetSelectionRelative()
