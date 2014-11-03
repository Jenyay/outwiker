# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.system import getImagesDir
from outwiker.gui.iconlistctrl import IconListCtrl


class IconsetPanel (wx.Panel):
    def __init__ (self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        super (IconsetPanel, self).__init__ (*args, **kwds)

        self.ADD_GROUP = wx.NewId()
        self.REMOVE_GROUP = wx.NewId()
        self.RENAME_GROUP = wx.NewId()

        self.ADD_ICONS = wx.NewId()
        self.REMOVE_ICONS = wx.NewId()
        self.SET_COVER = wx.NewId()

        self.__createGuiElements()


    def __fillGroupsToolbar (self):
        imagesDir = getImagesDir()

        self._groupsToolbar.AddLabelTool(
            self.ADD_GROUP,
            _(u"Add new group"),
            wx.Bitmap(os.path.join (imagesDir, "add.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Add new group"),
            "")

        self._groupsToolbar.AddLabelTool(
            self.REMOVE_GROUP,
            _(u"Remove group"),
            wx.Bitmap(os.path.join (imagesDir, "remove.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Remove group"),
            "")

        self._groupsToolbar.AddLabelTool(
            self.RENAME_GROUP,
            _(u"Rename group"),
            wx.Bitmap(os.path.join (imagesDir, "pencil.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Rename group"),
            "")


    def __fillIconsToolbar (self):
        imagesDir = getImagesDir()

        self._iconsToolbar.AddLabelTool(
            self.ADD_ICONS,
            _(u"Add icons"),
            wx.Bitmap(os.path.join (imagesDir, "add.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Add icons"),
            "")

        self._iconsToolbar.AddLabelTool(
            self.REMOVE_ICONS,
            _(u"Remove selected icons"),
            wx.Bitmap(os.path.join (imagesDir, "remove.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Remove selected icons"),
            "")

        self._iconsToolbar.AddLabelTool(
            self.SET_COVER,
            _(u"Set icon as group's cover"),
            wx.Bitmap(os.path.join (imagesDir, "picture.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Set icon as group's cover"),
            "")


    def __createGuiElements (self):
        mainSizer = wx.FlexGridSizer (cols=2, rows=1)
        mainSizer.AddGrowableCol (1)
        mainSizer.AddGrowableRow (0)

        #
        # Controls for groups
        groupsSizer = wx.FlexGridSizer (cols=1)
        groupsSizer.AddGrowableCol (0)
        groupsSizer.AddGrowableRow (0)

        self._groups = wx.TreeCtrl (
            self,
            style = wx.TR_EDIT_LABELS | wx.TR_LINES_AT_ROOT | wx.TR_SINGLE | wx.SUNKEN_BORDER)
        self._groups.SetMinSize ((200, -1))

        # Toolbar for groups
        self._groupsToolbar = wx.ToolBar (
            self,
            -1,
            style = wx.TB_HORIZONTAL | wx.TB_FLAT)

        self.__fillGroupsToolbar()

        groupsSizer.Add (self._groups, 1, wx.RIGHT | wx.EXPAND, border = 2)
        groupsSizer.Add (self._groupsToolbar, 1, wx.RIGHT | wx.EXPAND, border = 2)

        #
        # Controls for icons in the group
        iconsSizer = wx.FlexGridSizer (cols=1)
        iconsSizer.AddGrowableRow (0)
        iconsSizer.AddGrowableCol (0)

        self._iconsList = IconListCtrl (self)

        # Toolbar for icons in the group
        self._iconsToolbar = wx.ToolBar (
            self,
            -1,
            style = wx.TB_HORIZONTAL | wx.TB_FLAT)

        self.__fillIconsToolbar()
        iconsSizer.Add (self._iconsList, 1, wx.LEFT | wx.EXPAND, border = 2)
        iconsSizer.Add (self._iconsToolbar, 1, wx.LEFT | wx.EXPAND, border = 2)

        # Main sizer
        mainSizer.Add (groupsSizer, 1, wx.ALL | wx.EXPAND, border = 0)
        mainSizer.Add (iconsSizer, 1, wx.ALL | wx.EXPAND, border = 0)

        self.SetSizer (mainSizer)
        self.Layout()


    def Save (self):
        pass


    def LoadState (self):
        pass
