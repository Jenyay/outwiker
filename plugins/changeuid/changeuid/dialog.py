# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog

from .i18n import get_


class ChangeUidDialog (TestedDialog):
    """
    Диалог ввода нового UID
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (ChangeUidDialog, self).__init__ (parent,
                                                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
                                                title=u"ChangeUID")

        # Функция для проверки правильности введенного идентификатора
        self.uidValidator = None

        self._createGui()
        self.newUidText.SetFocus()
        self.newUidText.SetSelection (0, -1)

        self.Center(wx.CENTRE_ON_SCREEN)


    def _createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        questionLabel = wx.StaticText (self, label = _(u"Enter new page identifier"))

        newUidSizer = wx.FlexGridSizer (cols=2)
        newUidSizer.AddGrowableCol (1)

        protocolLabel = wx.StaticText (self, label = u"page://")
        self.newUidText = wx.TextCtrl (self)
        self.newUidText.SetMinSize ((320, -1))

        newUidSizer.Add (protocolLabel,
                         flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                         border = 2)

        newUidSizer.Add (self.newUidText,
                         flag = wx.ALL | wx.EXPAND,
                         border = 2)


        mainSizer.Add (questionLabel,
                       flag = wx.ALL,
                       border = 2)

        mainSizer.Add (newUidSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)

        self._createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self.Fit()


    def _createOkCancelButtons (self, mainSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (
            okCancel,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
            border=4
        )


    @property
    def uid (self):
        newuid = self.newUidText.GetValue().strip()

        assert len (newuid) != 0
        return newuid


    @uid.setter
    def uid (self, value):
        self.newUidText.SetValue (value.strip())
