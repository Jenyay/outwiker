# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class TextEntryDialog(TestedDialog):
    """
    The dialog to enter text value with optional prefix
    """
    def __init__(self, parent,
                 title=u'', message=u'', prefix=u'',
                 value=u'',
                 validator=None):
        super(TextEntryDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
            title=title
        )

        # Функция для проверки правильности введенного идентификатора
        self._validator = validator
        self._createGui(message, prefix, value)

        self.Bind(wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)

        self.Center(wx.BOTH)

    def __onOk(self, event):
        if self._validator is None or self._validator(self.Value):
            self.EndModal(wx.ID_OK)

    def _createGui(self, message, prefix, value):
        """
        Create GUI controls
        """
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(2)

        self.messageLabel = wx.StaticText(
            self,
            label=message
        )

        newUidSizer = wx.FlexGridSizer(cols=2)
        newUidSizer.AddGrowableCol(1)

        self.prefixLabel = wx.StaticText(self, label=prefix)
        self.valueTextCtrl = wx.TextCtrl(self, value=value)
        self.valueTextCtrl.SetMinSize((400, -1))

        newUidSizer.Add(self.prefixLabel,
                        flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                        border=2)
        newUidSizer.Add(self.valueTextCtrl, flag=wx.ALL | wx.EXPAND, border=2)

        mainSizer.Add(self.messageLabel, flag=wx.ALL, border=8)
        mainSizer.Add(newUidSizer, flag=wx.ALL | wx.EXPAND, border=8)

        self._createOkCancelButtons(mainSizer)

        self.SetSizer(mainSizer)
        self.Fit()

    def _createOkCancelButtons(self, mainSizer):
        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        mainSizer.Add(
            okCancel,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
            border=8
        )

    def SetPrefix(self, prefix):
        self.prefixLabel.SetLabel(prefix)

    def SetMessage(self, message):
        self.messageLabel.SetLabel(message)

    def SetValidator(self, validator):
        self._validator = validator

    @property
    def Value(self):
        return self.valueTextCtrl.GetValue()

    @Value.setter
    def Value(self, value):
        self.valueTextCtrl.SetValue(value)

    def GetValue(self):
        return self.Value

    def SetValue(self, value):
        self.Value = value

    def ShowModal(self):
        self.valueTextCtrl.SetSelection(0, 0)
        self.valueTextCtrl.SelectAll()
        self.valueTextCtrl.SetFocus()
        return super(TextEntryDialog, self).ShowModal()
