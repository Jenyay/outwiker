#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .pagelist import EVT_PAGE_CLICK
from .taglabel import EVT_TAG_CLICK

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import RootWikiPage


class TagsPanelController (object):
    def __init__ (self, tagsPanel, application):
        self.__tagsPanel = tagsPanel
        self.__application = application
        self.__currentTags = None

        self.__bindAppEvents()
        self.__tagsPanel.Bind (EVT_PAGE_CLICK, self.__onPageClick)
        self.__tagsPanel.Bind (EVT_TAG_CLICK, self.__onTagClick)

        self.updateTags()


    def __onTagClick (self, event):
        pages = self.__currentTags[event.text][:]
        pages.sort (RootWikiPage.sortAlphabeticalFunction)

        self.__tagsPanel.showPopup(pages)


    def __onPageClick (self, event):
        assert event.page != None
        self.__application.selectedPage = event.page


    def __bindAppEvents (self):
        self.__application.onPageUpdate += self.__onUpdate
        self.__application.onPageRemove += self.__onUpdate
        self.__application.onPageCreate += self.__onUpdate
        self.__application.onTreeUpdate += self.__onUpdate
        self.__application.onEndTreeUpdate += self.__onUpdate
        self.__application.onWikiOpen += self.__onUpdate
        self.__application.onPageSelect += self.__onPageSelect


    def __onPageSelect (self, page):
        self.__markTags()


    def __onUpdate (self, sender):
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
