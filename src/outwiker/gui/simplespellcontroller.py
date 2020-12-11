# -*- coding: utf-8 -*-

import threading

import wx

from outwiker.gui.texteditorhelper import TextEditorHelper
from outwiker.gui.basetextstylingcontroller import BaseTextStylingController


class SimpleSpellController(BaseTextStylingController):
    """
    Base class for styling controller which spell check only
    """

    def __init__(self, application, pageTypeString=None):
        super().__init__(application, pageTypeString)
        self._helper = TextEditorHelper()

    def getColorizingThread(self, page, params, runEvent):
        return threading.Thread(
            None,
            self._colorizeThreadFunc,
            args=(params.text,
                  params.editor,
                  params.enableSpellChecking)
        )

    def _colorizeThreadFunc(self, text, editor, enableSpellChecking):
        if not enableSpellChecking:
            return

        textlength = self._helper.calcByteLen(text)
        spellStatusFlags = [True] * textlength

        for start, end in self._splitText(text):
            if not self._runColorizingEvent.is_set():
                return
            self._checkSpell(editor, text, start, end, spellStatusFlags)

        wx.CallAfter(editor.markSpellErrors, spellStatusFlags)

    def _checkSpell(self, editor, text, start, end, spellStatusFlags):
        spellChecker = editor.getSpellChecker()
        errors = spellChecker.findErrors(text[start: end])

        for _word, err_start, err_end in errors:
            startbytes = self._helper.calcBytePos(text, err_start + start)
            endbytes = self._helper.calcBytePos(text, err_end + start)
            spellStatusFlags[startbytes:
                             endbytes] = [False] * (endbytes - startbytes)

    def _splitText(self, text):
        """
        Return part of the text for spell checking
        """
        portion = 8000
        position = 0
        length = len(text)

        while position < length:
            newposition = text.rfind(u' ', position, position + portion)
            if newposition != -1:
                yield (position, newposition)
                position = newposition + 1
            else:
                yield (position, len(text))
                break
