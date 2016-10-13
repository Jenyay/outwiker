# -*- coding: UTF-8 -*-

from outwiker.gui.simplespellcontroller import SimpleSpellController
from webnotepage import WebNotePage


class WebPageSpellController (SimpleSpellController):
    """Spell controller for HTML editor on Web page"""
    def initialize(self, page):
        if page.getTypeString() == WebNotePage.getTypeString():
            self._bindEvents()
