#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.aui

from .mainid import MainId
from outwiker.core.system import getImagesDir


class MainToolBar (wx.aui.AuiToolBar):
    def __init__ (self, parent, auiManager):
        wx.aui.AuiToolBar.__init__(self, parent)

        self._parent = parent
        self._auiManager = auiManager

        self._pane = wx.aui.AuiPaneInfo().Name("generalToolBar").Caption("General Toolbar").ToolbarPane().Top()

        self.imagesDir = getImagesDir()

        self.AddLabelTool(MainId.ID_NEW, 
                _(u"New…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), 
                wx.NullBitmap, 
                wx.ITEM_NORMAL, 
                _(u"Create new wiki…"), u"")

        self.AddLabelTool(MainId.ID_OPEN, 
                _(u"Open…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), 
                wx.NullBitmap, 
                wx.ITEM_NORMAL, 
                _(u"Open wiki…"), 
                "")

        #self.AddLabelTool(MainId.ID_SAVE, 
        #        _("Save"), 
        #        wx.Bitmap(os.path.join (self.imagesDir, "save.png"), wx.BITMAP_TYPE_ANY), 
        #        wx.NullBitmap, 
        #        wx.ITEM_NORMAL, 
        #        _("Save wiki"), 
        #        "")

        self.AddLabelTool(MainId.ID_RELOAD, 
                _("Reload"), 
                wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), 
                wx.NullBitmap, 
                wx.ITEM_NORMAL, 
                _("Reload wiki"), 
                "")

        self.AddSeparator()

        self.AddLabelTool(MainId.ID_ATTACH, 
                _(u"Attach files…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), 
                wx.NullBitmap, 
                wx.ITEM_NORMAL, 
                _(u"Attach files…"), "")

        self.AddLabelTool(MainId.ID_GLOBAL_SEARCH, 
                _(u"Global search…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), 
                wx.NullBitmap, 
                wx.ITEM_NORMAL, 
                _(u"Global search…"), 
                "")

        self.AddSeparator()
        self.Realize()


        self._auiManager.AddPane(self, self._pane)


    def AddLabelTool (self, toolid, label, bitmap, bmpDisabled, kind, shortHelp, longHelp):
        """
        Метод добавлен для совместимости с плагинами. 
        """
        self.AddTool (toolid, label, bitmap, shortHelp, kind)
        self._auiManager.DetachPane (self)
        self._auiManager.AddPane(self, self._pane)
        self.Realize()
        # self._auiManager.Update()


    def AddCheckTool(self, toolid, bitmap, bmpDisabled, shortHelp, longHelp=""):
        self.AddTool (toolid, shortHelp, bitmap, shortHelp, wx.ITEM_CHECK)


    def FindById (self, toolid):
        return self.FindTool (toolid)
