# -*- coding: utf-8 -*-

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.events import AttachListChangedParams


class AttachWatcher(object):
    def __init__(self, application, period_ms):
        self._application = application
        self._period = period_ms
        self._oldFilesList = []
        self._watchedPage = None
        self._timer = None

    def initialize(self):
        self._timer = wx.Timer()
        self._timer.Bind(wx.EVT_TIMER, handler=self._onTimer)
        self._application.onWikiClose += self._onWikiClose
        self._application.onPageSelect += self._onPageSelect
        self._application.onAttachListChanged += self._onAttachListChanged
        self._start_watch()

    def clear(self):
        self._application.onWikiClose -= self._onWikiClose
        self._application.onPageSelect -= self._onPageSelect
        self._application.onAttachListChanged -= self._onAttachListChanged
        self._stop_watch()
        self._timer.Unbind(wx.EVT_TIMER, handler=self._onTimer)
        self._timer = None

    def _onAttachListChanged(self, page, params):
        if page == self._watchedPage:
            attach = Attachment(self._watchedPage)
            self._oldFilesList = attach.getAttachRelative()

    def _onWikiClose(self, root):
        self._stop_watch()

    def _onPageSelect(self, page):
        self._checkAttachListForPage(self._watchedPage)
        self._stop_watch()
        self._start_watch()

    def _start_watch(self):
        if self._application.selectedPage is None:
            return

        self._watchedPage = self._application.selectedPage
        attach = Attachment(self._watchedPage)
        self._oldFilesList = attach.getAttachRelative()
        self._timer.Start(self._period)

    def _stop_watch(self):
        self._timer.Stop()
        self._watchedPage = None
        self._oldFilesList = []

    def _onTimer(self, event):
        self._checkAttachListForPage(self._application.selectedPage)

    def _checkAttachListForPage(self, page):
        if page is None or self._watchedPage != page:
            return

        attach = Attachment(page)
        current_list = attach.getAttachRelative()
        if set(self._oldFilesList) != set(current_list):
            eventParam = AttachListChangedParams()
            self._application.onAttachListChanged(self._watchedPage,
                                                  eventParam)
