# -*- coding=utf-8 -*-

from stickybutton import StickyButton


class StickyButtonThemed(StickyButton):
    def SetTheme(self, theme):
        self.SetColorNormal(theme.colorBackground)
        self.SetColorToggled(theme.colorBackgroundSelected)
        self.SetColorShadow(theme.colorShadow)
        self.SetColorTextNormal(theme.colorTextNormal)
        self.SetColorTextToggled(theme.colorTextSelected)
        self.SetRoundRadius(theme.roundRadius)
