# -*- coding: utf-8 -*-

import wx

from .tagscloud import TagsCloud
from .pagelistpopup import PageListPopup
from .tagspanelcontroller import TagsPanelController


class TagsCloudPanel(wx.Panel):
    def __init__(self, parent, application):
        wx.Panel.__init__(self, parent)
        self.__application = application
        self.__tagscloud = TagsCloud(self)

        self.__popupWidth = 300
        self.__popupHeight = 200

        self.__layout()

        self.__controller = TagsPanelController(self, application)

    def showPopup(self, pages):
        pageListPopup = PageListPopup(self.__application.mainWindow)
        pageListPopup.SetSize((self.__popupWidth, self.__popupHeight))
        pageListPopup.setPageList(pages)
        pageListPopup.Popup()

    def clearTags(self):
        self.__tagscloud.clear()

    def clearMarks(self):
        self.__tagscloud.clearMarks()

    def mark(self, tag, marked=True):
        self.__tagscloud.mark(tag, marked)

    def setTags(self, tags):
        self.__tagscloud.setTags(tags)

    def updateTagLabels(self):
        self.__tagscloud.updateTagLabels()

    def __layout(self):
        mainSizer = wx.FlexGridSizer(1, 1, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(self.__tagscloud, 0, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(mainSizer)
