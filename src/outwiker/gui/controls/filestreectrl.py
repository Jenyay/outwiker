# -*- coding=utf-8 -*-

from pathlib import Path
from typing import List, Union, Callable, Optional

import wx
from wx.lib.agw.customtreectrl import (CustomTreeCtrl, GenericTreeItem,
                                       TR_AUTO_CHECK_CHILD,
                                       TR_AUTO_CHECK_PARENT)

from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS


FilesTreeSelChangedEvent, EVT_FILES_TREE_SEL_CHANGED = wx.lib.newevent.NewEvent()


class FilesTreeCtrl(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, check_boxes=False):
        super().__init__(parent, id=id)
        self._check_boxes = check_boxes
        self._root_dir: Optional[Path] = None
        self._filter_func: Optional[Callable[[Path], bool]] = None

        self._items_relative = {}
        self._items_full = {}

        self._fileIcons = getOS().fileIcons

        agwStyle = (wx.TR_HAS_BUTTONS |
                    wx.TR_LINES_AT_ROOT |
                    wx.TR_HAS_VARIABLE_ROW_HEIGHT |
                    TR_AUTO_CHECK_CHILD |
                    TR_AUTO_CHECK_PARENT)
        self._tree_ctrl = CustomTreeCtrl(self, agwStyle=agwStyle)
        self._tree_ctrl.SetImageList(self._fileIcons.imageList)
        self._tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED,
                             handler=self._onSelChanged)
        self._layout()

    def _layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(0)
        main_sizer.Add(self._tree_ctrl, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(main_sizer)

    def _onSelChanged(self, event):
        full_path = self.GetSelectionFull()
        relative_path = self.GetSelectionRelative()
        new_event = FilesTreeSelChangedEvent(full_path=full_path,
                                             relative_path=relative_path)
        wx.PostEvent(self, new_event)

    def _getItemType(self):
        return int(self._check_boxes)

    def Clear(self):
        self._tree_ctrl.DeleteAllItems()
        self._items_relative = {}
        self._items_full = {}

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

    def GetSelectionRelative(self):
        selectedItem = self._tree_ctrl.GetSelection()
        full_path = None
        relative_path = None

        if selectedItem is not None:
            full_path = selectedItem.GetData()
            if self._root_dir is not None:
                relative_path = str(full_path.relative_to(self._root_dir))

        return relative_path

    def GetSelectionFull(self):
        selectedItem = self._tree_ctrl.GetSelection()
        full_path = None

        if selectedItem is not None:
            full_path = str(selectedItem.GetData())

        return full_path

    def SetSelectionRelative(self, path_relative: Union[str, Path]) -> bool:
        path_relative = str(path_relative).replace('\\', '/')
        item = self._items_relative.get(path_relative)

        if item == self._tree_ctrl.GetSelection():
            return False

        if item is not None:
            self._tree_ctrl.SelectItem(item)

        return item is not None

    def SetSelectionFull(self, path_full: Union[str, Path]) -> bool:
        path_full = str(path_full).replace('\\', '/')
        item = self._items_full.get(path_full)

        if item == self._tree_ctrl.GetSelection():
            return False

        if item is not None:
            self._tree_ctrl.SelectItem(item)

        return item is not None

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
            child_full = str(child)
            child_relative = str(child.relative_to(self._root_dir)).replace('\\', '/')

            if child.is_dir():
                item = self._tree_ctrl.AppendItem(
                    parent_item,
                    str(child.name),
                    self._getItemType(),
                    image=self._fileIcons.FOLDER_ICON,
                    data=child)

                self._addChildren(item, child)
            else:
                item = self._tree_ctrl.AppendItem(
                    parent_item,
                    str(child.name),
                    self._getItemType(),
                    image=self._fileIcons.getFileImage(str(child)),
                    data=child)

            self._items_full[child_full] = item
            self._items_relative[child_relative] = item
