# -*- coding: utf-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog

from markdown.i18n import get_


class ImageDialog (TestedDialog):
    def __init__(self, parent):
        """
        parent - parent window
        """
        global _
        _ = get_()
        super(ImageDialog, self).__init__(parent, title=_("Image"))

        self._createGui()
        self.filesListCombo.SetFocus()
        self.Center(wx.BOTH)

    @property
    def fileName(self):
        return self.filesListCombo.GetValue()

    @fileName.setter
    def fileName(self, value):
        self.filesListCombo.SetValue(value)

    @property
    def comment(self):
        return self.commentText.GetValue()

    @comment.setter
    def comment(self, value):
        self.commentText.SetValue(value)

    @property
    def filesList(self):
        return self.filesListCombo.GetItems()

    @filesList.setter
    def filesList(self, filesList):
        self.filesListCombo.SetItems(filesList)

    def _createGui(self):
        # Элементы для выбора имени файла
        filenameLabel = wx.StaticText(self, label=_(u"File name or link"))
        self.filesListCombo = wx.ComboBox(self, style=wx.CB_DROPDOWN)
        self.filesListCombo.SetSelection(0)
        self.filesListCombo.SetMinSize((250, -1))

        # Элементы для выбора размера
        commentLabel = wx.StaticText(self, label=_(u"Comment"))

        self.commentText = wx.TextCtrl(self)
        self.commentText.SetMinSize((250, -1))

        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        # Расстановка элементов
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(2)

        mainSizer.Add(filenameLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=4)
        mainSizer.Add(self.filesListCombo,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                      border=4)

        mainSizer.Add(commentLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=4)

        mainSizer.Add(self.commentText,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                      border=4)

        mainSizer.AddStretchSpacer()
        mainSizer.Add(okCancel,
                      flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                      border=4)

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()
