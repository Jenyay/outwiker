#!/usr/bin/env python
#-*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import wx
import wx.aui


class BaseToolBar (wx.aui.AuiToolBar):
    """
    Базовый класс для панелей инструментов
    """
    __metaclass__ = ABCMeta

    def __init__ (self, parent, auiManager):
        super (BaseToolBar, self).__init__(parent)

        self._parent = parent
        self._auiManager = auiManager
        self._pane = self._createPane()


    @abstractmethod
    def _createPane (self):
        """
        Абстрактный метод
        Должен вернуть экземпляр класса AuiPaneInfo
        """
        pass


    def DeleteTool (self, toolid, fullUpdate=True):
        super (BaseToolBar, self).DeleteTool (toolid)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()


    def AddTool(self, 
            tool_id, 
            label, 
            bitmap, 
            short_help_string=wx.EmptyString, 
            kind=wx.ITEM_NORMAL,
            fullUpdate=True):
        super (BaseToolBar, self).AddTool (tool_id, label, bitmap, short_help_string, kind)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()


    def UpdateToolBar (self):
        self.Realize()
        self._auiManager.DetachPane (self)
        self._auiManager.AddPane(self, self._pane)


    def FindById (self, toolid):
        return self.FindTool (toolid)


    @property
    def caption (self):
        return self._pane.caption


    @property
    def name (self):
        return self._pane.name


    def Hide (self):
        self._pane.Hide()
        super (BaseToolBar, self).Hide()


    def Show (self):
        self._pane.Show()
        super (BaseToolBar, self).Show()
