#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .tagscloud import TagsCloud, EVT_TAG_CLICK
from .pagelist import EVT_PAGE_CLICK
from .pagelistpopup import PageListPopup
from outwiker.core.tagslist import TagsList
from outwiker.core.tree import RootWikiPage


class TagsCloudPanel (wx.Panel):
    def __init__ (self, parent, application):
        wx.Panel.__init__ (self, parent)

        self.__application = application

        self.__currentTags = None
        self.__tagscloud = TagsCloud (self)
        self.__tagscloud.Bind (EVT_TAG_CLICK, self.__onTagClick)

        self.__popupWidth = 300
        self.__popupHeight = 200
        self.__pageListPopup = PageListPopup (self)
        self.__pageListPopup.SetSize ((self.__popupWidth, self.__popupHeight))

        self.__layout()
        self.__bindAppEvents()

        self.Bind (EVT_PAGE_CLICK, self.__onPageClick)


    def __onPageClick (self, event):
        assert event.page != None
        self.__application.selectedPage = event.page


    def __onTagClick (self, event):
        pages = self.__currentTags[event.text][:]
        pages.sort (RootWikiPage.sortAlphabeticalFunction)
        self.__pageListPopup.setPageList (pages)
        self.__pageListPopup.Popup()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (1, 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)
        mainSizer.Add (self.__tagscloud, 0, wx.ALL | wx.EXPAND, 4)
        self.SetSizer (mainSizer)


    def __bindAppEvents (self):
        self.__application.onPageUpdate += self.__onPageUpdate
        self.__application.onTreeUpdate += self.__onTreeUpdate
        self.__application.onEndTreeUpdate += self.__onEndTreeUpdate

    
    def __unbindAppEvents (self):
        self.__application.onPageUpdate -= self.__onPageUpdate
        self.__application.onTreeUpdate -= self.__onTreeUpdate
        self.__application.onEndTreeUpdate -= self.__onEndTreeUpdate


    def __onTreeUpdate (self, sender):
        self.__update()


    def __onEndTreeUpdate (self, root):
        self.__update()


    def __onPageUpdate (self, sender):
        self.__update()


    def __isEqual (self, taglist1, taglist2):
        """
        Возвращает True, если списки тегов одинаковые, и False в противном случае
        """
        if taglist1 == None or taglist2 == None:
            return False

        keys1 = taglist1.tags
        keys2 = taglist2.tags

        if keys1 != keys2:
            return False

        for key in keys1:
            if len (taglist2[key]) != len (taglist1[key]):
                return False

        return True


    def __update (self):
        if self.__application.wikiroot == None:
            self.__tagscloud.clear()
            return

        tags = TagsList (self.__application.wikiroot)

        if not self.__isEqual (tags, self.__currentTags):
            self.__tagscloud.setTags (tags)
            self.__currentTags = tags
