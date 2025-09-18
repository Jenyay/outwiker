# -*- coding: utf-8 -*-

import wx

from outwiker.gui.guiconfig import TreeConfig
from outwiker.gui.defines import NOTES_TREE_MIN_FONT_SIZE, NOTES_TREE_MAX_FONT_SIZE
from outwiker.gui.preferences.configelements import BooleanElement
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class NotesTreePanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._config = TreeConfig(application.config)
        self._createGUI()

        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createFontSizeGUI(main_sizer)
        self._createExtraIconsGUI(main_sizer)
        self.SetSizer(main_sizer)

    def _createExtraIconsGUI(self, main_sizer):
        sizer = self._createSection(main_sizer, _("Extra icons"), cols=1)[1]
        self._extraIconBookmarksCheckBox = self._createCheckBox(
            _("Show bookmark icon"), sizer
        )
        self._extraIconReadonlyCheckBox = self._createCheckBox(
            _("Show read-only icon"), sizer
        )

    def _createFontSizeGUI(self, main_sizer):
        self._fontSizeSizer = wx.FlexGridSizer(cols=2)
        self._fontSizeSizer.AddGrowableCol(1)
        self._fontSizeComboBox = self._createLabelAndFontSize(
            _("Font size"),
            NOTES_TREE_MIN_FONT_SIZE,
            NOTES_TREE_MAX_FONT_SIZE,
            self._fontSizeSizer,
        )[1]
        main_sizer.Add(self._fontSizeSizer, flag=wx.EXPAND)

    def LoadState(self):
        """
        Load state from config
        """
        font_size = self._config.fontSize.value

        if (
            font_size is None
            or font_size < NOTES_TREE_MIN_FONT_SIZE
            or font_size > NOTES_TREE_MAX_FONT_SIZE
        ):
            self._fontSizeComboBox.SetSelection(0)
        else:
            index = 1 + font_size - NOTES_TREE_MIN_FONT_SIZE
            self._fontSizeComboBox.SetSelection(index)

        self.extraIconBookmark = BooleanElement(
            self._config.extraIconBookmark, self._extraIconBookmarksCheckBox
        )
        self.readOnlyIcon = BooleanElement(
            self._config.extraIconReadOnly, self._extraIconReadonlyCheckBox
        )

    def Save(self):
        """
        Save state to config
        """
        font_size_index = self._fontSizeComboBox.GetSelection()
        if font_size_index == 0:
            self._config.fontSize.value = None
        else:
            font_size = font_size_index - 1 + NOTES_TREE_MIN_FONT_SIZE
            self._config.fontSize.value = font_size

        self.extraIconBookmark.save()
        self.readOnlyIcon.save()
