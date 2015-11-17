# -*- coding: UTF-8 -*-

import threading

import wx

from outwiker.gui.controllers.basecontroller import BaseController


class HtmlSpellController (BaseController):
    """Spell controller for HTML editor"""
    def __init__(self, application):
        super(HtmlSpellController, self).__init__()
        self._application = application
        self._colorizingThread = None


    def initialize (self):
        self._application.onEditorStyleNeeded += self.__onEditorStyleNeeded


    def clear (self):
        self._application.onEditorStyleNeeded -= self.__onEditorStyleNeeded
        if self._colorizingThread is not None:
            self._colorizingThread.join()


    def __onEditorStyleNeeded (self, page, params):
        if (self._colorizingThread is None or
                not self._colorizingThread.isAlive()):
            self._colorizingThread = threading.Thread (
                None,
                self._colorizeThreadFunc,
                args=(params.text,
                      params.editor)
            )

            self._colorizingThread.start()


    def _colorizeThreadFunc (self, text, editor):
        textlength = editor.calcByteLen (text)
        stylebytes = [0] * textlength
        editor.runSpellChecking (stylebytes, 0, len (text))

        wx.CallAfter (editor.applyStyle, text, None, stylebytes)
