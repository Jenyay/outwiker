# -*- coding: utf-8 -*-

import threading

from outwiker.api.gui.basetextstylingcontroller import BaseTextStylingController

from .colorizer import MarkdownColorizer
from .markdowneditor import MarkdownEditor


class ColorizerController(BaseTextStylingController):
    """Controller for colorize text in Markdown editor"""

    def getColorizingThread(self, page, params, runEvent):
        if isinstance(params.editor, MarkdownEditor):
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
        colorizer = MarkdownColorizer(editor,
                                      colorizeSyntax,
                                      enableSpellChecking,
                                      runEvent)
        stylebytes = colorizer.colorize(text)

        if self._runColorizingEvent.is_set():
            self.updateStyles(editor,
                              text,
                              stylebytes)
