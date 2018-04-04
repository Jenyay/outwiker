#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class ToolBar2(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)


if __name__ == '__main__':
    class MyTestFrame(wx.Frame):
        def __init__(self, parent, title):
            super().__init__(parent, wx.ID_ANY, title, size=(600, 400))
            self._createGUI()

            self.newPanelAddButton.Bind(wx.EVT_BUTTON,
                                        handler=self._onNewPanel)

            self.Show()

        def _createGUI(self):
            self._mainSizer = wx.FlexGridSizer(cols=1)
            self._mainSizer.AddGrowableCol(0)

            # ToolBar2
            self.toolbar = ToolBar2(self)
            self._mainSizer.Add(self.toolbar, flag=wx.EXPAND)

            self._createGUIAddPanel()
            self._createGUIAddButton()

            self.SetSizer(self._mainSizer)

        def _createGUIAddPanel(self):
            newPanelSizer = wx.BoxSizer(wx.HORIZONTAL)

            newPanelLabel = wx.StaticText(self, label='New panel ID')
            newPanelSizer.Add(newPanelLabel,
                              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                              border=2)

            self.newPanelIdTextCtrl = wx.TextCtrl(self)
            self.newPanelIdTextCtrl.SetMinSize((200, -1))
            newPanelSizer.Add(self.newPanelIdTextCtrl,
                              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                              border=2)

            self.newPanelAddButton = wx.Button(self, label='Add new panel')
            newPanelSizer.Add(self.newPanelAddButton,
                              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                              border=2)

            self._mainSizer.Add(newPanelSizer, flag=wx.EXPAND)

        def _createGUIAddButton(self):
            newButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

            newButtonLabel = wx.StaticText(self, label='Panel ID')
            newButtonSizer.Add(newButtonLabel,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self.panelIdComboBox = wx.ComboBox(self)
            self.panelIdComboBox.SetMinSize((200, -1))
            newButtonSizer.Add(self.panelIdComboBox,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self.newButtonAddButton = wx.Button(self, label='Add new button')
            newButtonSizer.Add(self.newButtonAddButton,
                               flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)

            self._mainSizer.Add(newButtonSizer, flag=wx.EXPAND)

        def _onNewPanel(self, event):
            panel_id = self.newPanelIdTextCtrl.GetValue().strip()
            if panel_id:
                self.panelIdComboBox.Append(panel_id)
                self.panelIdComboBox.SetSelection(self.panelIdComboBox.GetCount() - 1)

    app = wx.App()
    frame = MyTestFrame(None, 'Test')
    app.MainLoop()
