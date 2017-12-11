# -*- coding: UTF-8 -*-

from .fontsizebase import WikiFontSizeBaseAction


class WikiFontSizeBigAction (WikiFontSizeBaseAction):
    """
    Действие для выделения текста крупным шрифтом
    """
    stringId = u"WikiBigFont"

    @property
    def title (self):
        return _(u"Big font")


    @property
    def description (self):
        return _(u"Big font")


    def run (self, params):
        self.selectFontSize (4)
