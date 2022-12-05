# -*- coding: utf-8 -*-

import datetime

import wx

from outwiker.core.commands import setStatusText
from outwiker.core.application import ApplicationParams
from .guiconfig import MainWindowConfig, GeneralGuiConfig


class StatusBarController:
    def __init__(self,
                 statusbar: wx.StatusBar,
                 application: ApplicationParams):
        self._statusbar = statusbar
        self._application = application

        self._mainWindowConfig = MainWindowConfig(self._application.config)
        self._generalConfig = GeneralGuiConfig(self._application.config)
        datetime_width = self._mainWindowConfig.datetimeStatusWidth.value

        self._ATTACH_INFO_STATUS_ITEM = 1
        self._DATETIME_STATUS_ITEM = 2
        self._status_items_width = [-1, -1, datetime_width]
        self._items_count = len(self._status_items_width)

        self._bindEvents()
        self._initStatusBar()

    def destroy(self):
        self._unbindEvents()

    def _bindEvents(self):
        self._application.onTreeUpdate += self._onTreeUpdate
        self._application.onPageUpdate += self._onPageUpdate
        self._application.onWikiOpen += self._onWikiOpen
        self._application.onPageSelect += self._onPageSelect
        self._application.onPreferencesDialogClose += self._onPreferencesDialogClose

    def _unbindEvents(self):
        self._application.onTreeUpdate -= self._onTreeUpdate
        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onWikiOpen -= self._onWikiOpen
        self._application.onPageSelect -= self._onPageSelect
        self._application.onPreferencesDialogClose -= self._onPreferencesDialogClose

    def _initStatusBar(self):
        self._statusbar.SetFieldsCount(self._items_count)
        self._statusbar.SetStatusWidths(self._status_items_width)
        self.updateStatusBar()

    def _onTreeUpdate(self, _sender):
        self._updatePageDateTime()

    def _onPageUpdate(self, _page, **_kwargs):
        self._updatePageDateTime()

    def _onWikiOpen(self, _wikiroot):
        self._updatePageDateTime()

    def _onPageSelect(self, _newpage):
        self._updatePageDateTime()

    def _updatePageDateTime(self):
        dateFormat = self._generalConfig.dateTimeFormat.value
        text = ''

        if(self._application.selectedPage is not None and
                self._application.selectedPage.datetime is not None):
            text = datetime.datetime.strftime(
                self._application.selectedPage.datetime,
                dateFormat)

        setStatusText(text, self._DATETIME_STATUS_ITEM)

    def _onPreferencesDialogClose(self, _prefDialog):
        """
        Обработчик события изменения настроек главного окна
        """
        self._updatePageDateTime()
        self.updateStatusBar()

    def updateStatusBar(self):
        self._statusbar.Show(self._mainWindowConfig.statusbar_visible.value)
