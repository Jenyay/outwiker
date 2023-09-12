# -*- coding: utf-8 -*-

import wx
from wx.lib.newevent import NewEvent

from outwiker.core.tagscommands import getTagsString, parseTagsList
from outwiker.gui.tagscloud import TagsCloud
from outwiker.gui.controls.taglabel2 import EVT_TAG_LEFT_CLICK


TagsListChangedEvent, EVT_TAGS_LIST_CHANGED = NewEvent()


class TagsSelector(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self._tagsWidth = 350
        self._tagsHeight = 150
        self._current_tags = set()

        self.label_tags = wx.StaticText(self, -1, _("Tags (comma separated)"))

        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.tagsTextCtrl.SetMinSize((250, -1))

        self._tagsCloud = TagsCloud(self, use_buttons=False)
        self._tagsCloud.SetMinSize((self._tagsWidth, self._tagsHeight))
        self._tagsCloud.Bind(EVT_TAG_LEFT_CLICK, self._onTagClick)
        self.tagsTextCtrl.Bind(wx.EVT_TEXT, handler=self._onTagsChanged)

        self._layout()

    @property
    def tags(self):
        tagsString = self.tagsTextCtrl.GetValue().strip().lower()
        tags = parseTagsList(tagsString)
        return tags

    @tags.setter
    def tags(self, tags):
        tagsString = getTagsString(tags)
        self.tagsTextCtrl.SetValue(tagsString)

    def setFontSize(self, min_font_size: int, max_font_size: int):
        self._tagsCloud.setFontSize(min_font_size, max_font_size)

    def setMode(self, mode:str):
        self._tagsCloud.setMode(mode)

    def enableTooltips(self, enable: bool = True):
        self._tagsCloud.enableTooltips(enable)

    def _layout(self):
        titleTextSizer = wx.FlexGridSizer(1, 2, 0, 0)
        titleTextSizer.AddGrowableCol(1)

        titleTextSizer.Add(self.label_tags, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        titleTextSizer.Add(self.tagsTextCtrl, 0, wx.ALL | wx.EXPAND, 0)

        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.Add(titleTextSizer, 0, wx.ALL | wx.EXPAND, 4)
        mainSizer.Add(self._tagsCloud, 0, wx.ALL | wx.EXPAND, 4)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)

        self.SetSizer(mainSizer)
        self.Layout()

    def _onTagClick(self, event):
        tag_name = event.text
        if tag_name not in self.tags:
            self._addTagText(tag_name)
        else:
            self._removeTagText(tag_name)

    def _addTagText(self, tagname):
        currentText = self.tagsTextCtrl.GetValue().strip()

        if len(currentText) == 0:
            newtext = tagname
        elif currentText[-1] == ",":
            newtext = currentText + " " + tagname
        else:
            newtext = currentText + ", " + tagname

        self.tagsTextCtrl.SetValue(newtext)
        self.tagsTextCtrl.SetFocus()
        self.tagsTextCtrl.SetSelection(len(newtext), len(newtext))

    def _removeTagText(self, tag_name):
        tags_list = self.tags[:]
        if tag_name in tags_list:
            tags_list.remove(tag_name)
            text = ", ".join(tags_list)
            self.tagsTextCtrl.SetValue(text)
            pos = len(text)
            self.tagsTextCtrl.SetSelection(pos, pos)

    def setTagsList(self, tagsList):
        self._tagsCloud.setTags(tagsList)
        self._updateTagsMark()

    def _sendTagsListChangedEvent(self):
        propagationLevel = 10
        newevent = TagsListChangedEvent(tags=self.tags)
        newevent.ResumePropagation(propagationLevel)
        wx.PostEvent(self, newevent)

    def _onTagsChanged(self, _event):
        self._updateTagsMark()
        self._sendTagsListChangedEvent()

    def _updateTagsMark(self):
        new_current_tags = set(self.tags)
        new_tags = new_current_tags - self._current_tags
        removed_tags = self._current_tags - new_current_tags

        for tag_name in new_tags:
            self._tagsCloud.mark(tag_name)

        for tag_name in removed_tags:
            self._tagsCloud.mark(tag_name, False)

        self._current_tags = new_current_tags
