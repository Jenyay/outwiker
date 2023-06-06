# -*- coding: utf-8 -*-

from os import path
from pathlib import Path
from typing import List

import wx

from outwiker.api.core.attachment import (
    Attachment,
    getImagesOnlyFilter,
    getHiddenFilter,
    getDirOnlyFilter,
    andFilter,
    orFilter,
    notFilter,
)
from outwiker.api.gui.configelements import IntegerElement
from outwiker.api.gui.controls import FilesTreeCtrl

from .thumbconfig import ThumbConfig
from .i18n import get_


class ThumbDialog(wx.Dialog):
    def __init__(self, parent, page, application):
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        global _
        _ = get_()

        self._page = page
        self._config = ThumbConfig(application.config)

        self.SetTitle(_("Gallery"))

        self.Center(wx.BOTH)

        # Контролы для выбора количества столбцов
        self.columnsLabel = wx.StaticText(
            self, -1, _("Columns count (0 - without table)")
        )
        self.columns = wx.SpinCtrl(self, min=0, max=self._config.COLUMNS_COUNT_MAX)
        self.columns.SetMinSize((150, -1))

        # Контролы для указания размера превьюшек
        self.thumbSizeLabel = wx.StaticText(
            self, -1, _("Thumbnails size (0 - default size)")
        )
        self.thumbSizeCtrl = wx.SpinCtrl(self, min=0, max=self._config.THUMB_SIZE_MAX)
        self.thumbSizeCtrl.SetMinSize((150, -1))

        # Контролы для выбора прикрепленных файлов
        self.attachFiles = FilesTreeCtrl(self, check_boxes=True)

        files_filter = andFilter(
            orFilter(getImagesOnlyFilter(), getDirOnlyFilter()),
            notFilter(getHiddenFilter(self._page)),
        )
        self.attachFiles.SetFilterFunc(files_filter)

        self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

        self._fillAttaches()
        self.columns.SetFocus()

        dlgWidth = 500
        dlgHeight = 450
        self.SetMinSize((dlgWidth, dlgHeight))

        self._layout()
        self.LoadState()

    def _fillAttaches(self):
        attach = Attachment(self._page)
        root_dir = attach.getAttachPath(create=False)
        if path.exists(root_dir):
            self.attachFiles.SetRootDir(root_dir)

    def _getAttachSizer(self):
        buttonsSizer = wx.FlexGridSizer(1, 2, 0, 0)
        buttonsSizer.AddGrowableCol(0)
        buttonsSizer.AddGrowableCol(1)

        attachSizer = wx.FlexGridSizer(cols=1)
        attachSizer.AddGrowableCol(0)
        attachSizer.AddGrowableRow(0)

        attachSizer.Add(
            self.attachFiles, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2
        )

        attachSizer.Add(buttonsSizer, flag=wx.EXPAND | wx.BOTTOM, border=2)

        return attachSizer

    def _getColumsSizer(self):
        # Строка для выбора количества столбцов
        columnsSizer = wx.FlexGridSizer(1, 2, 0, 0)
        columnsSizer.AddGrowableCol(0)
        columnsSizer.AddGrowableCol(1)

        columnsSizer.Add(
            self.columnsLabel,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL,
            border=2,
        )

        columnsSizer.Add(
            self.columns,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL,
            border=2,
        )

        return columnsSizer

    def _getThumbSizeSizer(self):
        # Строка для выбора размера превьюшек
        thumbSizer = wx.FlexGridSizer(1, 2, 0, 0)
        thumbSizer.AddGrowableCol(0)
        thumbSizer.AddGrowableCol(1)

        thumbSizer.Add(
            self.thumbSizeLabel,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL,
            border=2,
        )

        thumbSizer.Add(
            self.thumbSizeCtrl,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL,
            border=2,
        )

        return thumbSizer

    def _layout(self):
        columnsSizer = self._getColumsSizer()
        thumbSizer = self._getThumbSizeSizer()
        attachSizer = self._getAttachSizer()

        self.mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        self.mainSizer.AddGrowableCol(0)
        self.mainSizer.AddGrowableRow(0)

        self.mainSizer.Add(attachSizer, flag=wx.EXPAND | wx.ALL, border=2)
        self.mainSizer.Add(columnsSizer, flag=wx.EXPAND | wx.ALL, border=2)
        self.mainSizer.Add(thumbSizer, flag=wx.EXPAND | wx.ALL, border=2)

        self._createOkCancelButtons(self.mainSizer)
        self.SetSizer(self.mainSizer)
        self.Layout()
        self.Fit()

    def _createOkCancelButtons(self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(
            buttonsSizer, flag=wx.ALIGN_RIGHT | wx.ALL | wx.ALIGN_BOTTOM, border=2
        )

    @property
    def columnsCount(self) -> int:
        """
        Количество столбцов. 0 - не использовать таблицу
        """
        return self.columns.GetValue()

    @property
    def thumbSize(self) -> int:
        """
        Размер превьюшек в галерее
        """
        return self.thumbSizeCtrl.GetValue()

    @property
    def selectedFiles(self) -> List[Path]:
        """
        Список выбранных файлов
        """
        return [fname for fname in self.attachFiles.GetChecked() if not fname.is_dir()]

    def LoadState(self):
        self.columnsCountConfigElement = IntegerElement(
            self._config.columnsCount, self.columns, 0, self._config.COLUMNS_COUNT_MAX
        )

        self.thumbSizeConfigElement = IntegerElement(
            self._config.thumbSize, self.thumbSizeCtrl, 0, self._config.THUMB_SIZE_MAX
        )

    def Save(self):
        self.columnsCountConfigElement.save()
        self.thumbSizeConfigElement.save()

    def onOk(self, event):
        self.Save()
        event.Skip()
