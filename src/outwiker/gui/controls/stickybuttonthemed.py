# -*- coding=utf-8 -*-

from stickybutton import StickyButton


class StickyButtonThemed(StickyButton):
    def SetTheme(self, theme):
        self.SetColorNormal(theme.colorBackground)
        self.SetColorToggled(theme.colorBackgroundSelected)
        self.SetColorShadow(theme.colorShadow)
        self.SetColorTextNormal(theme.colorTextNormal)
        self.SetColorTextToggled(theme.colorTextNormal)
        self.SetRoundRadius(theme.roundRadius)
