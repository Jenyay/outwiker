# -*- coding: utf-8 -*-

from configparser import NoSectionError

import wx
import wx.aui


class ToolBar(wx.aui.AuiToolBar):
    """
    The base class for a toolbars.
    """
    def __init__(self, parent, auiManager, config, name, caption):
        super().__init__(parent)
        self._SECTION_NAME = 'Toolbars'

        self._parent = parent
        self._auiManager = auiManager
        self._config = config
        self._name = name
        self._caption = caption
        self._pane = self._loadPaneInfo()

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

    def _createPane(self):
        return (wx.aui.AuiPaneInfo()
                .Name(self.name)
                .Caption(self.caption)
                .ToolbarPane()
                .Top()
                .Position(0)
                .Row(0))

    def _loadPaneInfo(self):
        try:
            paneinfo = self._config.get(self._SECTION_NAME, self.name)
            pane = wx.aui.AuiPaneInfo()
            self._auiManager.LoadPaneInfo(paneinfo, pane)
            pane.Caption(self.caption)
            pane.Dock()
        except (BaseException, NoSectionError):
            pane = self._createPane()

        return pane

    def savePaneInfo(self):
        paneinfo = self._auiManager.SavePaneInfo(self.pane)
        self._config.set(self._SECTION_NAME, self.name, paneinfo)

    def DeleteTool(self, toolid, fullUpdate=True):
        self.Freeze()
        super().DeleteTool(toolid)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()
        self.Thaw()

    def AddTool(self,
                tool_id,
                label,
                bitmap,
                short_help_string=wx.EmptyString,
                kind=wx.ITEM_NORMAL,
                fullUpdate=True):
        self.Freeze()
        item = super().AddTool(tool_id, label, bitmap, short_help_string, kind)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()
            self.updatePaneInfo()

        self.Thaw()
        return item

    @property
    def pane(self):
        return self._pane

    def updatePaneInfo(self):
        currentpane = self._auiManager.GetPane(self)
        (self.pane
         .Position(currentpane.dock_pos)
         .Row(currentpane.dock_row)
         .Direction(currentpane.dock_direction)
         .Layer(currentpane.dock_layer)
         )

    def UpdateToolBar(self):
        self.Realize()
        self._auiManager.DetachPane(self)
        self._auiManager.AddPane(self, self.pane)
        self.updatePaneInfo()

    def FindById(self, toolid):
        return self.FindTool(toolid)

    def Hide(self):
        self.updatePaneInfo()
        self.pane.Hide()
        super().Hide()

    def Show(self):
        self.pane.Show()
        super().Show()

    def Destroy(self):
        self.savePaneInfo()
        super().Destroy()
