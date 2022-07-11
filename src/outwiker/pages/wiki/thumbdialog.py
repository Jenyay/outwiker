# -*- coding: utf-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class ThumbDialog(TestedDialog):
    WIDTH = 0
    HEIGHT = 1
    MAX_SIZE = 2

    def __init__(self, parent, filesList, selectedFile):
        """
        parent - родительское окно
        filesList - список файлов, отображаемых в диалоге
        selectedFile - файл выбранный по умолчанию. Если selectedFile == None,
            никакой файл по умолчанию не выбирается
        """
        super().__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            title=_("Thumbnails"),
        )

        self.__filesList = filesList
        self.__selectedFile = selectedFile

        self.__createGui()
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

    def __createGui(self):
        # Controls for file name selection
        filenameLabel = wx.StaticText(self, label=_("Select attached image"))
        font = filenameLabel.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        filenameLabel.SetFont(font)

        self.filesListCombo = wx.ComboBox(
            self, choices=self.__filesList, style=wx.CB_READONLY
        )
        self.filesListCombo.SetSelection(0)
        self.filesListCombo.SetMinSize((250, -1))

        if self.__selectedFile:
            assert self.__selectedFile in self.__filesList
            self.filesListCombo.SetStringSelection(self.__selectedFile)

        # Controls for thumbnail size selection
        scaleLabel = wx.StaticText(self, label=_("Thumbnail size"))

        scaleItems = [_("Width"), _("Height"), _("Max size")]
        self.scaleCombo = wx.ComboBox(self, choices=scaleItems, style=wx.CB_READONLY)
        self.scaleCombo.SetSelection(0)
        self.scaleCombo.SetMinSize((250, -1))

        self.sizeCtrl = wx.SpinCtrl(self, min=0, max=10000, initial=0)
        self.sizeCtrl.SetMinSize((100, -1))
        sizeLabel = wx.StaticText(self, label=_("0 - default size"))

        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        # Layout controls
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(5)

        mainSizer.Add(filenameLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add(
            self.filesListCombo,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=4,
        )

        mainSizer.Add(scaleLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)

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

        mainSizer.Add(sizeLabel, flag=wx.ALL | wx.ALIGN_RIGHT, border=4)

        mainSizer.Add(
            okCancel, flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=4
        )

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()
