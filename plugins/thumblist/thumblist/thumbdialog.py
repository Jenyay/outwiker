#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx


class ThumbDialog (wx.Dialog):
    def __init__ (self, parent):
        super (ThumbDialog, self).__init__ (parent, 
                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self.Center(wx.CENTRE_ON_SCREEN)

        self._maxColumns = 100
        self._maxThumbSize = 10000

        # Контролы для выбора количества столбцов
        self.columnsLabel = wx.StaticText (self, -1, _(u"Columns count (0 - without table)") )
        self.columns = wx.SpinCtrl (self, min=0, max=self._maxColumns)
        self.columns.SetMinSize ((150, -1))

        # Контролы для указания размера превьюшек
        self.thumbSizeLabel = wx.StaticText (self, -1, _(u"Thumbnails size (0 - default size)") )
        self.thumbSizeCtrl = wx.SpinCtrl (self, min=0, max=self._maxThumbSize)
        self.thumbSizeCtrl.SetMinSize ((150, -1))

        self.columns.SetFocus()

        self._layout ()


    def _getColumsSizer (self):
        # Строка для выбора количества столбцов
        columnsSizer = wx.FlexGridSizer (1, 2)
        columnsSizer.AddGrowableCol (0)
        columnsSizer.AddGrowableCol (1)

        columnsSizer.Add (self.columnsLabel, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx. ALIGN_LEFT | wx.ALL,
                border = 2)

        columnsSizer.Add (self.columns, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL,
                border = 2)

        return columnsSizer


    def _getThumbSizeSizer (self):
        # Строка для выбора размера превьюшек
        thumbSizer = wx.FlexGridSizer (1, 2)
        thumbSizer.AddGrowableCol (0)
        thumbSizer.AddGrowableCol (1)

        thumbSizer.Add (self.thumbSizeLabel, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx. ALIGN_LEFT | wx.ALL,
                border = 2)

        thumbSizer.Add (self.thumbSizeCtrl, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL,
                border = 2)

        return thumbSizer


    def _layout (self):
        columnsSizer = self._getColumsSizer ()
        thumbSizer = self._getThumbSizeSizer()

        self.mainSizer = wx.FlexGridSizer (0, 1)
        self.mainSizer.AddGrowableCol (0)
        self.mainSizer.AddGrowableRow (2)
        self.mainSizer.Add (columnsSizer, flag = wx.EXPAND | wx.ALL, border = 2)
        self.mainSizer.Add (thumbSizer, flag = wx.EXPAND | wx.ALL, border = 2)

        self._createOkCancelButtons (self.mainSizer)
        self.SetSizer (self.mainSizer)
        self.Layout()
        self.Fit()


    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.Add (buttonsSizer, flag = wx.ALIGN_RIGHT | wx.ALL | wx.ALIGN_BOTTOM, border = 2)


    @property
    def columnsCount (self):
        """
        Количество столбцов. 0 - не использовать таблицу
        """
        return self.columns.GetValue()


    @property
    def thumbSize (self):
        """
        Размер превьюшек в галерее
        """
        return self.thumbSizeCtrl.GetValue()
