# -*- coding=utf-8 -*-

from pathlib import Path
from typing import List, Union, Callable, Optional

import wx
from wx.lib.agw.customtreectrl import (CustomTreeCtrl, GenericTreeItem,
                                       TR_AUTO_CHECK_CHILD,
                                       TR_AUTO_CHECK_PARENT)

from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS


class FilesTreeCtrl(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, check_boxes=False):
        super().__init__(parent, id=id)
        self._check_boxes = check_boxes
        self._root_dir: Optional[Path] = None
        self._filter_func: Optional[Callable[[Path], bool]] = None

        self._fileIcons = getOS().fileIcons

        agwStyle = (wx.TR_HAS_BUTTONS |
                    wx.TR_LINES_AT_ROOT |
                    wx.TR_HAS_VARIABLE_ROW_HEIGHT |
                    TR_AUTO_CHECK_CHILD |
                    TR_AUTO_CHECK_PARENT)
        self._tree_ctrl = CustomTreeCtrl(self, agwStyle=agwStyle)
        self._tree_ctrl.SetImageList(self._fileIcons.imageList)
        self._layout()

    def _layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(0)
        main_sizer.Add(self._tree_ctrl, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(main_sizer)

    def _getItemType(self):
        return int(self._check_boxes)

    def Clear(self):
        self._tree_ctrl.DeleteAllItems()

    def SetFilterFunc(self, filter: Optional[Callable[[Path], bool]] = None):
        self._filter_func = filter
        self.Update()

    def SetRootDir(self, root_dir: Union[Path, str]):
        self._root_dir = Path(root_dir)
        self.Update()

    def Update(self):
        self.Clear()
        if self._root_dir is not None and self._root_dir.exists():
            root_item = self._tree_ctrl.AddRoot(
                _('Attachments'),
                ct_type=self._getItemType(),
                image=self._fileIcons.FOLDER_ICON,
                data=self._root_dir)
            self._addChildren(root_item, self._root_dir)
            self._tree_ctrl.ExpandAll()

    def GetChecked(self):
        checked_list = []
        self._getCheckedChildren(self._tree_ctrl.GetRootItem(), checked_list)
        return checked_list

    def _getCheckedChildren(self, parent_item: GenericTreeItem, checked_list: List):
        if parent_item is not None:
            item, cookie = self._tree_ctrl.GetFirstChild(parent_item)
            while item is not None:
                if item.IsChecked():
                    checked_list.append(item.GetData())

                self._getCheckedChildren(item, checked_list)
                item, cookie = self._tree_ctrl.GetNextChild(
                    parent_item, cookie)

    def _addChildren(self, parent_item: GenericTreeItem, parent_dir: Path):
        children_files = list(parent_dir.iterdir())

        children_files = list(filter(self._filter_func, children_files))

        children_files.sort(key=lambda path: str.lower(str(path)))
        children_files.sort(
            key=lambda path: Attachment.sortByType(str(path)), reverse=True)

        for child in children_files:
            if child.is_dir():
                dir_item = self._tree_ctrl.AppendItem(
                    parent_item,
                    str(child.name),
                    self._getItemType(),
                    image=self._fileIcons.FOLDER_ICON,
                    data=child)
                self._addChildren(dir_item, child)
            else:
                self._tree_ctrl.AppendItem(
                    parent_item,
                    str(child.name),
                    self._getItemType(),
                    image=self._fileIcons.getFileImage(str(child)),
                    data=child)
