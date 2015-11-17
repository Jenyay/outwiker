# -*- coding: UTF-8 -*-

import threading

import wx

from outwiker.gui.controllers.basecontroller import BaseController
from outwiker.gui.texteditor import ApplyStyleEvent

from wikicolorizer import WikiColorizer
from wikieditor import WikiEditor


class WikiColorizerController (BaseController):
    """GUI controller for wiki page"""
    def __init__(self, application):
        super(WikiColorizerController, self).__init__()
        self._application = application
        self._colorizingThread = None


    def initialize (self):
        self._application.onEditorStyleNeeded += self.__onEditorStyleNeeded


    def clear (self):
        self._application.onEditorStyleNeeded -= self.__onEditorStyleNeeded


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
        stylebytes = self._getStyleBytes (editor, text, colorizeSyntax)
        event = ApplyStyleEvent (text=text,
                                 stylebytes=stylebytes,
                                 indicatorsbytes = stylebytes)
        wx.PostEvent (editor, event)


    def _getStyleBytes (self, editor, text, colorizeSyntax):
        colorizer = WikiColorizer (editor, colorizeSyntax)
        stylebytes = colorizer.colorize (text)
        return stylebytes
