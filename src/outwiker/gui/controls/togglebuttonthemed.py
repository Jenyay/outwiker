# -*- coding=utf-8 -*-

from .togglebutton import ToggleButton
from outwiker.gui.theme import Theme


class ToggleButtonThemed(ToggleButton):
    def SetTheme(self, theme):
        self.SetColorNormal(theme.colorBackground)
        self.SetColorToggled(theme.colorBackgroundSelected)
        self.SetColorShadow(theme.get(Theme.SECTION_GENERAL, Theme.SHADOW_COLOR))
        self.SetColorTextNormal(theme.colorText)
        self.SetColorTextToggled(theme.colorTextSelected)
        self.SetColorBorderToggled(theme.get(Theme.SECTION_GENERAL, Theme.CONTROL_BORDER_SELECTED_COLOR))
        self.SetColorBorder(theme.get(Theme.SECTION_GENERAL, Theme.CONTROL_BORDER_COLOR))
        self.SetRoundRadius(theme.get(Theme.SECTION_GENERAL, Theme.ROUND_RADIUS))
