# -*- coding: utf-8 -*-

from os import stat_result
import os.path
from datetime import datetime

import wx

from outwiker.core.system import getImagesDir
from outwiker.gui.defines import BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
from outwiker.gui.images import readImage
from outwiker.gui.testeddialog import TestedDialog


class OverwriteDialog(TestedDialog):
    ID_OVERWRITE = 1
    ID_SKIP = 2

    def __init__(self, parent):
        super().__init__(parent)
        self._createControls()
        self._do_layout()

        self.SetTitle(_("File already exists"))
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

    def setVisibleOverwriteAllButton(self, visible: bool):
        self.overwriteAll.Show(visible)
        self.Layout()

    def setVisibleSkipButton(self, visible: bool):
        self.skip.Show(visible)
        self.Layout()

    def setVisibleSkipAllButton(self, visible: bool):
        self.skipAll.Show(visible)
        self.Layout()

    def _createControls(self):
        self._createButtons()
        self._createFileInfoPanels()

        fname_font = wx.Font(
            wx.FontInfo(
                wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetPointSize() + 2
            ).Bold()
        )
        self.textLabel = wx.StaticText(self, label="File name", style=wx.ALIGN_CENTRE)
        self.textLabel.SetFont(fname_font)
        arrowBmp = readImage(
            os.path.join(getImagesDir(), "arrow_right.svg"),
            BUTTON_ICON_WIDTH,
            BUTTON_ICON_HEIGHT,
        )
        self._arrow = wx.StaticBitmap(self, bitmap=arrowBmp)

    def _do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(1)

        information_sizer = wx.FlexGridSizer(cols=3)
        information_sizer.AddGrowableCol(0)
        information_sizer.AddGrowableCol(2)
        information_sizer.AddGrowableRow(0)

        information_sizer.Add(self.newFileBox, flag=wx.ALL | wx.EXPAND, border=4)

        information_sizer.Add(
            self._arrow, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4
        )

        information_sizer.Add(self.oldFileBox, flag=wx.ALL | wx.EXPAND, border=4)

        buttons_sizer = self._createButtonsSizer()

        main_sizer.Add(
            self.textLabel, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=4
        )

        main_sizer.Add(
            information_sizer,
            flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
            border=4,
        )

        main_sizer.Add(
            buttons_sizer,
            flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=4,
        )

        self.SetSizer(main_sizer)
        self.Fit()

    def _createFileInfoPanels(self):
        self.newFileBox = wx.StaticBoxSizer(wx.VERTICAL, self, _("New file"))
        self._newFileSizeLabel = wx.StaticText(self)
        self._newFileDateLabel = wx.StaticText(self)
        self.newFileBox.Add(self._newFileSizeLabel, flag=wx.ALL, border=4)
        self.newFileBox.Add(self._newFileDateLabel, flag=wx.ALL, border=4)

        self.oldFileBox = wx.StaticBoxSizer(wx.VERTICAL, self, _("Exiting file"))
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
        size_label = _("{size:_d} bytes").format(size=info.st_size).replace("_", " ")

        date = datetime.fromtimestamp(info.st_mtime)
        date_label = "{date:%c}".format(date=date)

        self._newFileSizeLabel.SetLabel(size_label)
        self._newFileDateLabel.SetLabel(date_label)

    def _setOldFileInfo(self, info: stat_result):
        size_label = _("{size:_d} bytes").format(size=info.st_size).replace("_", " ")

        date = datetime.fromtimestamp(info.st_mtime)
        date_label = "{date:%c}".format(date=date)

        self._oldFileSizeLabel.SetLabel(size_label)
        self._oldFileDateLabel.SetLabel(date_label)

    def ShowDialog(
        self, text: str, old_file_stat: stat_result, new_file_stat: stat_result
    ):
        """
        Показать диалог, если нужно спросить, что делать с файлом.
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
