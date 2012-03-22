#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.system import getImagesDir
from outwiker.core.tagscommands import getTagsString, parseTagsList
from .tagscloud import TagsCloud
from .taglabel import EVT_TAG_LEFT_CLICK


class TagsSelector (wx.Panel):
    def __init__ (self, parent):
        super (TagsSelector, self).__init__ (parent)

        self.__ID_TAGS_BUTTON = wx.NewId()
        self.__tagsWidth = 350
        self.__tagsHeight = 150

        self.__tagBitmap = wx.Bitmap (os.path.join (getImagesDir(), "tag.png"), 
                wx.BITMAP_TYPE_PNG)

        self.label_tags = wx.StaticText(self, -1, _(u"Tags (comma separated)"))

        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.tagsTextCtrl.SetMinSize((250, -1))

        self.__tagsCloud = TagsCloud (self)
        self.__tagsCloud.SetMinSize ((self.__tagsWidth, self.__tagsHeight))
        self.__tagsCloud.Bind (EVT_TAG_LEFT_CLICK, self.__onTagClick)

        self.__layout()


    @property
    def tags (self):
        tagsString = self.tagsTextCtrl.GetValue().strip()
        tags = parseTagsList (tagsString)
        return tags


    @tags.setter
    def tags (self, tags):
        tagsString = getTagsString (tags)
        self.tagsTextCtrl.SetValue (tagsString)


    def __layout (self):
        titleTextSizer = wx.FlexGridSizer (1, 2, 0, 0)
        titleTextSizer.AddGrowableCol(1)

        titleTextSizer.Add(self.label_tags, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        titleTextSizer.Add(self.tagsTextCtrl, 0, wx.ALL|wx.EXPAND, 0)

        mainSizer = wx.FlexGridSizer (2, 1, 0, 0)
        mainSizer.Add (titleTextSizer, 0, wx.ALL|wx.EXPAND, 4)
        mainSizer.Add (self.__tagsCloud, 0, wx.ALL|wx.EXPAND, 4)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)

        self.SetSizer(mainSizer)
        self.Layout()


    def __onTagClick (self, event):
        self.__addTagText (event.text)


    def __addTagText (self, tagname):
        currentText = self.tagsTextCtrl.GetValue().strip()

        if len (currentText) == 0:
            newtext = tagname
        elif currentText[-1] == ",":
            newtext = currentText + " " + tagname
        else:
            newtext = currentText + ", " + tagname

        self.tagsTextCtrl.SetValue (newtext)
        self.tagsTextCtrl.SetFocus()
        self.tagsTextCtrl.SetSelection (len (newtext), len (newtext))


    def setTagsList (self, tagsList):
        self.__tagsCloud.setTags (tagsList)
