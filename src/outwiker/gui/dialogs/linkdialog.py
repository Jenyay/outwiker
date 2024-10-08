# -*- coding: utf-8 -*-

import wx

from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox
from outwiker.gui.testeddialog import TestedDialog


class LinkDialog(TestedDialog):
    """
    Dialog to inserting a link.
    User may enter link and comment.
    """

    def __init__(self, parent):
        """
        parent - parent window
        """
        super().__init__(
            parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, title=_("Link")
        )

        self.textWidth = 300

        self._createGui()
        self.linkText.SetFocus()
        self.Center(wx.BOTH)

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(2)

        # Link
        linkLabel = wx.StaticText(self, label=_("Link"))
        self.linkText = FilesTreeComboBox(self)
        self.linkText.SetMinSize((self.textWidth, -1))

        mainSizer.Add(linkLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add(
            self.linkText, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4
        )

        # Comment
        commentLabel = wx.StaticText(self, label=_("Comment"))
        self.commentText = wx.TextCtrl(self)
        self.commentText.SetMinSize((self.textWidth, -1))

        mainSizer.Add(commentLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add(
            self.commentText,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=4,
        )

        # Ok / Cancel buttons
        self.__okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(
            self.__okCancel, flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=4
        )

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()

    @property
    def comment(self):
        return self.commentText.GetValue()

    @comment.setter
    def comment(self, value):
        self.commentText.SetValue(value)

    @property
    def link(self):
        return self.linkText.GetValue()

    @link.setter
    def link(self, value):
        self.linkText.SetValue(value)
