# -*- coding: UTF-8 -*-

import wx

from outwiker.core.system import getOS

from .i18n import get_


class UpdateDialog(wx.Dialog):
    """Dialog to show new versions of hte OutWiekr and plugins"""

    def __init__(self, parent):
        super(UpdateDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        global _
        _ = get_()
        self.SetSize((750, 500))
        self.SetTitle(_(u"UpdateNotifier"))
        self._createGui()

    def setContent(self, HTMLContent, basepath):
        self._htmlRender.SetPage(HTMLContent, basepath)

    def _createGui(self):
        """
        Создание элементов управления в дилалоге
        """
        self._mainSizer = wx.FlexGridSizer(cols=1)
        self._mainSizer.AddGrowableCol(0)
        self._mainSizer.AddGrowableRow(0)

        self._htmlRender = getOS().getHtmlRender(self)
        self._mainSizer.Add(self._htmlRender,
                            1,
                            wx.EXPAND | wx.ALL,
                            border=2)

        buttonsSizer = self.CreateButtonSizer(wx.OK)
        self._mainSizer.Add(buttonsSizer,
                            1,
                            wx.ALIGN_RIGHT | wx.ALL,
                            border=2)

        self.SetSizer(self._mainSizer)
        self.Layout()
