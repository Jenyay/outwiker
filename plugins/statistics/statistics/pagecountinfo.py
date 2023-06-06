# -*- coding: utf-8 -*-

from .i18n import get_


class PageCountInfo:
    """Класс для оформления информации о количестве страниц в дереве"""

    def __init__(self, pageCount):
        self._pageCount = pageCount

        global _
        _ = get_()

    @property
    def content(self):
        return "<p>" + _("Page count: {0}").format(self._pageCount) + "</p><hr/>"
