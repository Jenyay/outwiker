# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class LinkDialog (TestedDialog):
    """
    Диалог для создания ссылок
    """
    def __init__ (self, parent):
        """
        link - Ссылка по умолчанию
        comment - Комментарий к ссылке по умолчанию
        """
        super (LinkDialog, self).__init__ (parent,
                                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                                           title=_("Link"))

        self.textWidth = 300

        self._createGui ()
        self.linkText.SetFocus()
        self.Center(wx.CENTRE_ON_SCREEN)


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (rows=0, cols=2)
        mainSizer.AddGrowableCol (1)
        mainSizer.AddGrowableRow (2)

        linkLabel = wx.StaticText (self, label=_(u"Link"))
        self.linkText = wx.ComboBox (self, style=wx.CB_DROPDOWN)
        self.linkText.SetMinSize ((self.textWidth, -1))
        mainSizer.Add (linkLabel, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add (self.linkText, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)

        commentLabel = wx.StaticText (self, label=_(u"Comment"))
        self.commentText = wx.TextCtrl (self)
        self.commentText.SetMinSize ((self.textWidth, -1))
        mainSizer.Add (commentLabel, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add (self.commentText, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)

        self.__okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (self.__okCancel, 0, flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=4)

        self.SetSizer (mainSizer)
        self.Fit()
        self.Layout()


    @property
    def comment (self):
        return self.commentText.GetValue()


    @comment.setter
    def comment (self, value):
        self.commentText.SetValue (value)


    @property
    def link (self):
        return self.linkText.GetValue()


    @link.setter
    def link (self, value):
        self.linkText.SetValue (value)
