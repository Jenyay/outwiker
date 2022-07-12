# -*- coding: utf-8 -*-

from pathlib import Path

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.attachfilters import getNotHiddenImageRecursiveFilter
from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox
from outwiker.gui.testeddialog import TestedDialog


class ThumbDialog(TestedDialog):
    WIDTH = 0
    HEIGHT = 1
    MAX_SIZE = 2

    def __init__(self, parent, page, selected_file):
        """
        parent - родительское окно
        page - current page
        selected_file - файл выбранный по умолчанию. Если selectedFile == None,
            никакой файл по умолчанию не выбирается
        """
        super().__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            title=_("Thumbnails"),
        )
        self._selected_file = selected_file

        attach = Attachment(page)
        self._root_dir = Path(attach.getAttachPath(create=False))
        self._filter = getNotHiddenImageRecursiveFilter(page)

        self._createGui()
        self.filesListCombo.SetFocus()
        self.Center(wx.BOTH)

    @property
    def fileName(self):
        return self.filesListCombo.GetValue()

    @property
    def scaleType(self):
        return self.scaleCombo.GetSelection()

    @property
    def size(self):
        return self.sizeCtrl.GetValue()

    def _createGui(self):
        # "Select attached image" label
        self.filenameLabel = wx.StaticText(self,
                                           label=_("Select attached image"))
        font = self.filenameLabel.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.filenameLabel.SetFont(font)

        # Files combobox
        self.filesListCombo = FilesTreeComboBox(self)
        self.filesListCombo.SetFilterFunc(self._filter)
        if self._root_dir.exists():
            self.filesListCombo.SetRootDir(self._root_dir)

            if self._selected_file:
                self.filesListCombo.SetValue(self._selected_file)

        # Controls for thumbnail size selection
        self.scaleLabel = wx.StaticText(self, label=_("Thumbnail size"))

        scaleItems = [_("Width"), _("Height"), _("Max size")]
        self.scaleCombo = wx.ComboBox(self,
                                      choices=scaleItems,
                                      style=wx.CB_READONLY)
        self.scaleCombo.SetSelection(0)
        self.scaleCombo.SetMinSize((250, -1))

        self.sizeCtrl = wx.SpinCtrl(self, min=0, max=10000, initial=0)
        self.sizeCtrl.SetMinSize((100, -1))
        self.sizeLabel = wx.StaticText(self, label=_("0 - default size"))

        self.okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self._layout()

    def _layout(self):
        # Layout controls
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(5)

        mainSizer.Add(self.filenameLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add(
            self.filesListCombo,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=4,
        )

        mainSizer.Add(self.scaleLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)

        # Scale controls
        scaleSizer = wx.FlexGridSizer(cols=2)
        scaleSizer.AddGrowableCol(0)
        scaleSizer.AddGrowableCol(1)

        scaleSizer.Add(
            self.scaleCombo,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=4,
        )
        scaleSizer.Add(self.sizeCtrl, flag=wx.ALL | wx.EXPAND, border=4)
        mainSizer.Add(scaleSizer, flag=wx.ALL | wx.EXPAND, border=2)

        mainSizer.Add(self.sizeLabel, flag=wx.ALL | wx.ALIGN_RIGHT, border=4)

        mainSizer.Add(
            self.okCancel, flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=4
        )

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()
