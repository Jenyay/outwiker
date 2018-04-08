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
        super().__init__(parent)
        self._elements = []
        self._sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self._sizer)

        self._reservedElements = 3
        for n in range(self._reservedElements):
            self.AddSeparator()

    def GetElementsCount(self):
        return len(self._elements) - self._reservedElements

    def AddButton(self, label, bitmap, button_id=wx.ID_ANY):
        '''
        label - tool tip for the button.
        bitmap - wx.Bitmap or file name.
        '''
        bmp = wx.Bitmap(bitmap)
        button = wx.BitmapButton(self, button_id, bmp, style=wx.NO_BORDER)
        button.SetToolTip(label)
        self._addElement(button)
        return button.GetId()

    def AddSeparator(self):
        separator = wx.StaticLine(self, style=wx.LI_VERTICAL)
        self._addElement(separator)
        return separator.GetId()

    def _addElement(self, element):
        self._sizer.Add(element, flag=wx.EXPAND)
        self._elements.append(element)
        self._layout()

    def _layout(self):
        self.GetParent().GetParent().Layout()

    def DeleteTool(self, tool_id):
        for n, element in list(enumerate(self._elements)):
            if element.GetId() == tool_id:
                self._sizer.Remove(n)
                element.Close()
                del self._elements[n]
                self._layout()
                break

    def EnableTool(self, tool_id, enable):
        for element in self._elements:
            if element.GetId() == tool_id:
                element.Enable(enable)
                return

        raise KeyError('Tools not found: {}'.format(tool_id))

    def FindById(self, tool_id):
        for element in self._elements:
            if element.GetId() == tool_id:
                return element

        return None

    def ToggleTool(self, tool_id, checked):
        pass

    def IsFocusable(self):
        return False

    def AcceptsFocusRecursively(self):
        return False

    def AcceptsFocus(self):
        return False


class ToolBar2Container(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Key - toolbar_id, value - instance of the ToolBar2
        self._toolbars = {}

        self._mainSizer = wx.WrapSizer()
        self.SetSizer(self._mainSizer)

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
        self._mainSizer.Add(toolbar, flag=wx.EXPAND)
        toolbar.Bind(wx.EVT_BUTTON, handler=self._onButtonClick)
        self.GetParent().Layout()
        return toolbar

    def destroyToolBar(self, toolbar_id):
        toolbar = self.__getitem__(toolbar_id)
        self._mainSizer.Detach(toolbar)
        toolbar.Close()
        del self._toolbars[toolbar_id]
        self.GetParent().Layout()

    def _onButtonClick(self, event):
        new_event = event.Clone()
        new_event.SetEventType(wx.EVT_TOOL.typeId)
        wx.PostEvent(self, new_event)

    def IsFocusable(self):
        return False

    def AcceptsFocusRecursively(self):
        return False

    def AcceptsFocus(self):
        return False


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
