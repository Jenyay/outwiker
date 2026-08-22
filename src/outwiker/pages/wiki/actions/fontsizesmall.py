# -*- coding: utf-8 -*-

from .fontsizebase import WikiFontSizeBaseAction


class WikiFontSizeSmallAction(WikiFontSizeBaseAction):
    """
    Действие для выделения текста мелким шрифтом
    """

    stringId = "WikiSmallFont"

    @property
    def title(self):
        return _("Small font")

    @property
    def description(self):
        return _("Small font")

    def run(self, params):
        self.selectFontSize(3)
