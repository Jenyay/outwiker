# -*- coding: UTF-8 -*-

from outwiker.gui.simplespellcontroller import SimpleSpellController
from textpage import TextWikiPage


class TextSpellController (SimpleSpellController):
    """Spell controller for simple text editor"""
    def initialize (self, page):
        if page.getTypeString() == TextWikiPage.getTypeString():
            self._bindEvents()
