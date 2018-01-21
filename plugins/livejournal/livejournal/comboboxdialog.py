# -*- coding: utf-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class ComboBoxDialog(TestedDialog):
    def __init__(self, parent, message, title, comboStyle):
        """
        parent - родительское окно для диалога
        message - сообщение, выводимое в диалоге
        title - заголовок диалога
        readonly - должен ли быть комбобокс доступен только для чтения?
        """
        super().__init__(parent)

        self.__createGui(comboStyle)

        self._messageCtrl.SetLabel(message)
        self.SetTitle(title)

        self.Fit()
        self._comboBox.SetFocus()

    def __createGui(self, comboStyle):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(1)

        self._messageCtrl = wx.StaticText(self, -1, u"")
        self._comboBox = wx.ComboBox(self, -1, style=comboStyle)
        self._comboBox.SetMinSize((200, -1))

        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        mainSizer.Add(self._messageCtrl,
                      1,
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.Add(self._comboBox,
                      1,
                      wx.ALL | wx.EXPAND,
                      border=2)
        mainSizer.AddSpacer(1)
        mainSizer.Add(okCancel,
                      1,
                      wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                      border=2)

        self.SetSizer(mainSizer)

    def AppendItems(self, items):
        self._comboBox.AppendItems(items)

    def Clear(self):
        self._comboBox.Clear()

    def SetSelection(self, index):
        self._comboBox.SetSelection(index)

    def GetValue(self):
        return self._comboBox.GetValue()

    def SetValue(self, value):
        self._comboBox.SetValue(value)

    Value = property(GetValue, SetValue)

    def GetStrings(self):
        return self._comboBox.GetStrings()
