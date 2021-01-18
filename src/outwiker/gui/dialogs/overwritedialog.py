# -*- coding: utf-8 -*-

from os import stat_result
import os.path
from datetime import datetime

import wx

from outwiker.core.system import getImagesDir
from outwiker.gui.testeddialog import TestedDialog


class OverwriteDialog(TestedDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self._createControls()
        self._do_layout()

        self.ID_OVERWRITE = 1
        self.ID_SKIP = 2

        self.SetTitle(_("Overwrite Files"))
        self.overwrite.SetFocus()
        self.overwrite.SetDefault()

        # Флаг, который сохраняет выбор пользователя,
        # чтобы не показывать диалог после выбора "... all"
        self.flag = 0

        self.Bind(wx.EVT_BUTTON, self.onOverwrite, self.overwrite)
        self.Bind(wx.EVT_BUTTON, self.onOverwriteAll, self.overwriteAll)
        self.Bind(wx.EVT_BUTTON, self.onSkip, self.skip)
        self.Bind(wx.EVT_BUTTON, self.onSkipAll, self.skipAll)

        self.SetEscapeId(wx.ID_CANCEL)
        self.Center(wx.BOTH)

    def _createControls(self):
        self._createButtons()
        self._createFileInfoPanels()
        self.textLabel = wx.StaticText(self,
                                       label=_("Overwrite file?"),
                                       style=wx.ALIGN_CENTRE)
        downArrowBmp = wx.Image(os.path.join(
            getImagesDir(), 'arrow_down.png')).ConvertToBitmap()
        self._downArrow = wx.StaticBitmap(self, bitmap=downArrowBmp)

    def _do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(1)

        buttons_sizer = self._createButtonsSizer()

        main_sizer.Add(self.textLabel,
                       flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
                       border=4)

        main_sizer.Add(self.newFileBox,
                       flag=wx.ALL | wx.EXPAND,
                       border=4)

        main_sizer.Add(self._downArrow,
                       flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
                       border=4)

        main_sizer.Add(self.oldFileBox,
                       flag=wx.ALL | wx.EXPAND,
                       border=4)

        main_sizer.Add(buttons_sizer,
                       flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                       border=4)

        self.SetSizer(main_sizer)
        self.Fit()

    def _createFileInfoPanels(self):
        self.newFileBox = wx.StaticBoxSizer(wx.VERTICAL,
                                            self,
                                            _("New file"))
        self._newFileSizeLabel = wx.StaticText(self)
        self._newFileDateLabel = wx.StaticText(self)
        self.newFileBox.Add(self._newFileSizeLabel, flag=wx.ALL, border=4)
        self.newFileBox.Add(self._newFileDateLabel, flag=wx.ALL, border=4)

        self.oldFileBox = wx.StaticBoxSizer(wx.VERTICAL,
                                            self,
                                            _("Exiting file"))
        self._oldFileSizeLabel = wx.StaticText(self)
        self._oldFileDateLabel = wx.StaticText(self)

        self.oldFileBox.Add(self._oldFileSizeLabel, flag=wx.ALL, border=4)
        self.oldFileBox.Add(self._oldFileDateLabel, flag=wx.ALL, border=4)

    def _createButtons(self):
        self.overwrite = wx.Button(self, label=_("Overwrite"))
        self.overwriteAll = wx.Button(self, label=_("Overwrite all"))
        self.skip = wx.Button(self, label=_("Skip"))
        self.skipAll = wx.Button(self, label=_("Skip all"))
        self.cancel = wx.Button(self, id=wx.ID_CANCEL, label=_("Cancel"))

    def _createButtonsSizer(self):
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.overwrite, flag=wx.ALL, border=4)
        buttons_sizer.Add(self.overwriteAll, flag=wx.ALL, border=4)
        buttons_sizer.Add(self.skip, flag=wx.ALL, border=4)
        buttons_sizer.Add(self.skipAll, flag=wx.ALL, border=4)
        buttons_sizer.Add(self.cancel, flag=wx.ALL, border=4)
        return buttons_sizer

    def _setNewFileInfo(self, info: stat_result):
        size_label = _('New file size: {size:_d} bites').format(
            size=info.st_size).replace('_', ' ')

        date = datetime.fromtimestamp(info.st_mtime)
        date_label = _("New file date: {date:%c}").format(date=date)

        self._newFileSizeLabel.SetLabel(size_label)
        self._newFileDateLabel.SetLabel(date_label)

    def _setOldFileInfo(self, info: stat_result):
        size_label = _('Exiting file size: {size:_d} bites').format(
            size=info.st_size).replace('_', ' ')

        date = datetime.fromtimestamp(info.st_mtime)
        date_label = _("Exiting file date: {date:%c}").format(date=date)

        self._oldFileSizeLabel.SetLabel(size_label)
        self._oldFileDateLabel.SetLabel(date_label)

    def ShowDialog(self,
                   text: str,
                   old_file_stat: stat_result,
                   new_file_stat: stat_result):
        """
        Показать диалог, если нужно спросить, что делать с файлов.
        Этот метод вызывается вместо Show/ShowModal.
        text - текст для сообщения в диалоге
        """
        if self.flag == 0:
            self.textLabel.SetLabel(text)
            self._setNewFileInfo(new_file_stat)
            self._setOldFileInfo(old_file_stat)
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
