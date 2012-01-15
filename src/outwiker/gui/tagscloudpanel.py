#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .tagscloud import TagsCloud
from outwiker.core.application import Application
from outwiker.core.tagslist import TagsList


class TagsCloudPanel (wx.Panel):
    def __init__ (self, parent):
        wx.Panel.__init__ (self, parent)

        self.__currentTags = None
        self.__tagscloud = TagsCloud (self)

        self.__layout()
        self.__bindAppEvents()


    def __layout (self):
        mainSizer = wx.FlexGridSizer (1, 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)
        mainSizer.Add (self.__tagscloud, 0, wx.ALL | wx.EXPAND, 4)
        self.SetSizer (mainSizer)


    def __bindAppEvents (self):
        Application.onPageUpdate += self.__onPageUpdate
        Application.onTreeUpdate += self.__onTreeUpdate
        Application.onEndTreeUpdate += self.__onEndTreeUpdate

    
    def __unbindAppEvents (self):
        Application.onPageUpdate -= self.__onPageUpdate
        Application.onTreeUpdate -= self.__onTreeUpdate
        Application.onEndTreeUpdate -= self.__onEndTreeUpdate


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
        if Application.wikiroot == None:
            self.__tagscloud.clear()
            return

        tags = TagsList (Application.wikiroot)

        if not self.__isEqual (tags, self.__currentTags):
            self.__tagscloud.setTags (tags)
            self.__currentTags = tags
