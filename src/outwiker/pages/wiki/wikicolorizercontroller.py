# -*- coding: utf-8 -*-

import threading

import wx

from outwiker.gui.basetextstylingcontroller import BaseTextStylingController

from outwiker.pages.wiki.wikicolorizer import WikiColorizer
from outwiker.pages.wiki.wikieditor import WikiEditor


class WikiColorizerController(BaseTextStylingController):
    """Controller for colorize text in wiki editor"""

    def getColorizingThread(self, page, params, runEvent):
        if isinstance(params.editor, WikiEditor):
            return threading.Thread(
                None,
                self._colorizeThreadFunc,
                args=(params.text,
                      params.editor,
                      params.editor.colorizeSyntax,
                      params.editor.enableSpellChecking,
                      runEvent)
            )
        else:
            return None

    def _colorizeThreadFunc(self,
                            text,
                            editor,
                            colorizeSyntax,
                            enableSpellChecking,
                            runEvent):
        colorizer = WikiColorizer(editor,
                                  colorizeSyntax,
                                  enableSpellChecking,
                                  runEvent)
        stylingInfo = colorizer.colorize(text)

        if self._runColorizingEvent.is_set():
            self.updateStyles(editor,
                              text,
                              stylingInfo.styleBytes)

        wx.CallAfter(editor.markSpellErrors, stylingInfo.spellStatusFlags)
