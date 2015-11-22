# -*- coding: UTF-8 -*-

from outwiker.gui.simplespellcontroller import SimpleSpellController
from htmlpage import HtmlWikiPage


class HtmlSpellController (SimpleSpellController):
    """Spell controller for HTML editor"""
    def initialize (self, page):
        if page.getTypeString() == HtmlWikiPage.getTypeString():
            self._bindEvents()
