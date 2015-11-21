# -*- coding: UTF-8 -*-

import threading

import wx

from outwiker.gui.texteditor import ApplyStyleEvent
from wikicolorizer import WikiColorizer
from wikieditor import WikiEditor
from wikipage import WikiWikiPage


class WikiColorizerController (object):
    """Controller for colorize text in wiki editor"""
    def __init__(self, application):
        self._application = application
        self._colorizingThread = None

        self._runColorizingEvent = threading.Event()


    def initialize (self, page):
        if page.getTypeString() == WikiWikiPage.getTypeString():
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

        event = ApplyStyleEvent (text=text,
                                 stylebytes=stylebytes,
                                 indicatorsbytes = stylebytes)
        wx.PostEvent (editor, event)


    def __onPreferencesDialogCreate (self, dialog):
        self._stopColorizing()


    def __onPageSelect (self, page):
        self._stopColorizing()
