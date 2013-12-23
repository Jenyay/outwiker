#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlAutoLineWrap (BaseAction):
    """
    Выделение текста полужирным шрифтом (добавление тега <B>)
    """
    stringId = u"HtmlAutoLineWrap"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Auto Line Wrap")


    @property
    def description (self):
        return _(u"Auto line wrap for HTML pages")


    def run (self, checked):
        assert self._application.selectedPage.getTypeString() == "html"

        self._application.selectedPage.autoLineWrap = checked
