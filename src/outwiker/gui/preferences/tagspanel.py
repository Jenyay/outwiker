# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class TagsPanel(BasePrefPanel):
    def __init__(self, parent):
        super (type (self), self).__init__ (parent)

        self.ACTIONS_COMBOBOX_WIDTH = 300

        self._actions = [
            (_(u'Search pages with the tag'), TagsConfig.ACTION_SHOW_LIST),
            (_(u'Toggle tag selection'), TagsConfig.ACTION_MARK_TOGGLE),
        ]

        self._config = TagsConfig (Application.config)
        self._createGui()
        self._setScrolling()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        self._createColorsGui (mainSizer)
        self._createActionsGui (mainSizer)

        self.SetSizer (mainSizer)


    def _addControlsPairToSizer (self, sizer, label, control):
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)


    def _createLabelAndColorPicker (self, text, sizer):
        label = wx.StaticText (
            self,
            label = text)

        colorPicker = wx.ColourPickerCtrl(
            self,
            style=wx.CLRP_SHOW_LABEL)

        self._addControlsPairToSizer (sizer, label, colorPicker)

        return (label, colorPicker)


    def _createColorsGui (self, mainsizer):
        colorsSizer = wx.FlexGridSizer(cols=2)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        colorFontNormalLabel, self.colorFontNormalPicker = self._createLabelAndColorPicker (_(u'Tag color'), colorsSizer)

        colorFontNormalHoverLabel, self.colorFontNormalHoverPicker = self._createLabelAndColorPicker (_(u'Hover tag color'), colorsSizer)

        colorFontSelectedLabel, self.colorFontSelectedPicker = self._createLabelAndColorPicker (_(u'Marked tag color'), colorsSizer)

        colorFontSelectedHoverLabel, self.colorFontSelectedHoverPicker = self._createLabelAndColorPicker (_(u'Hover marked tag color'), colorsSizer)

        colorBackSelectedLabel, self.colorBackSelectedPicker = self._createLabelAndColorPicker (_(u'Marked tag background color'), colorsSizer)

        mainsizer.Add (colorsSizer, 0, wx.EXPAND | wx.ALL, border = 2)


    def _createLabelAndComboBox (self, text, sizer):
        label = wx.StaticText (self, label = text)

        combobox = wx.ComboBox (self,
                                -1,
                                style=wx.CB_DROPDOWN | wx.CB_READONLY)

        combobox.SetMinSize((self.ACTIONS_COMBOBOX_WIDTH, -1))

        self._addControlsPairToSizer (sizer, label, combobox)

        return (label, combobox)


    def _createActionsGui (self, mainsizer):
        actionsSizer = wx.FlexGridSizer(cols=2)
        actionsSizer.AddGrowableCol(0)

        leftClickActionLabel, self.leftClickActionCombo = self._createLabelAndComboBox (_(u'Left click on the tag'), actionsSizer)
        middleClickActionLabel, self.middleClickActionCombo = self._createLabelAndComboBox (_(u'Middle click on the tag'), actionsSizer)

        mainsizer.Add (actionsSizer, 0, wx.EXPAND | wx.ALL, border = 2)


    def _fillActionsCombos (self):
        for action in self._actions:
            self.leftClickActionCombo.Append (action[0])
            self.middleClickActionCombo.Append (action[0])

        self.leftClickActionCombo.SetSelection (0)
        self.middleClickActionCombo.SetSelection (0)

        for n, action in enumerate (self._actions):
            if action[1] == self._config.leftClickAction.value:
                self.leftClickActionCombo.SetSelection (n)

            if action[1] == self._config.middleClickAction.value:
                self.middleClickActionCombo.SetSelection (n)


    def LoadState(self):
        self._fillActionsCombos()

        self.colorFontNormalPicker.SetColour (self._config.colorFontNormal.value)
        self.colorFontNormalHoverPicker.SetColour (self._config.colorFontNormalHover.value)

        self.colorFontSelectedPicker.SetColour (self._config.colorFontSelected.value)
        self.colorFontSelectedHoverPicker.SetColour (self._config.colorFontSelectedHover.value)

        self.colorBackSelectedPicker.SetColour (self._config.colorBackSelected.value)


    def _saveColorsState (self):
        self._config.colorFontNormal.value = self.colorFontNormalPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)
        self._config.colorFontNormalHover.value = self.colorFontNormalHoverPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)

        self._config.colorFontSelected.value = self.colorFontSelectedPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)
        self._config.colorFontSelectedHover.value = self.colorFontSelectedHoverPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)

        self._config.colorBackSelected.value = self.colorBackSelectedPicker.GetColour().GetAsString (wx.C2S_HTML_SYNTAX)


    def _saveActionsState (self):
        leftClickAction = self.leftClickActionCombo.GetSelection()
        middleClickAction = self.middleClickActionCombo.GetSelection()

        assert leftClickAction >= 0 and leftClickAction < len (self._actions)
        assert middleClickAction >= 0 and middleClickAction < len (self._actions)

        self._config.leftClickAction.value = self._actions[leftClickAction][1]
        self._config.middleClickAction.value = self._actions[middleClickAction][1]


    def Save (self):
        self._saveColorsState()
        self._saveActionsState()
