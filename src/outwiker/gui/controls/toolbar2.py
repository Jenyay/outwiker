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
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self._buttons = []
        self._sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self._sizer)

    def addTool(self, button_id, label, image_filename):
        bmp = wx.Bitmap(image_filename)
        button = wx.BitmapButton(self, button_id, bmp, style=wx.NO_BORDER)
        button.SetToolTip(label)
        self._sizer.Add(button, flag=wx.EXPAND)
        self.Layout()


class ToolBar2Container(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Key - toolbar_id, value - instance of the ToolBar2
        self._toolbars = {}

        self._mainSizer = wx.WrapSizer()
        self.SetSizer(self._mainSizer)

    def addButton(self, toolbar_id, button_id, label, image_filename):
        toolbar = self._toolbars[toolbar_id].toolbar
        toolbar.addTool(button_id, label, image_filename)
        self._layout()

    def createToolbar(self, toolbar_id, priority=1):
        if not toolbar_id:
            raise KeyError('Invalid toolbar ID: "{}"'.format(toolbar_id))

        if toolbar_id in self._toolbars:
            raise KeyError('Duplicate toolbars ID: "{}"'.format(toolbar_id))

        toolbar = ToolBar2(self)
        toolbar_info = ToolBar2Info(toolbar, priority)
        self._toolbars[toolbar_id] = toolbar_info
        self._mainSizer.Add(toolbar, flag=wx.EXPAND)
        self._layout()

    def _layout(self):
        self.GetParent().Layout()


if __name__ == '__main__':
    class MyTestFrame(wx.Frame):
        def __init__(self, parent, title):
            super().__init__(parent, wx.ID_ANY, title, size=(600, 400))
            self._createGUI()

            self.newToolbarAddButton.Bind(wx.EVT_BUTTON,
                                          handler=self._onNewToolbar)
            self.newButtonAddButton.Bind(wx.EVT_BUTTON,
                                         handler=self._onNewButton)

            self.Show()

        def _createGUI(self):
            self._mainSizer = wx.FlexGridSizer(cols=1)
            self._mainSizer.AddGrowableCol(0)

            # ToolBar2
            self.toolbar = ToolBar2Container(self)
            # self.toolbar.SetMinSize((-1, 40))
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
            button_id = -1
            label = 'Бла-бла-бла'
            image_filename = '../../../images/page.png'
            self.toolbar.addButton(toolbar_id, button_id, label, image_filename)

    app = wx.App()
    frame = MyTestFrame(None, 'Test')
    app.MainLoop()
