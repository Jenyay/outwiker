# -*- coding: utf-8 -*-

import wx

from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.core.attachment import Attachment


class AttachWatcher(object):
    def __init__(self, application):
        self._application = application
        self._is_run = False
        self._watcher = wx.FileSystemWatcher()
        self._watcher.Bind(wx.EVT_FSWATCHER, handler=self._onFSWatcher)

    def initialize(self):
        self._application.onWikiClose += self._onWikiClose
        self._application.onPageSelect += self._onPageSelect
        self._start_watch()

    def clear(self):
        self._application.onWikiClose -= self._onWikiClose
        self._application.onPageSelect -= self._onPageSelect
        self._stop_watch()
        self._watcher.Unbind(wx.EVT_FSWATCHER)

    def _onWikiClose(self, root):
        self._stop_watch()

    def _onPageSelect(self, page):
        self._stop_watch()
        self._start_watch()

    def _start_watch(self):
        self._is_run = True

    def _stop_watch(self):
        self._watcher.RemoveAll()
        self._is_run = False

    def _onFSWatcher(self, event):
        pass
