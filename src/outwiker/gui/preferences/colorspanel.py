# -*- coding: utf-8 -*-

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

    def _createSection(self, main_sizer, title):
        staticBox = wx.StaticBox(self, label=title)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)

        colorsSizer = wx.FlexGridSizer(cols=2)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        staticBoxSizer.Add(colorsSizer, flag=wx.EXPAND)
        main_sizer.Add(staticBoxSizer, flag=wx.EXPAND | wx.ALL, border=2)
        return (staticBox, colorsSizer)

    def _createMainWindowColorsGUI(self, main_sizer):
        parent, sizer = self._createSection(main_sizer, _('Main window'))

        # Panels background color
        panelsBackgroundColorLabel, self.panelsBackgroundColorPicker = self._createLabelAndColorPicker(
            _(u"Main panels background color"), sizer
        )

        # Panels text color
        panelsTextColorLabel, self.panelsTextColorPicker = self._createLabelAndColorPicker(
            _(u"Main panels text color"), sizer
        )

    def _createTagsColorsGUI(self, main_sizer):
        parent, sizer = self._createSection(main_sizer, _('Tags'))

        colorFontNormalLabel, self.colorFontNormalPicker = self._createLabelAndColorPicker(
            _(u'Tag color'), sizer)

        colorFontNormalHoverLabel, self.colorFontNormalHoverPicker = self._createLabelAndColorPicker(
            _(u'Hover tag color'), sizer)

        colorFontSelectedLabel, self.colorFontSelectedPicker = self._createLabelAndColorPicker(
            _(u'Marked tag color'), sizer)

        colorFontSelectedHoverLabel, self.colorFontSelectedHoverPicker = self._createLabelAndColorPicker(
            _(u'Hover marked tag color'), sizer)

        colorBackSelectedLabel, self.colorBackSelectedPicker = self._createLabelAndColorPicker(
            _(u'Marked tag background color'), sizer)

    def _addControlsPairToSizer(self, sizer, label, control):
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

    def _createLabelAndColorPicker(self, text, sizer):
        label = wx.StaticText(self, label=text)
        colorPicker = wx.ColourPickerCtrl(self)
        self._addControlsPairToSizer(sizer, label, colorPicker)
        return (label, colorPicker)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
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
            self.colorFontNormalPicker)

        self.tagsFontNormalHover = configelements.ColourElement(
            self.tagsConfig.colorFontNormalHover,
            self.colorFontNormalHoverPicker)

        self.tagsFontSelected = configelements.ColourElement(
            self.tagsConfig.colorFontSelected,
            self.colorFontSelectedPicker)

        self.tagsFontSelectedHover = configelements.ColourElement(
            self.tagsConfig.colorFontSelectedHover,
            self.colorFontSelectedHoverPicker)

        self.tagsBackSelected = configelements.ColourElement(
            self.tagsConfig.colorBackSelected,
            self.colorBackSelectedPicker)

    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        # Main panels
        self.panelsBackgroundColor.save()
        self.panelsTextColor.save()

        # Tags
        self.tagsFontNormal.save()
        self.tagsFontNormalHover.save()
        self.tagsFontSelected.save()
        self.tagsFontSelectedHover.save()
        self.tagsBackSelected.save()
