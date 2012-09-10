#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path

import wx

from outwiker.core.config import StringListSection


class TabsController (object):
    def __init__ (self, tabsCtrl, application):
        """
        tabsCtrl - экземпляр класса TabsCtrl
        application - экземпляр класса ApplicationParams
        """
        self._tabsCtrl = tabsCtrl
        self._application = application

        self._tabsSection = u"Tabs"
        self._tabsParamName = u"tab_"

        self.__bindEvents()


    def __createConfig (self, config):
        return StringListSection (config, self._tabsSection, self._tabsParamName)


    def destroy (self):
        if self._application.wikiroot != None:
            self.__saveTabs(self._application.wikiroot)

        self.__unbindEvents()


    def __bindEvents (self):
        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onPageUpdate += self.__updateCurrentPage
        self._application.onPageSelect += self.__updateCurrentPage
        self._application.onPageCreate += self.__updateCurrentPage
        self._application.onTreeUpdate += self.__updateCurrentPage
        self._application.onPageRename += self.__onPageRename
        self._application.onEndTreeUpdate += self.__updateCurrentPage

        self._tabsCtrl.Bind (wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.__onTabChanged)


    def __unbindEvents (self):
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onPageUpdate -= self.__updateCurrentPage
        self._application.onPageSelect -= self.__updateCurrentPage
        self._application.onPageCreate -= self.__updateCurrentPage
        self._application.onTreeUpdate -= self.__updateCurrentPage
        self._application.onPageRename -= self.__onPageRename
        self._application.onEndTreeUpdate -= self.__updateCurrentPage

        self._tabsCtrl.Unbind (wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, handler=self.__onTabChanged)


    def __onTabChanged (self, event):
        newindex = event.GetSelection()
        page = self._tabsCtrl.getPage(newindex)
        self._application.selectedPage = page


    def __loadTabs (self, wikiroot):
        self._tabsCtrl.clear()

        if wikiroot == None:
            return

        tabsList = self.__createConfig(wikiroot.params).value

        for tab in tabsList:
            page = wikiroot[tab]
            if page != None:
                self._tabsCtrl.addPage (self.__getTitle (page), page)


    def __saveTabs (self, wikiroot):
        pageSubpathList = [page.subpath for page in self._tabsCtrl.getPages() if page != None]
        self.__createConfig(wikiroot.params).value = pageSubpathList


    def cloneTab (self):
        self.__createCurrentTab()


    def __onPageRename (self, page, oldSubpath):
        self.__updateCurrentPage (self._application.selectedPage)


    def __onWikiOpen (self, root):
        self.__loadTabs(root)


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
