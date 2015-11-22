# -*- coding: UTF-8 -*-

import threading

from outwiker.gui.basetextstylingcontroller import BaseTextStylingController

from wikicolorizer import WikiColorizer
from wikieditor import WikiEditor
from wikipage import WikiWikiPage


class WikiColorizerController (BaseTextStylingController):
    """Controller for colorize text in wiki editor"""
    def initialize (self, page):
        if page.getTypeString() == WikiWikiPage.getTypeString():
            self._bindEvents()


    def _onEditorStyleNeeded (self, page, params):
        if not isinstance (params.editor, WikiEditor):
            return

        if (self._colorizingThread is None or
                not self._colorizingThread.isAlive()):
            self._runColorizingEvent.set()

            self._colorizingThread = threading.Thread (
                None,
                self._colorizeThreadFunc,
                args=(params.text,
                      params.editor,
                      params.editor.colorizeSyntax,
                      params.editor.enableSpellChecking,
                      self._runColorizingEvent)
            )

            self._colorizingThread.start()


    def _colorizeThreadFunc (self, text, editor, colorizeSyntax, enableSpellChecking, runEvent):
        colorizer = WikiColorizer (editor, colorizeSyntax, enableSpellChecking, runEvent)
        stylebytes = colorizer.colorize (text)

        if self._runColorizingEvent.is_set():
            self._updateStyles (editor,
                                text,
                                stylebytes,
                                stylebytes,
                                0,
                                len (text))
