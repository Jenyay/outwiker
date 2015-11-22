# -*- coding: UTF-8 -*-

import threading

from outwiker.gui.texteditorhelper import TextEditorHelper
from outwiker.gui.basetextstylingcontroller import BaseTextStylingController


class SimpleSpellController (BaseTextStylingController):
    """
    Base class for styling controller which spell check only
    """
    def _onEditorStyleNeeded (self, page, params):
        if (self._colorizingThread is None or
                not self._colorizingThread.isAlive()):
            self._runColorizingEvent.set()

            self._colorizingThread = threading.Thread (
                None,
                self._colorizeThreadFunc,
                args=(params.text,
                      params.editor,
                      params.enableSpellChecking)
            )

            self._colorizingThread.start()


    def _colorizeThreadFunc (self, text, editor, enableSpellChecking):
        helper = TextEditorHelper()
        textlength = helper.calcByteLen (text)
        stylebytes = [0] * textlength

        if enableSpellChecking:
            for start, end in self._splitText (text):
                if not self._runColorizingEvent.is_set():
                    break

                editor.runSpellChecking (stylebytes, text, start, end)
                self._updateStyles (editor, text, None, stylebytes)

        self._updateStyles (editor, text, None, stylebytes)


    def _splitText (self, text):
        """
        Return part of the text for spell checking
        """
        portion = 8000
        position = 0
        length = len (text)

        while position < length:
            newposition = text.rfind (u' ', position, position + portion)
            if newposition != -1:
                yield (position, newposition)
            else:
                yield (position, len(text))

            position += portion
