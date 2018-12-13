# -*- coding: utf-8 -*-

from typing import List

import wx

from outwiker.core.system import getOS
import outwiker.gui.controls.ultimatelistctrl as ULC
from .controls.pagelist import PageList, BaseColumn
from .controls.popupwindow import ResizablePopupWindow


class PageListPopup(ResizablePopupWindow):
    def __init__(self, parent):
        super().__init__(parent)

    def createGUI(self):
        self._pagelist = PageListForTagsCloud(self, self)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._pagelist, 0, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def setPageList(self, pagelist):
        self._pagelist.setPageList(pagelist)

    def setColumns(self, columns: List[BaseColumn]):
        self._pagelist.setColumns(columns)

    def sortByColumn(self, col_index: int):
        self._pagelist.sortByColumn(col_index)

    def getColumns(self) -> List[BaseColumn]:
        self._pagelist.updateColumnsWidth()
        return self._pagelist.getColumns()


class PageListForTagsCloud(PageList):
    '''
    Page list to use in the PageListPopup
    '''
    def __init__(self,
                 parent: wx.Window,
                 popupWindow: ResizablePopupWindow):
        super().__init__(parent)
        # Key - MenuItem ID, value - item from self._columns
        self._popupMenuColumnItems = {}        # type: Dict[int, BaseColumn]

        self._listCtrl.Bind(ULC.EVT_LIST_COL_RIGHT_CLICK,
                            handler=self._onColRightClick)
        self.Bind(wx.EVT_MENU, handler=self._onPopupMenuClick)

    def _onColRightClick(self, event):
        menu = wx.Menu()
        self._popupMenuColumnItems = {}

        for col in self._columns[1:]:
            menu_item = menu.AppendCheckItem(wx.ID_ANY, col.getTitle())
            menu_item.Check(col.visible)
            self._popupMenuColumnItems[menu_item.GetId()] = col

        if getOS().name != 'windows':
            # In Linux popup menu deactivates parent window
            self.GetParent().setDeactivateCount(1)
        self.PopupMenu(menu)

    def _onPopupMenuClick(self, event):
        col = self._popupMenuColumnItems[event.GetId()]
        col.visible = not col.visible
        self._popupMenuColumnItems = {}
        self._updatePageList()
