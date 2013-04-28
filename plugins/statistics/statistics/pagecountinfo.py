#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .i18n import get_


class PageCountInfo (object):
    """Класс для оформления информации о количестве страниц в дереве"""
    def __init__(self, treestat):
        self._treestat = treestat

        global _
        _ = get_()


    @property
    def content (self):
        return u"<p>" + _(u"Page count: {0}").format (self._treestat.pageCount) + "</p><hr/>";
