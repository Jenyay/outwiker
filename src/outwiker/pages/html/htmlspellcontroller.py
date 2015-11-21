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
        self._runColorizingEvent = threading.Event()


    def initialize (self, page):
        if page.getTypeString() == HtmlWikiPage.getTypeString():
            self._application.onEditorStyleNeeded += self.__onEditorStyleNeeded
            self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
            self._application.onPageSelect += self.__onPageSelect


    def clear (self):
        self._application.onEditorStyleNeeded -= self.__onEditorStyleNeeded
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self._application.onPageSelect -= self.__onPageSelect

        self._stopColorizing()


    def _stopColorizing (self):
        self._runColorizingEvent.clear()

        if self._colorizingThread is not None:
            self._colorizingThread.join()


    def __onEditorStyleNeeded (self, page, params):
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
                position += portion
            else:
                yield (position, len(text))
                break


    def _updateStyles (self, editor, text, stylebytes, indicatorsbytes):
        event = ApplyStyleEvent (text=text,
                                 stylebytes=stylebytes,
                                 indicatorsbytes = indicatorsbytes)
        wx.PostEvent (editor, event)


    def __onPreferencesDialogCreate (self, dialog):
        self._stopColorizing()


    def __onPageSelect (self, page):
        self._stopColorizing()
