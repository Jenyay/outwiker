# -*- coding=utf-8 -*-

from outwiker.gui.controls.togglebutton import ToggleButton


class ToggleButtonThemed(ToggleButton):
    def setTheme(self, theme):
        self.SetColorNormal(theme.colorBackground)
        self.SetColorToggled(theme.colorBackgroundSelected)
        self.SetColorShadow(theme.colorShadow)
        self.SetColorTextNormal(theme.colorTextNormal)
        self.SetColorTextToggled(theme.colorTextNormal)
        self.SetRoundRadius(theme.roundRadius)