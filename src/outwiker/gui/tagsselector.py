# -*- coding: utf-8 -*-

from typing import List

import wx
from wx.lib.newevent import NewEvent

from outwiker.core.system import getBuiltinImagePath
from outwiker.core.tagscommands import getTagsString, parseTagsList
from outwiker.core.tagslist import TagsList
from outwiker.gui.tagscloud import TagsCloud
from outwiker.gui.controls.taglabel2 import EVT_TAG_LEFT_DOWN



TagsListChangedEvent, EVT_TAGS_LIST_CHANGED = NewEvent()


class TagsAutocompleter(wx.TextCompleterSimple):
    def __init__(self, tagsList: TagsList):
        super().__init__()
        self._tags = sorted(tagsList.tags)

    def GetCompletions(self, prefix: str) -> List[str]:
        prefix_src = prefix
        pos_comma = prefix.rfind(",")

        # start of tag
        prefix_last_tag = prefix[pos_comma + 1 :] if pos_comma >= 0 else prefix
        prefix_last_tag_strip = prefix_last_tag.strip().lower()
        if prefix_last_tag.strip() == "":
            return []

        # Leading spaces in prefix
        space_count = len(prefix_last_tag) - len(prefix_last_tag.lstrip())

        # Begin of the full entered text
        begin = prefix_src[: pos_comma + 1] if pos_comma >= 0 else ""

        # List of autocomplete samples
        result = [
            f"{begin}{' ' * space_count}{tag}"
            for tag in self._tags
            if tag.startswith(prefix_last_tag_strip) and tag != prefix_last_tag_strip
        ]
        return result


class TagsSelector(wx.Panel):
    def __init__(self, parent, enable_active_tags_filter: bool = True):
        super().__init__(parent)

        self._tagsWidth = 350
        self._tagsHeight = 150
        self._current_tags = set()

        self.label_tags = wx.StaticText(self, -1, _("Tags (comma separated)"))

        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.tagsTextCtrl.SetMinSize((250, -1))

        tagBitmap = wx.Bitmap(getBuiltinImagePath("tag.png"))
        self.tagsButton = wx.BitmapButton(self, bitmap=tagBitmap)

        self._tagsCloud = TagsCloud(
            self, use_buttons=False, enable_active_tags_filter=enable_active_tags_filter
        )
        self._tagsCloud.SetMinSize((self._tagsWidth, self._tagsHeight))
        self._tagsCloud.Bind(EVT_TAG_LEFT_DOWN, self._onTagClick)
        self.tagsTextCtrl.Bind(wx.EVT_TEXT, handler=self._onTagsChanged)

        self._layout()

    @property
    def tags(self) -> List[str]:
        tagsString = self.tagsTextCtrl.GetValue().strip().lower()
        tags = parseTagsList(tagsString)
        return tags

    @tags.setter
    def tags(self, tags: List[str]):
        tagsString = getTagsString(tags)
        self.tagsTextCtrl.SetValue(tagsString)

    def setFontSize(self, min_font_size: int, max_font_size: int):
        self._tagsCloud.setFontSize(min_font_size, max_font_size)

    def setMode(self, mode: str):
        self._tagsCloud.setMode(mode)

    def enableTooltips(self, enable: bool = True):
        self._tagsCloud.enableTooltips(enable)

    def _layout(self):
        titleTextSizer = wx.FlexGridSizer(cols=3)
        titleTextSizer.AddGrowableCol(1)
        titleTextSizer.AddGrowableRow(0)

        titleTextSizer.Add(
            self.label_tags, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4
        )
        titleTextSizer.Add(self.tagsTextCtrl, flag=wx.ALL | wx.EXPAND, border=0)
        titleTextSizer.Add(self.tagsButton, flag=wx.ALIGN_RIGHT)

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)
        mainSizer.Add(titleTextSizer, flag=wx.ALL | wx.EXPAND, border=4)
        mainSizer.Add(self._tagsCloud, flag=wx.ALL | wx.EXPAND, border=4)

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

    def setTagsList(self, tagsList: TagsList):
        # self.tagsTextCtrl.AutoComplete(sorted(tagsList.tags))
        self.tagsTextCtrl.AutoComplete(TagsAutocompleter(tagsList))
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

        self._tagsCloud.mark_list(new_tags)
        self._tagsCloud.mark_list(removed_tags, False)

        self._current_tags = new_current_tags
