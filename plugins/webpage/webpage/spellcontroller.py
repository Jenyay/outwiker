# -*- coding: utf-8 -*-

from outwiker.api.core.spellchecker import SimpleSpellController

from .defines import PAGE_TYPE_STRING


class WebPageSpellController(SimpleSpellController):
    """Spell controller for HTML editor on Web page"""

    def initialize(self, page):
        if page.getTypeString() == PAGE_TYPE_STRING:
            self._bindEvents()
