# -*- coding: utf-8 -*-

import wx

from outwiker.core.tagslist import TagsList
from .tagsselector import TagsSelector


class TagsDialog(wx.Dialog):
    def __init__(self, parent, application):
        super(TagsDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.__application = application

        self.__createControls()
        self.__setTagsList()
        self.__tagsSelector.SetFocus()
        self.Center(wx.BOTH)

    def __setTagsList(self):
        assert self.__application.wikiroot is not None

        tagslist = TagsList(self.__application.wikiroot)
        self.__tagsSelector.setTagsList(tagslist)

    def __createControls(self):
        self.__tagsSelector = TagsSelector(self, enable_active_tags_filter=False)
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        mainSizer.Add(self.__tagsSelector,
                      flag=wx.EXPAND | wx.ALL,
                      border=2)
        mainSizer.Add(buttonsSizer,
                      flag=wx.ALIGN_RIGHT | wx.ALL,
                      border=2)

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()

    @property
    def tags(self):
        return self.__tagsSelector.tags

    def setTagsCloudFontSize(self, minFontSize: int, maxFontSize: int):
        self.__tagsSelector.setFontSize(minFontSize, maxFontSize)

    def setTagsCloudMode(self, mode: str):
        self.__tagsSelector.setMode(mode)

    def enableTagsCloudTooltips(self, enable: bool = True):
        self.__tagsSelector.enableTooltips(enable)
