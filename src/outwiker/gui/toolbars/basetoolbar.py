# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

import wx
import wx.aui

from outwiker.core.application import Application
from outwiker.gui.guiconfig import MainWindowConfig


class BaseToolBar (wx.aui.AuiToolBar):
    """
    Базовый класс для панелей инструментов
    """
    __metaclass__ = ABCMeta

    def __init__ (self, parent, auiManager):
        super (BaseToolBar, self).__init__(parent)
        self._SECTION_NAME = MainWindowConfig.MAIN_WINDOW_SECTION

        self._parent = parent
        self._auiManager = auiManager
        self._pane = self._loadPaneInfo()


    def _loadPaneInfo (self):
        try:
            paneinfo = Application.config.get (self._SECTION_NAME, self.name)
            pane = wx.aui.AuiPaneInfo()
            self._auiManager.LoadPaneInfo (paneinfo, pane)
            pane.Caption(self.caption)
            pane.Dock()
        except BaseException:
            pane = self._createPane()

        return pane


    @abstractmethod
    def _createPane (self):
        """
        Абстрактный метод
        Должен вернуть экземпляр класса AuiPaneInfo
        """
        pass


    def savePaneInfo (self):
        config = Application.config
        paneinfo = self._auiManager.SavePaneInfo (self.pane)
        config.set (self._SECTION_NAME, self.name, paneinfo)


    def DeleteTool (self, toolid, fullUpdate=True):
        self.Freeze()
        super (BaseToolBar, self).DeleteTool (toolid)
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
        item = super (BaseToolBar, self).AddTool (tool_id, label, bitmap, short_help_string, kind)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()
            self.updatePaneInfo()
        self.Thaw()
        return item


    @property
    def pane (self):
        return self._pane


    def updatePaneInfo (self):
        currentpane = self._auiManager.GetPane (self)
        self.pane.Position (currentpane.dock_pos).Row (currentpane.dock_row).Direction (currentpane.dock_direction).Layer (currentpane.dock_layer)


    def UpdateToolBar (self):
        self.Realize()
        self._auiManager.DetachPane (self)
        self._auiManager.AddPane(self, self.pane)
        self.updatePaneInfo()


    def FindById (self, toolid):
        return self.FindTool (toolid)


    @abstractproperty
    def caption (self):
        pass


    @abstractproperty
    def name (self):
        return self.pane.name


    def Hide (self):
        self.updatePaneInfo()
        self.pane.Hide()
        super (BaseToolBar, self).Hide()


    def Show (self):
        self.pane.Show()
        super (BaseToolBar, self).Show()


    def Destroy (self):
        self.savePaneInfo()
        super (BaseToolBar, self).Destroy()
