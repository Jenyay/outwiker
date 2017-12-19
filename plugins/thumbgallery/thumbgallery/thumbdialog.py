# -*- coding: UTF-8 -*-

import wx

from outwiker.core.attachment import Attachment
from outwiker.gui.preferences.configelements import IntegerElement

from .thumbconfig import ThumbConfig
from .utilites import isImage


class ThumbDialog (wx.Dialog):
    def __init__ (self, parent, page, lang, application):
        super (ThumbDialog, self).__init__ (parent,
                                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        global _
        _ = lang

        self._page = page
        self._config = ThumbConfig (application.config)


        self.SetTitle (_(u"Gallery"))

        self.Center(wx.BOTH)

        self.ALL_BUTTON = wx.NewId()
        self.CLEAR_BUTTON = wx.NewId()

        # Контролы для выбора количества столбцов
        self.columnsLabel = wx.StaticText (self, -1, _(u"Columns count (0 - without table)"))
        self.columns = wx.SpinCtrl (self, min=0, max=self._config.COLUMNS_COUNT_MAX)
        self.columns.SetMinSize ((150, -1))

        # Контролы для указания размера превьюшек
        self.thumbSizeLabel = wx.StaticText (self, -1, _(u"Thumbnails size (0 - default size)"))
        self.thumbSizeCtrl = wx.SpinCtrl (self, min=0, max=self._config.THUMB_SIZE_MAX)
        self.thumbSizeCtrl.SetMinSize ((150, -1))

        # Контролы для выбора прикрепленных файлов
        self.attachFiles = wx.CheckListBox (self)
        self.attachFiles.SetMinSize ((-1, 100))
        self.allFilesButton = wx.Button (self, self.ALL_BUTTON, _(u"All Images"))
        self.clearFilesButton = wx.Button (self, self.CLEAR_BUTTON, _(u"Clear"))

        self.Bind (wx.EVT_BUTTON, self._onAll, id=self.ALL_BUTTON)
        self.Bind (wx.EVT_BUTTON, self._onClear, id=self.CLEAR_BUTTON)
        self.Bind (wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

        self._fillAttaches()
        self.columns.SetFocus()

        # Используем золотое сечение
        dlgWidth = 500
        dlgHeight = int (500 / 1.61803399)
        self.SetMinSize ((dlgWidth, dlgHeight))

        self._layout ()
        self.LoadState()


    def _onAll (self, event):
        self.attachFiles.SetChecked (list(range(self.attachFiles.GetCount())))


    def _onClear (self, event):
        self.attachFiles.SetChecked ([])


    def _fillAttaches (self):
        attach = Attachment (self._page)
        allFiles = attach.getAttachRelative()
        imagesFiles = [fname for fname in allFiles if isImage (fname)]

        imagesFiles.sort(Attachment.sortByName)

        self.attachFiles.Clear()
        self.attachFiles.AppendItems (imagesFiles)


    def _getAttachSizer (self):
        buttonsSizer = wx.FlexGridSizer (1, 2, 0, 0)
        buttonsSizer.AddGrowableCol (0)
        buttonsSizer.AddGrowableCol (1)

        buttonsSizer.Add (self.allFilesButton,
                          flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
                          border = 2)

        buttonsSizer.Add (self.clearFilesButton,
                          flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
                          border = 2)


        attachSizer = wx.FlexGridSizer (cols=1)
        attachSizer.AddGrowableCol (0)
        attachSizer.AddGrowableRow (0)

        attachSizer.Add (self.attachFiles,
                         flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                         border = 2)

        attachSizer.Add (buttonsSizer,
                         flag = wx.EXPAND | wx.BOTTOM,
                         border = 2)

        return attachSizer


    def _getColumsSizer (self):
        # Строка для выбора количества столбцов
        columnsSizer = wx.FlexGridSizer (1, 2, 0, 0)
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
        thumbSizer = wx.FlexGridSizer (1, 2, 0, 0)
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
        attachSizer = self._getAttachSizer()

        self.mainSizer = wx.FlexGridSizer (0, 1, 0, 0)
        self.mainSizer.AddGrowableCol (0)
        self.mainSizer.AddGrowableRow (2)

        self.mainSizer.Add (columnsSizer, flag = wx.EXPAND | wx.ALL, border = 2)
        self.mainSizer.Add (thumbSizer, flag = wx.EXPAND | wx.ALL, border = 2)
        self.mainSizer.Add (attachSizer, flag = wx.EXPAND | wx.ALL, border = 2)

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


    @property
    def selectedFiles (self):
        """
        Список выбранных файлов
        """
        return self.attachFiles.GetCheckedStrings()


    @property
    def isAllFiles (self):
        """
        Вовзращает True, если выбраны все файлы и False в противном случае
        """
        return len (self.selectedFiles) == self.attachFiles.GetCount()


    def LoadState(self):
        self.columnsCountConfigElement = IntegerElement (self._config.columnsCount,
                                                         self.columns,
                                                         0,
                                                         self._config.COLUMNS_COUNT_MAX)

        self.thumbSizeConfigElement = IntegerElement (self._config.thumbSize,
                                                      self.thumbSizeCtrl,
                                                      0,
                                                      self._config.THUMB_SIZE_MAX)


    def Save (self):
        self.columnsCountConfigElement.save()
        self.thumbSizeConfigElement.save()


    def onOk (self, event):
        self.Save()
        event.Skip()
