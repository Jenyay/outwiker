# -*- coding: utf-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class OverwriteDialog(TestedDialog):
    def __init__(self, *args, **kwds):
        super(OverwriteDialog, self).__init__(*args, **kwds)
        self.textLabel = wx.StaticText(self,
                                       -1,
                                       _("Overwrite file?"),
                                       style=wx.ALIGN_CENTRE)
        self.overwrite = wx.Button(self, -1, _("Overwrite"))
        self.overwriteAll = wx.Button(self, -1, _("Overwrite all"))
        self.skip = wx.Button(self, -1, _("Skip"))
        self.skipAll = wx.Button(self, -1, _("Skip all"))
        self.cancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onOverwrite, self.overwrite)
        self.Bind(wx.EVT_BUTTON, self.onOverwriteAll, self.overwriteAll)
        self.Bind(wx.EVT_BUTTON, self.onSkip, self.skip)
        self.Bind(wx.EVT_BUTTON, self.onSkipAll, self.skipAll)

        self.ID_OVERWRITE = 1
        self.ID_SKIP = 2

        # Флаг, который сохраняет выбор пользователя,
        # чтобы не показывать диалог после выбора "... all"
        self.flag = 0

        self.SetEscapeId(wx.ID_CANCEL)
        self.Center(wx.BOTH)

    def __set_properties(self):
        self.SetTitle(_("Overwrite Files"))
        self.overwrite.SetFocus()
        self.overwrite.SetDefault()

    def __do_layout(self):
        sizer_1 = wx.FlexGridSizer(cols=1)
        sizer_1.AddGrowableCol(0)
        sizer_1.AddGrowableRow(1)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(self.textLabel,
                    flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
                    border=10)

        sizer_2.Add(self.overwrite, flag=wx.ALL, border=4)
        sizer_2.Add(self.overwriteAll, flag=wx.ALL, border=4)
        sizer_2.Add(self.skip, flag=wx.ALL, border=4)
        sizer_2.Add(self.skipAll, flag=wx.ALL, border=4)
        sizer_2.Add(self.cancel, flag=wx.ALL, border=4)

        sizer_1.Add(sizer_2,
                    flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                    border=4)

        self.SetSizer(sizer_1)
        self.Fit()

    def ShowDialog(self, text):
        """
        Показать диалог, если нужно спросить, что делать с файлов.
        Этот метод вызывается вместо Show/ShowModal.
        text - текст для сообщения в диалоге
        """
        if self.flag == 0:
            self.textLabel.SetLabel(text)
            self.Layout()
            return self.ShowModal()

        return self.flag

    def onOverwrite(self, event):
        self.EndModal(self.ID_OVERWRITE)

    def onOverwriteAll(self, event):
        self.flag = self.ID_OVERWRITE
        self.EndModal(self.ID_OVERWRITE)

    def onSkip(self, event):
        self.EndModal(self.ID_SKIP)

    def onSkipAll(self, event):
        self.flag = self.ID_SKIP
        self.EndModal(self.ID_SKIP)
