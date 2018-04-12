# -*- coding: utf-8 -*-

import wx


class ToolBar2Info(object):
    def __init__(self, toolbar, order):
        '''
        toolbar - instance of the ToolBar2 class
        order - integer number define toolbars order on the window.
        '''
        self.toolbar = toolbar
        self.order = order


class ToolBar2(wx.Panel):
    def __init__(self, parent, order=0):
        '''
        parent - instance of the ToolBar2Container
        '''

        super().__init__(parent)
        self._parent = parent
        self._order = order
        self._elements = []
        self._sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._toolbar = wx.ToolBar(self)
        self._sizer.Add(self._toolbar)
        self.SetSizer(self._sizer)

    def AddButton(self, label, bitmap, button_id=wx.ID_ANY):
        '''
        label - tool tip for the button.
        bitmap - wx.Bitmap or file name.
        '''
        bmp = wx.Bitmap(bitmap)
        new_id = self._toolbar.AddTool(button_id, label, bmp, label).GetId()
        self._setToolbarUpdated()
        return new_id

    def AddCheckButton(self, label, bitmap, button_id=wx.ID_ANY):
        '''
        label - tool tip for the button.
        bitmap - wx.Bitmap or file name.
        '''
        self._setToolbarUpdated()
        bmp = wx.Bitmap(bitmap)
        new_id = self._toolbar.AddTool(button_id, label,
                                       bmp, label,
                                       wx.ITEM_CHECK).GetId()
        return new_id

    def AddSeparator(self):
        self._setToolbarUpdated()
        new_id = self._toolbar.AddSeparator().GetId()
        return new_id

    def _setToolbarUpdated(self):
        self._parent.setToolbarsUpdated()

    def DeleteTool(self, tool_id):
        self._setToolbarUpdated()
        self._toolbar.DeleteTool(tool_id)

    def EnableTool(self, tool_id, enable):
        self._toolbar.EnableTool(tool_id, enable)

    def FindById(self, tool_id):
        return self._toolbar.FindById(tool_id)

    def __getitem__(self, tool_id):
        return self.FindById(tool_id)

    def ToggleTool(self, tool_id, toggle):
        self._toolbar.ToggleTool(tool_id, toggle)

    def Hide(self):
        self._setToolbarUpdated()
        super().Hide()

    def Show(self):
        self._setToolbarUpdated()
        super().Show()

    def Destroy(self):
        self._parent = None
        super().Destroy()

    def Realize(self):
        self._toolbar.Realize()

    def GetToolsCount(self):
        return self._toolbar.GetToolsCount()

    def __len__(self):
        return self.GetToolsCount()

    def IsChecked(self, tool_id):
        return self._toolbar.GetToolState(tool_id)

    def SetToolShortHelp(self, tool_id, helpString):
        self._toolbar.SetToolShortHelp(tool_id, helpString)

    def GetToolEnabled(self, tool_id):
        return self._toolbar.GetToolEnabled(tool_id)

    def GetOrder(self):
        return self._order


class ToolBar2Container(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Key - toolbar_id, value - instance of the ToolBar2Info
        self._toolbars = {}
        self._isUpdated = False
        self._oldClientSize = self.GetClientSize()

        self._mainSizer = wx.WrapSizer()
        self.SetSizer(self._mainSizer)
        self.Bind(wx.EVT_SIZE, handler=self._onSize)

    def __getitem__(self, toolbar_id):
        return self._toolbars[toolbar_id].toolbar

    def __len__(self):
        return len(self._toolbars)

    def createToolBar(self, toolbar_id, order=0):
        if not toolbar_id:
            raise KeyError('Invalid toolbar ID: "{}"'.format(toolbar_id))

        if toolbar_id in self._toolbars:
            raise KeyError('Duplicate toolbars ID: "{}"'.format(toolbar_id))

        toolbar = ToolBar2(self, order=order)
        toolbar_info = ToolBar2Info(toolbar, order)
        self._toolbars[toolbar_id] = toolbar_info
        index = self._getToolBarIndex(order)
        self._mainSizer.Insert(index,
                               toolbar,
                               flag=wx.EXPAND | wx.ALIGN_TOP | wx.ALL,
                               border=4)
        self.GetParent().Layout()
        return toolbar

    def _getToolBarIndex(self, order):
        index = self._mainSizer.GetItemCount()
        for n in range(self._mainSizer.GetItemCount(), -1, -1):
            index = n
            if n == 0:
                break

            item = self._mainSizer.GetItem(n - 1)
            element = item.GetWindow()
            assert isinstance(element, ToolBar2)

            if element.GetOrder() <= order:
                break

        return index

    def getToolBarByIndex(self, index):
        assert index < len(self._toolbars)

        item = self._mainSizer.GetItem(index)
        element = item.GetWindow()
        assert isinstance(element, ToolBar2)

        return element

    def destroyToolBar(self, toolbar_id):
        toolbar = self.__getitem__(toolbar_id)
        self._mainSizer.Detach(toolbar)
        toolbar.Destroy()
        del self._toolbars[toolbar_id]
        self.GetParent().Layout()

    def setToolbarsUpdated(self):
        if not self._isUpdated:
            self.Bind(wx.EVT_IDLE, handler=self._onIdle)
        self._isUpdated = True

    def _onIdle(self, event):
        self._isUpdated = False
        self.Unbind(wx.EVT_IDLE, handler=self._onIdle)
        self.Freeze()

        for toolbar_info in self._toolbars.values():
            toolbar_info.toolbar.Realize()

        self.GetParent().Layout()
        self.Thaw()

    def _onSize(self, event):
        newClientSize = self.GetClientSize()
        if newClientSize != self._oldClientSize:
            self._oldClientSize = newClientSize
            self.setToolbarsUpdated()

        event.Skip()
