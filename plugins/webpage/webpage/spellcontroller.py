# -*- coding: utf-8 -*-

from outwiker.api.core.spellchecker import SimpleSpellController

from .webnotepage import WebNotePage


class WebPageSpellController(SimpleSpellController):
    """Spell controller for HTML editor on Web page"""

    def initialize(self, page):
        if page.getTypeString() == WebNotePage.getTypeString():
            self._bindEvents()
