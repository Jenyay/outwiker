# -*- coding: utf-8 -*-

import os.path

import wx

from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.core.attachment import Attachment
from outwiker.core.events import AttachListChangedParams


class AttachWatcher(object):
    def __init__(self, application):
        self._application = application
        self._watcher = wx.FileSystemWatcher()
        self._oldFilesList = []
        self._watchedPage = None
        self._watched_dir = None

    def initialize(self):
        self._application.onWikiClose += self._onWikiClose
        self._application.onPageSelect += self._onPageSelect
        self._start_watch()
        self._watcher.Bind(wx.EVT_FSWATCHER, handler=self._onFSWatcher)

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
        if self._application.selectedPage is None:
            return

        self._watchedPage = self._application.selectedPage

        # If the "__attach" directory is not exists then watch for
        # a page directory and wait while "__attach" will be created.
        attach = Attachment(self._watchedPage)
        attach_dir = attach.getAttachPath(create=False)

        self._oldFilesList = attach.getAttachRelative()
        # Event flags (filters) for FileSystemWatcher.Add() method:
        # 'FSW_EVENT_ACCESS', 'FSW_EVENT_ALL', 'FSW_EVENT_ATTRIB',
        # 'FSW_EVENT_CREATE', 'FSW_EVENT_DELETE', 'FSW_EVENT_ERROR',
        # 'FSW_EVENT_MODIFY', 'FSW_EVENT_RENAME', 'FSW_EVENT_UNMOUNT',
        # 'FSW_EVENT_WARNING',

        # The flags works in Linux only
        # flags = wx.FSW_EVENT_CREATE | wx.FSW_EVENT_DELETE | wx.FSW_EVENT_RENAME
        flags = wx.FSW_EVENT_ALL

        if os.path.exists(attach_dir):
            self._watched_dir = attach_dir
            self._watcher.Add(self._watched_dir, flags)
        else:
            self._watched_dir = self._watchedPage.path
            self._watcher.Add(self._watched_dir, wx.FSW_EVENT_CREATE)

    def _stop_watch(self):
        self._watcher.RemoveAll()
        self._watchedPage = None

    def _onFSWatcher(self, event):
        change_type = event.GetChangeType()

        if (change_type != wx.FSW_EVENT_CREATE and
                change_type != wx.FSW_EVENT_DELETE and
                change_type != wx.FSW_EVENT_RENAME):
            return

        current_dir = self._watched_dir
        if current_dir.endswith('/') or current_dir.endswith('\\'):
            current_dir = current_dir[:-1]

        # Watch for the attachments directory
        if current_dir.endswith(PAGE_ATTACH_DIR):
            self._checkForAttachChanges()
        else:
            self._checkForNewAttachDir()

    def _checkForAttachChanges(self):
        attach = Attachment(self._watchedPage)
        current_list = attach.getAttachRelative()
        if set(self._oldFilesList) != set(current_list):
            self._oldFilesList = current_list
            eventParam = AttachListChangedParams()
            self._application.onAttachListChanged(self._watchedPage,
                                                  eventParam)

    def _checkForNewAttachDir(self):
        self._checkForAttachChanges()

        attach = Attachment(self._watchedPage)
        if os.path.exists(attach.getAttachPath(create=False)):
            self._stop_watch()
            self._start_watch()
