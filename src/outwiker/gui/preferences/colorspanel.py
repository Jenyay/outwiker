# -*- coding: utf-8 -*-

from typing import Tuple

import wx

from . import configelements
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class ColorsPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self.mainWindowConfig = MainWindowConfig(application.config)
        self.tagsConfig = TagsConfig(application.config)
        self._createGUI()

        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createMainWindowColorsGUI(main_sizer)
        self._createTagsColorsGUI(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def _createMainWindowColorsGUI(self, main_sizer):
        parent, sizer = self._createSection(main_sizer, _('Main window'))

        # Panels background color
        self.panelsBackgroundColorPicker = self._createLabelAndColorPicker(
            _(u"Main panels background color"), sizer)[1]

        # Panels text color
        self.panelsTextColorPicker = self._createLabelAndColorPicker(
            _(u"Main panels text color"), sizer)[1]

    def _createTagsColorsGUI(self, main_sizer):
        parent, sizer = self._createSection(main_sizer, _('Tags cloud'))

        self.tagsFontNormalColorPicker = self._createLabelAndColorPicker(
            _(u'Tag color'), sizer)[1]

        self.tagsFontNormalHoverColorPicker = self._createLabelAndColorPicker(
            _(u'Hover tag color'), sizer)[1]

        self.tagsFontSelectedColorPicker = self._createLabelAndColorPicker(
            _(u'Marked tag color'), sizer)[1]

        self.tagsFontSelectedHoverColorPicker = self._createLabelAndColorPicker(
            _(u'Hover marked tag color'), sizer)[1]

        self.tagsBackSelectedColorPicker = self._createLabelAndColorPicker(
            _(u'Marked tag background color'), sizer)[1]

    def LoadState(self):
        # Main panels
        self.panelsBackgroundColor = configelements.ColourElement(
            self.mainWindowConfig.mainPanesBackgroundColor,
            self.panelsBackgroundColorPicker)

        self.panelsTextColor = configelements.ColourElement(
            self.mainWindowConfig.mainPanesTextColor,
            self.panelsTextColorPicker)

        # Tags
        self.tagsFontNormal = configelements.ColourElement(
            self.tagsConfig.colorFontNormal,
            self.tagsFontNormalColorPicker)

        self.tagsFontNormalHover = configelements.ColourElement(
            self.tagsConfig.colorFontNormalHover,
            self.tagsFontNormalHoverColorPicker)

        self.tagsFontSelected = configelements.ColourElement(
            self.tagsConfig.colorFontSelected,
            self.tagsFontSelectedColorPicker)

        self.tagsFontSelectedHover = configelements.ColourElement(
            self.tagsConfig.colorFontSelectedHover,
            self.tagsFontSelectedHoverColorPicker)

        self.tagsBackSelected = configelements.ColourElement(
            self.tagsConfig.colorBackSelected,
            self.tagsBackSelectedColorPicker)

    def Save(self):
        # Main panels
        self.panelsBackgroundColor.save()
        self.panelsTextColor.save()

        # Tags
        self.tagsFontNormal.save()
        self.tagsFontNormalHover.save()
        self.tagsFontSelected.save()
        self.tagsFontSelectedHover.save()
        self.tagsBackSelected.save()
