# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional
import datetime

import wx

from outwiker.core.application import ApplicationParams
from outwiker.gui.defines import (STATUSBAR_MESSAGE_ITEM,
                                  STATUSBAR_PAGE_DATETIME_ITEM)
from .guiconfig import MainWindowConfig, GeneralGuiConfig


@dataclass(slots=True)
class StatusBarItemInfo:
    name: str
    position: int
    width: int


class StatusBarController:
    def __init__(self,
                 statusbar: wx.StatusBar,
                 application: ApplicationParams):
        self._statusbar = statusbar
        self._application = application

        self._mainWindowConfig = MainWindowConfig(self._application.config)
        self._generalConfig = GeneralGuiConfig(self._application.config)
        datetime_width = self._mainWindowConfig.datetimeStatusWidth.value

        self._statusbar_items: List[StatusBarItemInfo] = []

        self.addItem(STATUSBAR_MESSAGE_ITEM)
        self.addItem(STATUSBAR_PAGE_DATETIME_ITEM, datetime_width)

        self._bindEvents()

    def addItem(self, name: str, width: int = -1, position: Optional[int] = None) -> None:
        if position:
            item = StatusBarItemInfo(name, position, width)
            self._statusbar_items.insert(position, item)
        else:
            item = StatusBarItemInfo(name, len(self._statusbar_items), width)
            self._statusbar_items.append(item)

        for n, item in enumerate(self._statusbar_items):
            item.position = n

        self._initStatusBar()

    def setStatusText(self, name: str, text: str) -> None:
        position = None
        for item in self._statusbar_items:
            if item.name == name:
                position = item.position
                break

        if position is not None:
            self._statusbar.SetStatusText(text, position)

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
        widths = [item.width for item in self._statusbar_items]
        self._statusbar.SetFieldsCount(len(widths), widths)
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

        self.setStatusText(STATUSBAR_PAGE_DATETIME_ITEM, text)

    def _onPreferencesDialogClose(self, _prefDialog):
        """
        Обработчик события изменения настроек главного окна
        """
        self._updatePageDateTime()
        self.updateStatusBar()

    def updateStatusBar(self):
        self._statusbar.Show(self._mainWindowConfig.statusbar_visible.value)
