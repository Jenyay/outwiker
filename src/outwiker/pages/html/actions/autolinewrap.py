# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from ..defines import PAGE_TYPE_STRING


class HtmlAutoLineWrap(BaseAction):
    """Enable / disable auto line wrap on HTML pages."""

    stringId = "HtmlAutoLineWrap"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Auto Line Wrap")

    @property
    def description(self):
        return _("Auto line wrap for HTML pages")

    def run(self, checked):
        assert self._application.selectedPage.getTypeString() == PAGE_TYPE_STRING
        self._application.selectedPage.autoLineWrap = checked
