# -*- coding: utf-8 -*-

import datetime

import wx

from outwiker.core.commands import setStatusText
from outwiker.core.application import ApplicationParams
from .guiconfig import MainWindowConfig, GeneralGuiConfig


class StatusBarController(object):
    def __init__(self,
                 statusbar: wx.StatusBar,
                 application: ApplicationParams):
        self._statusbar = statusbar
        self._application = application
        self._items_count = 2

        self._mainWindowConfig = MainWindowConfig(self._application.config)
        self._generalConfig = GeneralGuiConfig(self._application.config)

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
        datetime_width = self._mainWindowConfig.datetimeStatusWidth.value
        self._statusbar.SetFieldsCount(self._items_count)
        self._statusbar.SetStatusWidths([-1, datetime_width])
        self.updateStatusBar()

    def _onTreeUpdate(self, sender):
        self.updatePageDateTime()

    def _onPageUpdate(self, page, **kwargs):
        self.updatePageDateTime()

    def _onWikiOpen(self, wikiroot):
        self.updatePageDateTime()

    def _onPageSelect(self, newpage):
        self.updatePageDateTime()

    def updatePageDateTime(self):
        statusbar_item = 1

        dateFormat = self._generalConfig.dateTimeFormat.value
        text = u""

        if(self._application.selectedPage is not None and
                self._application.selectedPage.datetime is not None):
            text = datetime.datetime.strftime(
                self._application.selectedPage.datetime,
                dateFormat)

        setStatusText(text, statusbar_item)

    def _onPreferencesDialogClose(self, prefDialog):
        """
        Обработчик события изменения настроек главного окна
        """
        self.updatePageDateTime()
        self.updateStatusBar()

    def updateStatusBar(self):
        self._statusbar.Show(self._mainWindowConfig.statusbar_visible.value)
