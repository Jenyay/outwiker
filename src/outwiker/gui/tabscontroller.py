#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path

import wx


class TabsController (object):
    def __init__ (self, tabsCtrl, application):
        """
        tabsCtrl - экземпляр класса TabsCtrl
        application - экземпляр класса ApplicationParams
        """
        self._tabsCtrl = tabsCtrl
        self._application = application

        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onPageUpdate += self.__updateCurrentPage
        self._application.onPageSelect += self.__updateCurrentPage
        self._application.onPageCreate += self.__updateCurrentPage
        self._application.onTreeUpdate += self.__updateCurrentPage
        self._application.onPageRename += self.__onPageRename
        self._application.onEndTreeUpdate += self.__updateCurrentPage

        self._tabsCtrl.Bind (wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.__onTabChanged)


    def __onTabChanged (self, event):
        newindex = event.GetSelection()
        page = self._tabsCtrl.getPage(newindex)
        self._application.selectedPage = page


    def cloneTab (self):
        self.__createCurrentTab()


    def __onPageRename (self, page, oldSubpath):
        self.__updateCurrentPage (self._application.selectedPage)


    def __onWikiOpen (self, root):
        self._tabsCtrl.clear()
        self.__createCurrentTab()


    def __getTitle (self, page):
        if page != None:
            return page.title

        if self._application.wikiroot == None:
            return "    "
        else:
            return os.path.basename (self._application.wikiroot.path)


    def __createCurrentTab (self):
        page = self._application.selectedPage
        self._tabsCtrl.addPage (self.__getTitle (page), page)


    def __updateCurrentPage (self, page):
        self._tabsCtrl.renameCurrentTab (self.__getTitle (self._application.selectedPage))
        self._tabsCtrl.setCurrentPage (self._application.selectedPage)
