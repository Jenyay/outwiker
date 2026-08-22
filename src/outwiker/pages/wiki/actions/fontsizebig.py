# -*- coding: utf-8 -*-

from .fontsizebase import WikiFontSizeBaseAction


class WikiFontSizeBigAction(WikiFontSizeBaseAction):
    """
    Действие для выделения текста крупным шрифтом
    """

    stringId = "WikiBigFont"

    @property
    def title(self):
        return _("Big font")

    @property
    def description(self):
        return _("Big font")

    def run(self, params):
        self.selectFontSize(4)
