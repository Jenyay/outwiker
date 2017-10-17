# -*- coding=utf-8 -*-

from togglebutton import ToggleButton


class ToggleButtonThemed(ToggleButton):
    def SetTheme(self, theme):
        self.SetColorNormal(theme.colorBackground)
        self.SetColorToggled(theme.colorBackgroundSelected)
        self.SetColorShadow(theme.colorShadow)
        self.SetColorTextNormal(theme.colorTextNormal)
        self.SetColorTextToggled(theme.colorTextSelected)
        self.SetColorBorderToggled(theme.colorBorderSelected)
        self.SetRoundRadius(theme.roundRadius)
