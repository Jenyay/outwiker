#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from .mainid import MainId
from core.system import getImagesDir

class MainToolBar (wx.ToolBar):
	def __init__ (self, parent, id, style):
		wx.ToolBar.__init__(self, parent, id, style=style)

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

		self.AddLabelTool(MainId.ID_SAVE, 
				_("Save"), 
				wx.Bitmap(os.path.join (self.imagesDir, "save.png"), wx.BITMAP_TYPE_ANY), 
				wx.NullBitmap, 
				wx.ITEM_NORMAL, 
				_("Save wiki"), 
				"")

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
