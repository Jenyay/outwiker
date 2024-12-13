# -*- coding: utf-8 -*-

import wx

from outwiker.gui.guiconfig import TreeConfig
from outwiker.gui.controls.treebook2 import BasePrefPanel


class NotesTreePanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._config = TreeConfig(application.config)
        self._min_font_size = 4
        self._max_font_size = 40
        self._createGUI()

        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createFontSizeGUI(main_sizer)
        self.SetSizer(main_sizer)

    def _createFontSizeGUI(self, main_sizer):
        self._fontSizeLabel = wx.StaticText(self, label=_("Font size"))

        font_size_items = [
            str(n) for n in range(self._min_font_size, self._max_font_size + 1)
        ]
        font_size_items.insert(0, _("Default size"))
        self._fontSizeComboBox = wx.ComboBox(
            self, choices=font_size_items, style=wx.CB_DROPDOWN | wx.CB_READONLY
        )
        self._fontSizeComboBox.SetMinSize((150, -1))

        self._fontSizeSizer = wx.FlexGridSizer(cols=2)
        self._fontSizeSizer.AddGrowableCol(1)
        self._fontSizeSizer.Add(
            self._fontSizeLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        self._fontSizeSizer.Add(
            self._fontSizeComboBox,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            border=2,
        )
        main_sizer.Add(self._fontSizeSizer, flag=wx.EXPAND)

    def LoadState(self):
        """
        Load state from config
        """
        font_size = self._config.fontSize.value
        if font_size is None or font_size < self._min_font_size or font_size > self._max_font_size:
            self._fontSizeComboBox.SetSelection(0)
        else:
            index = 1 + font_size - self._min_font_size
            self._fontSizeComboBox.SetSelection(index)

    def Save(self):
        """
        Save state to config
        """
        font_size_index = self._fontSizeComboBox.GetSelection()
        if font_size_index == 0:
            self._config.fontSize.value = None
        else:
            font_size = font_size_index - 1 + self._min_font_size
            self._config.fontSize.value = font_size
