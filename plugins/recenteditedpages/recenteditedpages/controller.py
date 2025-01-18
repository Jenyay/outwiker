# -*- coding: utf-8 -*-
import os.path
from datetime import datetime
from typing import List, Set

import wx

from outwiker.api.core.events import (
    NotesTreeItemsPreparingParams,
    ForceNotesTreeItemsUpdate,
)
from outwiker.api.gui.controls import NotesTreeItem
from outwiker.api.gui.defines import PREF_PANEL_PLUGINS

from .i18n import get_
from .defines import IMAGES_DIR
from .preferencepanel import PreferencePanel
from .config import RecentPagesConfig

class Controller:
    def __init__(self, plugin, application):
        """ """
        self._plugin = plugin
        self._application = application

        # Set of marked subpaths of pages
        self._markedPages: Set[str] = set()
        self._EXTRA_ICON_RECENT = "recent"
        self._extraIconFile = os.path.join(self._plugin.pluginPath, IMAGES_DIR, "recent.svg")

    def initialize(self):
        global _
        _ = get_()

        self._application.onNotesTreeItemsPreparing += self._onNotesTreeItemsPreparing
        self._application.onPageUpdate += self._onPageUpdate
        self._application.onAttachListChanged += self._onAttachListChanged
        self._application.onTreeUpdate += self._onTreeUpdate
        self._application.onPreferencesDialogCreate += self._onPreferencesDialogCreate

    def destroy(self):
        """
        Run on plugin deactivation
        """
        self._application.onNotesTreeItemsPreparing -= self._onNotesTreeItemsPreparing
        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onAttachListChanged -= self._onAttachListChanged
        self._application.onTreeUpdate -= self._onTreeUpdate
        self._application.onPreferencesDialogCreate -= self._onPreferencesDialogCreate

    def _get_image_full_path(self, fname):
        return os.path.join(self._plugin.pluginPath, "images", fname)

    def _onPreferencesDialogCreate(self, dialog):
        prefPanel = PreferencePanel(dialog.treeBook, self._application.config)
        dialog.addPage(
            prefPanel,
            _("RecentEditedPages"),
            parent_page_tag=PREF_PANEL_PLUGINS,
            icon_fname=self._get_image_full_path("recent.svg"),
        )

    def _onTreeUpdate(self, sender):
        self._markedPages.clear()

    def _onAttachListChanged(self, page, params):
        self._pageUpated(page)

    def _onPageUpdate(self, page, change):
        self._pageUpated(page)

    def _pageUpated(self, page):
        if page.subpath not in self._markedPages:
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
        config = RecentPagesConfig(self._application.config)
        colorize = config.colorizePage.value
        addExtraIcon = config.addExtraIcon.value
        if not colorize and not addExtraIcon:
            return

        nowColor = wx.Colour(config.highlightColor.value)
        now = datetime.now()
        for item in items:
            page_datetime = item.getPage().datetime
            if (
                page_datetime is not None
                and page_datetime.year == now.year
                and page_datetime.month == now.month
                and page_datetime.day == now.day
            ):
                self._markedPages.add(item.getPage().subpath)

                if colorize:
                    item.setFontColor(nowColor)

                if addExtraIcon:
                    item.addExtraIcon(self._EXTRA_ICON_RECENT, self._extraIconFile)
