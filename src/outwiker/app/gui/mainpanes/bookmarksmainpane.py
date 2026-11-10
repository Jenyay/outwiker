# -*- coding: utf-8 -*-

import wx.aui

from outwiker.app.gui.bookmarkspanel import BookmarksPanel
from outwiker.gui.guiconfig import BookmarksPaneConfig
from outwiker.gui.mainpanes.mainpane import MainPane

class BookmarksMainPane(MainPane):
    def _createPanel(self):
        return BookmarksPanel(self.parent, self.application)

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
                .Layer(0)            # D1
                .Position(1)
                .CloseButton(True)
                .MaximizeButton(False)
                .Bottom()
            )
        pane.BestSize((self.config.width.value, self.config.height.value))
        return pane

    def __init__(self, parent, auiManager, application):
        super().__init__(parent, auiManager, application)
        self.pane.Hide()

    def show(self):
        assert self.panel is not None
        self.panel.Show()
        super().show()

    def close(self):
        # self.panel._unbindAppEvents()
        super().close()
