# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Set

import wx

from outwiker.api.core.events import (
    PAGE_UPDATE_CONTENT,
    NotesTreeItemsPreparingParams,
    ForceNotesTreeItemsUpdate,
)
from outwiker.api.gui.controls import NotesTreeItem

from .i18n import get_


class Controller:
    def __init__(self, plugin, application):
        """ """
        self._plugin = plugin
        self._application = application

        # Set of marked subpaths of pages
        self._markedPages: Set[str] = set()

    def initialize(self):
        global _
        _ = get_()

        self._application.onNotesTreeItemsPreparing += self._onNotesTreeItemsPreparing
        self._application.onPageUpdate += self._onPageUpdate
        self._application.onTreeUpdate += self._onTreeUpdate

    def destroy(self):
        """
        Run on plugin deactivation
        """
        self._application.onNotesTreeItemsPreparing -= self._onNotesTreeItemsPreparing
        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onTreeUpdate -= self._onTreeUpdate

    def _onTreeUpdate(self, sender):
        self._markedPages.clear()

    def _onPageUpdate(self, page, change):
        if change == PAGE_UPDATE_CONTENT and page.subpath not in self._markedPages:
            self._application.onForceNotesTreeItemsUpdate(
                self._application.selectedPage,
                ForceNotesTreeItemsUpdate(pages=[page])
            )

    def _onNotesTreeItemsPreparing(self, page, params: NotesTreeItemsPreparingParams):
        """
        onNotesTreeItemsPreparing event handler
        """
        self._markItems(params.visible_items)

    def _markItems(self, items: List[NotesTreeItem]):
        nowColor = wx.Colour(0, 0, 255)
        now = datetime.now()
        for item in items:
            page_datetime = item.getPage().datetime
            if (
                page_datetime is not None
                and page_datetime.year == now.year
                and page_datetime.month == now.month
                and page_datetime.day == now.day
            ):
                item.setFontColor(nowColor)
                self._markedPages.add(item.getPage().subpath)
