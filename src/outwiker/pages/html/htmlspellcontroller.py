# -*- coding: UTF-8 -*-

import threading

import wx

from outwiker.gui.texteditor import ApplyStyleEvent
from outwiker.gui.texteditorhelper import TextEditorHelper
from htmlpage import HtmlWikiPage


class HtmlSpellController (object):
    """Spell controller for HTML editor"""
    def __init__(self, application):
        self._application = application
        self._colorizingThread = None


    def initialize (self, page):
        if page.getTypeString() == HtmlWikiPage.getTypeString():
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
        helper = TextEditorHelper()
        textlength = helper.calcByteLen (text)
        stylebytes = [0] * textlength
        editor.runSpellChecking (stylebytes, text, 0, len (text))

        event = ApplyStyleEvent (text=text,
                                 stylebytes=None,
                                 indicatorsbytes = stylebytes)
        wx.PostEvent (editor, event)
