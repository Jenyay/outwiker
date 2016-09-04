# -*- coding: UTF-8 -*-

import threading

from outwiker.gui.basetextstylingcontroller import BaseTextStylingController

from wikicolorizer import WikiColorizer


class WikiColorizerController(BaseTextStylingController):
    """Controller for colorize text in wiki editor"""

    def getColorizingThread(self, page, params, runEvent):
        return threading.Thread(
            None,
            self._colorizeThreadFunc,
            args=(params.text,
                  params.editor,
                  params.editor.colorizeSyntax,
                  params.editor.enableSpellChecking,
                  runEvent)
        )

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
        stylebytes = colorizer.colorize(text)

        if self._runColorizingEvent.is_set():
            self.updateStyles(editor,
                              text,
                              stylebytes,
                              stylebytes,
                              0,
                              len(text))
