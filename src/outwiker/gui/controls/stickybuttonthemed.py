# -*- coding=utf-8 -*-

from outwiker.gui.theme import Theme
from .stickybutton import StickyButton


class StickyButtonThemed(StickyButton):
    def SetTheme(self, theme: Theme):
        self.SetColorNormal(theme.colorBackground)
        self.SetColorToggled(theme.colorBackgroundSelected)
        self.SetColorTextNormal(theme.colorText)
        self.SetColorTextToggled(theme.colorTextSelected)
        self.SetColorShadow(theme.get(Theme.SECTION_GENERAL, Theme.SHADOW_COLOR))
        self.SetRoundRadius(theme.get(Theme.SECTION_GENERAL, Theme.ROUND_RADIUS))
