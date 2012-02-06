#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.system import getImagesDir
from outwiker.core.application import Application
from outwiker.core.tagslist import TagsList
from outwiker.core.tagscommands import getTagsString, parseTagsList
from .tagspopup import TagsPopup
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

        self.tagsButton = wx.BitmapButton (self, 
                self.__ID_TAGS_BUTTON, 
                self.__tagBitmap)

        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.tagsTextCtrl.SetMinSize((250, -1))

        self.__tagsCloud = TagsPopup (self)
        self.__tagsCloud.SetSize ((self.__tagsWidth, self.__tagsHeight))
        self.__tagsCloud.Bind (EVT_TAG_LEFT_CLICK, self.__onTagClick)

        self.Bind(wx.EVT_BUTTON, self.__onShowTags, id=self.__ID_TAGS_BUTTON)

        self.__layout()
        self.__fillTagsList()


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
        tagsSizer = wx.FlexGridSizer(1, 3, 0, 0)
        tagsSizer.Add(self.label_tags, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        tagsSizer.Add(self.tagsTextCtrl, 0, wx.ALL|wx.EXPAND, 0)
        tagsSizer.Add(self.tagsButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 4)
        tagsSizer.AddGrowableCol(1)

        self.SetSizer(tagsSizer)
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


    def __fillTagsList (self):
        assert Application.wikiroot != None

        tagslist = TagsList (Application.wikiroot)
        self.__tagsCloud.setTags (tagslist)


    def __onShowTags (self, event):
        if self.__tagsCloud.IsShown():
            self.__tagsCloud.Hide()
        else:
            (buttonx, buttony) = self.tagsButton.GetPositionTuple()
            (buttonw, buttonh) = self.tagsButton.GetSizeTuple()

            (screenx, screeny) = self.ClientToScreenXY (buttonx + buttonw - self.__tagsWidth,
                    buttony + buttonh)

            self.__tagsCloud.SetPosition ((screenx, screeny))

            self.__tagsCloud.Popup()
