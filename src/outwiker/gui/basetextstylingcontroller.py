# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import threading

import wx

from outwiker.gui.texteditor import ApplyStyleEvent


class BaseTextStylingController (object):
    __metaclass__ = ABCMeta


    def __init__(self, application):
        self._application = application
        self._colorizingThread = None
        self._runColorizingEvent = threading.Event()


    @abstractmethod
    def _onEditorStyleNeeded (self, page, params):
        pass


    @abstractmethod
    def initialize (self, page):
        pass


    def clear (self):
        self._unbindEvents()
        self._stopColorizing()


    def _bindEvents (self):
        self._application.onEditorStyleNeeded += self._onEditorStyleNeeded
        self._application.onPreferencesDialogCreate += self._stopEventHandler
        self._application.onPageSelect += self._stopEventHandler


    def _unbindEvents (self):
        self._application.onEditorStyleNeeded -= self._onEditorStyleNeeded
        self._application.onPreferencesDialogCreate -= self._stopEventHandler
        self._application.onPageSelect -= self._stopEventHandler


    def _stopColorizing (self):
        self._runColorizingEvent.clear()

        if self._colorizingThread is not None:
            self._colorizingThread.join()
            self._colorizingThread = None


    def _updateStyles (self, editor, text, stylebytes, indicatorsbytes, start, end):
        event = ApplyStyleEvent (text=text,
                                 stylebytes=stylebytes,
                                 indicatorsbytes = indicatorsbytes,
                                 start = start,
                                 end = end)
        wx.PostEvent (editor, event)


    def _stopEventHandler (self, *args, **kwargs):
        self._stopColorizing()
