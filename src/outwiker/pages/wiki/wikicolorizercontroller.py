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


    def initialize (self, page):
        if page.getTypeString() == WikiWikiPage.getTypeString():
            self._application.onEditorStyleNeeded += self.__onEditorStyleNeeded


    def clear (self):
        self._application.onEditorStyleNeeded -= self.__onEditorStyleNeeded

        if self._colorizingThread is not None:
            self._colorizingThread.join()


    def __onEditorStyleNeeded (self, page, params):
        if not isinstance (params.editor, WikiEditor):
            return

        if (self._colorizingThread is None or
                not self._colorizingThread.isAlive()):
            self._colorizingThread = threading.Thread (
                None,
                self._colorizeThreadFunc,
                args=(params.text,
                      params.editor,
                      params.editor.colorizeSyntax)
            )

            self._colorizingThread.start()


    def _colorizeThreadFunc (self, text, editor, colorizeSyntax):
        colorizer = WikiColorizer (editor, colorizeSyntax)
        stylebytes = colorizer.colorize (text)

        event = ApplyStyleEvent (text=text,
                                 stylebytes=stylebytes,
                                 indicatorsbytes = stylebytes)
        wx.PostEvent (editor, event)
