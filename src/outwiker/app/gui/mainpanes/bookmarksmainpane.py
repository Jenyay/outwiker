# -*- coding: utf-8 -*-

import wx.aui

from outwiker.app.gui.bookmarkspanel import BookmarksPanel
from outwiker.gui.guiconfig import BookmarksPaneConfig
from outwiker.gui.mainpanes.mainpane import MainPane
from outwiker.core.events import BookmarksChangedParams

class BookmarksMainPane(MainPane):
    def _createPanel(self):
        panel = BookmarksPanel(self.parent, self.application)
        self.application.onBookmarksChanged += self._onBookmarksChanged
        panel.move_up_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveUp)
        panel.move_down_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveDown)
        panel.remove_btn.Bind(wx.EVT_BUTTON, handler=self._onRemoveBookmark)
        return panel

    def _createConfig(self):
        return BookmarksPaneConfig(self.application.config)

    @property
    def caption(self):
        return _("Bookmarks")

    def _createPane(self):
        pane = self._loadPaneInfo(self.config.pane)
        if pane is None:
            pane = (
                wx.aui.AuiPaneInfo()
                .Name("bookmarksPane")
                .Caption(self.caption)
                .Gripper(False)
                .CaptionVisible(True)
                .Layer(0)
                .Position(1)
                .CloseButton(True)
                .MaximizeButton(False)
                .Bottom()
            )
        pane.BestSize((self.config.width.value, self.config.height.value))
        return pane

    def __init__(self, parent, auiManager, application):
        super().__init__(parent, auiManager, application)

    def show(self):
        assert self.panel is not None
        self.panel.create_gui_part_2()
        self._update_bookmark_list()
        super().show()

    def close(self):
        self.application.onBookmarksChanged -= self._onBookmarksChanged
        self.panel.move_up_btn.Unbind(wx.EVT_BUTTON, handler=self._onMoveUp)
        self.panel.move_down_btn.Unbind(wx.EVT_BUTTON, handler=self._onMoveDown)
        self.panel.remove_btn.Unbind(wx.EVT_BUTTON, handler=self._onRemoveBookmark)
        super().close()
        wx.SafeYield()

    def _update_bookmark_list(self):
        if self.panel.bookmark_list is not None:
            pages = [page for page in self._application.bookmarks if page is not None]
            old_selection = self.panel.bookmark_list.getSelectedIndex()
            self.panel.bookmark_list.setPageList(pages)

            # Update selection
            if old_selection is None:
                old_selection = 0

            if old_selection >= len(pages):
                old_selection = len(pages) - 1

            if old_selection >= 0:
                self.panel.bookmark_list.setSelected(old_selection)

    def _onMoveUp(self, event):
        assert self.panel.bookmark_list is not None
        self.panel.bookmark_list.moveSelectedItemUp()
        self._set_bookmark_list()

    def _onMoveDown(self, event):
        assert self.panel.bookmark_list is not None
        self.panel.bookmark_list.moveSelectedItemDown()
        self._set_bookmark_list()

    def _onRemoveBookmark(self, event):
        assert self.panel.bookmark_list is not None
        selected_page = self.panel.bookmark_list.getSelectedPage()
        if selected_page is not None:
            sel_index = self.panel.bookmark_list.getSelectedIndex()
            self._application.bookmarks.remove(selected_page)

            # Update selection
            pages = self.panel.bookmark_list.getPageList()
            if sel_index >= len(pages):
                sel_index = len(pages) - 1

            if sel_index >= 0:
                self.panel.bookmark_list.setSelected(sel_index)

    def _set_bookmark_list(self):
        assert self.panel.bookmark_list is not None
        pages = self.panel.bookmark_list.getPageList()

        self._application.onBookmarksChanged -= self._onBookmarksChanged
        self._application.bookmarks.setBookmarks(pages)
        self._application.onBookmarksChanged += self._onBookmarksChanged

    def _onBookmarksChanged(self, params: BookmarksChangedParams):
        self._update_bookmark_list()
