#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .pagelist import EVT_PAGE_CLICK
from .taglabel import EVT_TAG_LEFT_CLICK, EVT_TAG_MIDDLE_CLICK

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import RootWikiPage
from outwiker.core.tagscommands import removeTag, appendTag
from outwiker.core.sortfunctions import sortAlphabeticalFunction


class TagsPanelController (object):
    def __init__ (self, tagsPanel, application):
        self.__tagsPanel = tagsPanel
        self.__application = application
        self.__currentTags = None

        self.__bindAppEvents()
        self.__tagsPanel.Bind (EVT_PAGE_CLICK, self.__onPageClick)
        self.__tagsPanel.Bind (EVT_TAG_LEFT_CLICK, self.__onTagLeftClick)
        self.__tagsPanel.Bind (EVT_TAG_MIDDLE_CLICK, self.__onTagMiddleClick)
        self.__tagsPanel.Bind (wx.EVT_CLOSE, self.__onClose)

        self.__application.onStartTreeUpdate += self.__onStartUpdate
        self.__application.onEndTreeUpdate += self.__onEndUpdate
        self.__application.onPageSelect += self.__onPageSelect

        self.updateTags()


    def __onClose (self, event):
        self.__tagsPanel.Unbind (EVT_PAGE_CLICK, handler=self.__onPageClick)
        self.__tagsPanel.Unbind (EVT_TAG_LEFT_CLICK, handler=self.__onTagLeftClick)
        self.__tagsPanel.Unbind (EVT_TAG_MIDDLE_CLICK, handler=self.__onTagMiddleClick)
        self.__tagsPanel.Unbind (wx.EVT_CLOSE, handler=self.__onClose)

        self.__application.onStartTreeUpdate -= self.__onStartUpdate
        self.__application.onEndTreeUpdate -= self.__onEndUpdate
        self.__application.onPageSelect -= self.__onPageSelect

        self.__unbindAppEvents()
        self.__tagsPanel.clearTags()
        self.__tagsPanel.Destroy()


    def __onStartUpdate (self, page):
        self.__unbindAppEvents()


    def __onEndUpdate (self, page):
        self.__bindAppEvents()
        self.updateTags()


    def __onTagLeftClick (self, event):
        assert self.__currentTags != None

        pages = self.__currentTags[event.text][:]
        pages.sort (sortAlphabeticalFunction)

        self.__tagsPanel.showPopup(pages)


    def __onTagMiddleClick (self, event):
        """
        Средний клик по тегу
        """
        selectedPage = self.__application.selectedPage
        if selectedPage != None:
            tag = event.text

            if tag in selectedPage.tags:
                removeTag (selectedPage, tag)
            else:
                appendTag (selectedPage, tag)


    def __onPageClick (self, event):
        assert event.page != None
        self.__application.selectedPage = event.page


    def __bindAppEvents (self):
        self.__application.onPageUpdate += self.__onUpdate
        self.__application.onPageRemove += self.__onUpdate
        self.__application.onPageCreate += self.__onUpdate
        self.__application.onTreeUpdate += self.__onUpdate
        self.__application.onWikiOpen += self.__onUpdate


    def __unbindAppEvents (self):
        self.__application.onPageUpdate -= self.__onUpdate
        self.__application.onPageRemove -= self.__onUpdate
        self.__application.onPageCreate -= self.__onUpdate
        self.__application.onTreeUpdate -= self.__onUpdate
        self.__application.onWikiOpen -= self.__onUpdate


    def __onPageSelect (self, page):
        self.__markTags()


    def __onUpdate (self, sender, **kwargs):
        self.updateTags()


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


    def updateTags (self):
        if self.__application.wikiroot == None:
            self.__tagsPanel.clearMarks()
            self.__tagsPanel.clearTags()
            return

        tags = TagsList (self.__application.wikiroot)

        if not self.__isEqual (tags, self.__currentTags):
            self.__tagsPanel.setTags (tags)
            self.__currentTags = tags
            self.__markTags()


    def __markTags (self):
        self.__tagsPanel.clearMarks()

        if self.__application.selectedPage != None:
            for tag in self.__application.selectedPage.tags:
                self.__tagsPanel.mark (tag)
