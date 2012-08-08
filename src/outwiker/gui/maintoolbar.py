#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.aui

from .mainid import MainId
from outwiker.core.system import getImagesDir


class MainToolBar (wx.aui.AuiToolBar):
    def __init__ (self, parent, auiManager):
        super (MainToolBar, self).__init__(parent)

        self._parent = parent
        self._auiManager = auiManager

        self._pane = wx.aui.AuiPaneInfo().Name("generalToolBar").Caption("General").ToolbarPane().Top()

        self.imagesDir = getImagesDir()

        self.AddTool(MainId.ID_NEW, 
                _(u"New…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Create new wiki…"),
                fullUpdate=False)

        self.AddTool(MainId.ID_OPEN, 
                _(u"Open…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Open wiki…"),
                fullUpdate=False)

        self.AddTool(MainId.ID_RELOAD, 
                _("Reload"), 
                wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), 
                _("Reload wiki"),
                fullUpdate=False)

        self.AddSeparator()

        self.AddTool(MainId.ID_ATTACH, 
                _(u"Attach files…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Attach files…"),
                fullUpdate=False)

        self.AddTool(MainId.ID_GLOBAL_SEARCH, 
                _(u"Global search…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Global search…"),
                fullUpdate=False)

        self.AddSeparator()
        self.Realize()

        self._auiManager.AddPane(self, self._pane)


    def AddLabelTool (self, toolid, label, bitmap, bmpDisabled, kind, shortHelp, longHelp):
        """
        Метод добавлен для совместимости со старыми плагинами. 
        """
        self.AddTool (toolid, label, bitmap, shortHelp, kind)


    def AddCheckTool(self, 
            toolid, 
            bitmap, 
            bmpDisabled, 
            shortHelp, 
            longHelp="",
            fullUpdate=True):
        self.AddTool (toolid, shortHelp, bitmap, shortHelp, wx.ITEM_CHECK, fullUpdate)


    def DeleteTool (self, toolid, fullUpdate=True):
        super (MainToolBar, self).DeleteTool (toolid)
        self.UpdateToolBar()
        if fullUpdate:
            self.UpdateAuiManager()


    def AddTool(self, 
            tool_id, 
            label, 
            bitmap, 
            short_help_string=wx.EmptyString, 
            kind=wx.ITEM_NORMAL,
            fullUpdate=True):
        super (MainToolBar, self).AddTool (tool_id, label, bitmap, short_help_string, kind)
        self.UpdateToolBar()
        if fullUpdate:
            self.UpdateAuiManager()


    def UpdateToolBar (self):
        self.Realize()
        self._auiManager.DetachPane (self)
        self._auiManager.AddPane(self, self._pane)


    def UpdateAuiManager (self):
        self._auiManager.Update()


    def FindById (self, toolid):
        return self.FindTool (toolid)


