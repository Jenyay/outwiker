# -*- coding: UTF-8 -*-

import wx
from wx.lib.newevent import NewEvent


PopupButtonMenuClick, EVT_POPUP_BUTTON_MENU_CLICK = NewEvent()


# Added in outwiker.gui 1.3
class PopupButton(wx.Panel):
    def __init__(self, parent, bitmap):
        super(PopupButton, self).__init__(parent)
        # Key - menu item's id
        # Value - user's object
        self._items = {}
        self._createGUI(bitmap)
        self.Bind(wx.EVT_MENU, handler=self._onMenuClick)

    def appendMenuItem(self, title, obj):
        menuitem_id = wx.NewId()
        self._items[menuitem_id] = obj
        self._menu.Append(menuitem_id, title)

    def _createGUI(self, bitmap):
        self._menu = wx.Menu()
        self._button = wx.BitmapButton(self, wx.ID_ANY, bitmap)
        self._button.Bind(wx.EVT_BUTTON, handler=self._onButtonClick)

        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._button, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

    def _onButtonClick(self, event):
        rect = self.GetRect()
        self.PopupMenu(self._menu, rect.GetBottomLeft())

    def _onMenuClick(self, event):
        item_id = event.GetId()
        assert item_id in self._items
        propagationLevel = 10
        newevent = PopupButtonMenuClick(data=self._items[item_id])
        newevent.ResumePropagation(propagationLevel)
        wx.PostEvent(self, newevent)
