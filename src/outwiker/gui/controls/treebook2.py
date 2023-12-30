import os.path
from typing import List, Optional

import wx

from outwiker.gui.imagelistcache import ImageListCache


class Treebook2(wx.SplitterWindow):
    def __init__(self, parent: wx.Window, defaultIcon: str):
        super().__init__(parent)
        self._default_icon = defaultIcon
        self._current_page: Optional[wx.Panel] = None
        self._default_leftSize = 300
        self._last_added_section: Optional[wx.TreeItemId] = None
        self._create_gui()

        self._tree.Bind(wx.EVT_TREE_SEL_CHANGED, handler=self._onSelected)

    def _onSelected(self, event):
        if self._current_page is not None:
            self._container_sizer.Clear()
            self._current_page.Hide()

        page = self._tree.GetItemData(event.GetItem())
        if page is not None:
            self._container_sizer.Add(page, flag=wx.EXPAND)
            page.Show()
            self._container.Layout()

        self._current_page = page

    def _create_gui(self):
        self._iconsCache = ImageListCache(self._default_icon)
        self._tree = wx.TreeCtrl(
            self, style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS | wx.TR_NO_LINES
        )
        self._tree.AssignImageList(self._iconsCache.getImageList())
        self._root = self._tree.AddRoot(
            _("Preferences"), image=self._iconsCache.getDefaultImageId()
        )

        self._container = wx.Panel(self)
        self.SplitVertically(
            self._tree, self._container, sashPosition=self._default_leftSize
        )

        self._container_sizer = wx.FlexGridSizer(cols=1)
        self._container_sizer.AddGrowableCol(0)
        self._container_sizer.AddGrowableRow(0)

    def GetParentPanel(self) -> wx.Panel:
        return self.GetWindow2()

    def GetCurrentPage(self) -> Optional[wx.Panel]:
        return self._current_page

    def AddPage(self, page: wx.Window, label: str, icon_fname=None):
        page.Hide()
        self._last_added_section = self._tree.AppendItem(
            self._root, text=label, data=page, image=self._loadIcon(icon_fname)
        )

    def AddSubPage(self, page: wx.Window, label: str, icon_fname=None):
        page.Hide()
        parent = (
            self._last_added_section
            if self._last_added_section is not None
            else self._root
        )
        self._tree.AppendItem(
            parent, text=label, data=page, image=self._loadIcon(icon_fname)
        )

    def GetPages(self) -> List[wx.Panel]:
        return []

    def SetSelection(self, index: int):
        pass

    def ExpandNode(self, index: int):
        pass

    def _loadIcon(self, icon_fname: Optional[str]):
        """
        Добавляет иконку страницы в ImageList и возвращает ее идентификатор.
        Если иконки нет, то возвращает идентификатор иконки по умолчанию
        """
        if icon_fname is None:
            return self._iconsCache.getDefaultImageId()

        icon_fname = os.path.abspath(icon_fname)
        imageId = self._iconsCache.add(icon_fname)

        if imageId is None:
            imageId = self._iconsCache.getDefaultImageId()

        return imageId
