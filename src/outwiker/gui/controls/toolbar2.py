# -*- coding: utf-8 -*-

import wx


class ToolBar2Info(object):
    def __init__(self, toolbar, priority):
        '''
        toolbar - instance of the ToolBar2 class
        priority - integer number define toolbars order on the window.
        '''
        self.toolbar = toolbar
        self.priority = priority


class ToolBar2(wx.Panel):
    def __init__(self, parent):
        '''
        parent - instance of the ToolBar2Container
        '''

        super().__init__(parent)
        self._parent = parent
        self._elements = []
        self._sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._toolbar = wx.ToolBar(self)
        self._sizer.Add(self._toolbar)
        self.SetSizer(self._sizer)

        self._reservedElements = 0
        for n in range(self._reservedElements):
            self.AddSeparator()

        self.Fit()

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

    def GetToolState(self, tool_id):
        return self._toolbar.GetToolState(tool_id)

    def SetToolShortHelp(self, tool_id, helpString):
        self._toolbar.SetToolShortHelp(tool_id, helpString)

    def GetToolEnabled(self, tool_id):
        return self._toolbar.GetToolEnabled(tool_id)


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

    def createToolbar(self, toolbar_id, priority=1):
        if not toolbar_id:
            raise KeyError('Invalid toolbar ID: "{}"'.format(toolbar_id))

        if toolbar_id in self._toolbars:
            raise KeyError('Duplicate toolbars ID: "{}"'.format(toolbar_id))

        toolbar = ToolBar2(self)
        toolbar_info = ToolBar2Info(toolbar, priority)
        self._toolbars[toolbar_id] = toolbar_info
        self._mainSizer.Add(toolbar, flag=wx.EXPAND | wx.ALIGN_TOP | wx.ALL, border=4)
        self.GetParent().Layout()
        return toolbar

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


if __name__ == '__main__':
    class MyTestFrame(wx.Frame):
        def __init__(self, parent, title):
            super().__init__(parent, wx.ID_ANY, title, size=(600, 400))
            self._createGUI()

            self.newToolbarAddButton.Bind(wx.EVT_BUTTON,
                                          handler=self._onNewToolbar)
            self.newButtonAddButton.Bind(wx.EVT_BUTTON,
                                         handler=self._onNewButton)
            self.newSeparatorButton.Bind(wx.EVT_BUTTON,
                                         handler=self._onAddSeparator)

            self.Show()

        def _createGUI(self):
            self._mainSizer = wx.FlexGridSizer(cols=1)
            self._mainSizer.AddGrowableCol(0)

            # ToolBar2
            self.toolbar = ToolBar2Container(self)
            self.Bind(wx.EVT_TOOL, handler=self._onTool)
            self._mainSizer.Add(self.toolbar, flag=wx.EXPAND)

            self._createGUIAddPanel()
            self._createGUIAddButton()

            self.SetSizer(self._mainSizer)

        def _createGUIAddPanel(self):
            newToolbarSizer = wx.BoxSizer(wx.HORIZONTAL)

            newToolbarLabel = wx.StaticText(self, label='New panel ID')
            newToolbarSizer.Add(newToolbarLabel,
                                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                border=2)

            self.newToolbarIdTextCtrl = wx.TextCtrl(self)
            self.newToolbarIdTextCtrl.SetMinSize((200, -1))
            newToolbarSizer.Add(self.newToolbarIdTextCtrl,
                                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                border=2)

            self.newToolbarAddButton = wx.Button(self, label='Add new toolbar')
            newToolbarSizer.Add(self.newToolbarAddButton,
                                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                border=2)

            self._mainSizer.Add(newToolbarSizer, flag=wx.EXPAND)

        def _createGUIAddButton(self):
            newButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

            newButtonLabel = wx.StaticText(self, label='Toolbar ID')
            newButtonSizer.Add(newButtonLabel,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self.toolbarIdComboBox = wx.ComboBox(self)
            self.toolbarIdComboBox.SetMinSize((200, -1))
            newButtonSizer.Add(self.toolbarIdComboBox,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self.newButtonAddButton = wx.Button(self, label='Add new button')
            newButtonSizer.Add(self.newButtonAddButton,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self.newSeparatorButton = wx.Button(self, label='Add separator')
            newButtonSizer.Add(self.newSeparatorButton,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self._mainSizer.Add(newButtonSizer, flag=wx.EXPAND)

        def _onNewToolbar(self, event):
            toolbar_id = self.newToolbarIdTextCtrl.GetValue().strip()
            priority = 1

            if toolbar_id:
                self.toolbarIdComboBox.Append(toolbar_id)
                self.toolbarIdComboBox.SetSelection(self.toolbarIdComboBox.GetCount() - 1)
                self.toolbar.createToolbar(toolbar_id, priority)
                self.newToolbarIdTextCtrl.SetValue('')

        def _onNewButton(self, event):
            toolbar_id = self.toolbarIdComboBox.GetStringSelection()
            label = 'Бла-бла-бла'
            # bitmap = '../../../images/page.png'
            bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION)
            self.toolbar[toolbar_id].AddButton(label, bitmap)

        def _onAddSeparator(self, event):
            toolbar_id = self.toolbarIdComboBox.GetStringSelection()
            self.toolbar[toolbar_id].AddSeparator()

        def _onTool(self, event):
            print(event.GetId())

    app = wx.App()
    frame = MyTestFrame(None, 'Test')
    app.MainLoop()
