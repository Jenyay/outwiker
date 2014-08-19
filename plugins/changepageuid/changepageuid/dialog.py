# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

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
        self._newUidText.SetFocus()
        self._newUidText.SetSelection (0, -1)

        self.Center(wx.CENTRE_ON_SCREEN)

        self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)


    def __onOk (self, event):
        result = u"" if self.uidValidator is None else self.uidValidator (self.uid)

        if len (result) == 0:
            self.EndModal (wx.ID_OK)
        else:
            MessageBox (result,
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)


    def _createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        self._questionLabel = wx.StaticText (self, label = _(u"Enter new page identifier"))

        newUidSizer = wx.FlexGridSizer (cols=2)
        newUidSizer.AddGrowableCol (1)

        protocolLabel = wx.StaticText (self, label = u"page://")
        self._newUidText = wx.TextCtrl (self)
        self._newUidText.SetMinSize ((320, -1))

        newUidSizer.Add (protocolLabel,
                         flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                         border = 2)

        newUidSizer.Add (self._newUidText,
                         flag = wx.ALL | wx.EXPAND,
                         border = 2)


        mainSizer.Add (self._questionLabel,
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
        newuid = self._newUidText.GetValue().strip()

        assert len (newuid) != 0
        return newuid


    @uid.setter
    def uid (self, value):
        self._newUidText.SetValue (value.strip())


    def setPageTitle (self, pageTitle):
        self._questionLabel.SetLabel (_(u'Enter new identifier for page "{}"').format (pageTitle))
        self.Fit()
