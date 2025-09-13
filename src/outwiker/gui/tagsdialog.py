# -*- coding: utf-8 -*-

import wx

from outwiker.core.tagslist import TagsList
from outwiker.gui.defines import CONTROLS_HGAP, CONTROLS_MARGIN, CONTROLS_VGAP
from outwiker.gui.controls.marginsizer import MarginSizer
from .tagsselector import TagsSelector


class TagsDialog(wx.Dialog):
    def __init__(self, parent, application):
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

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
        self.__tagsLabel = wx.StaticText(self, -1, _("Tags (comma separated)"))
        self.__tagsSelector = TagsSelector(self, enable_active_tags_filter=False)
        self.__tagsSelector.SetMinSize((350, -1))
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        mainSizer = wx.FlexGridSizer(cols=2, vgap=CONTROLS_VGAP, hgap=CONTROLS_HGAP)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(1)

        mainSizer.Add(self.__tagsLabel, flag=wx.ALIGN_CENTER_VERTICAL)
        mainSizer.Add(self.__tagsSelector, flag=wx.EXPAND)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(buttonsSizer, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.TOP | wx.BOTTOM, border=CONTROLS_MARGIN)

        marginSizer = MarginSizer()
        marginSizer.Add(mainSizer)
        self.SetSizerAndFit(marginSizer)

    @property
    def tags(self):
        return self.__tagsSelector.tags

    def setTagsCloudFontSize(self, minFontSize: int, maxFontSize: int):
        self.__tagsSelector.setFontSize(minFontSize, maxFontSize)

    def setTagsCloudMode(self, mode: str):
        self.__tagsSelector.setMode(mode)

    def enableTagsCloudTooltips(self, enable: bool = True):
        self.__tagsSelector.enableTooltips(enable)
