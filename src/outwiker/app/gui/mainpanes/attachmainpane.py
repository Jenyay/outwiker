# -*- coding: utf-8 -*-

import wx.aui

from outwiker.gui.attachpanel import AttachPanel
from outwiker.gui.guiconfig import AttachConfig
from outwiker.gui.mainpanes.mainpane import MainPane


class AttachMainPane(MainPane):
    def __init__(self, parent, auiManager, application):
        super().__init__(parent, auiManager, application)
        self._bindAppEvents()

    def _bindAppEvents(self):
        self._application.onPageSelect += self._onPageSelect
        self._application.onAttachListChanged += self._onAttachListChanged
        self._application.onAttachSubdirChanged += self._onAttachSubdirChanged
        self._application.onWikiOpen += self._onWikiOpen

    def _unbindAppEvents(self):
        self._application.onPageSelect -= self._onPageSelect
        self._application.onAttachListChanged -= self._onAttachListChanged
        self._application.onAttachSubdirChanged -= self._onAttachSubdirChanged
        self._application.onWikiOpen -= self._onWikiOpen

    def _createPanel(self):
        return AttachPanel(self.parent, self.application)

    def _createConfig(self):
        return AttachConfig(self.application.config)

    def close(self):
        super().close()
        self._unbindAppEvents()

    @property
    def caption(self):
        page = self._application.selectedPage
        title = _('Attachments')
        if page is None:
            return title

        subdir = page.currentAttachSubdir
        if not subdir:
            return title

        caption = '{title} [{subdir}]'.format(title = title, subdir=subdir)
        return caption

    def _createPane(self):
        pane = self._loadPaneInfo(self.config.pane)

        if pane is None:
            pane = self._getPaneDefault()

        pane.Dock()
        pane.CloseButton()
        pane.Caption(self.caption)

        return pane

    def _getPaneDefault(self):
        pane = wx.aui.AuiPaneInfo().Name("attachesPane").Caption(self.caption).Gripper(False).CaptionVisible(
            True).Layer(0).Position(0).CloseButton(True).MaximizeButton(False).Bottom().Dock()

        return pane

    def _updateCaption(self):
        new_caption = self.caption
        if self.pane.caption != new_caption:
            self.pane.Caption(new_caption)
            self._auiManager.Update()

    def _onPageSelect(self, _page):
        self._updateCaption()

    def _onAttachListChanged(self, page, _params):
        self._updateCaption()

    def _onAttachSubdirChanged(self, page, _params):
        self._updateCaption()

    def _onWikiOpen(self, _wiki):
        self._updateCaption()
