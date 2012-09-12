#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path

import wx
import wx.lib.agw.flatnotebook as fnb

from outwiker.core.config import StringListSection, IntegerOption
from outwiker.core.tree import RootWikiPage


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

        self._tabSelectedSection = RootWikiPage.sectionGeneral
        self._tabSelectedOption = u"selectedtab"

        self.__bindEvents()


    def getTabsCount (self):
        """
        Возвращает количество открытых вкладок
        """
        return self._tabsCtrl.GetPageCount()


    def getTabTitle (self, index):
        """
        Возвращает заголовок вкладки с номером index
        """
        return self._tabsCtrl.GetPageText(index)


    def getSelection (self):
        return self._tabsCtrl.GetSelection()


    def getPage (self, index):
        return self._tabsCtrl.GetPage (index)


    def __createStringListConfig (self, config):
        return StringListSection (config, self._tabsSection, self._tabsParamName)


    def destroy (self):
        self.__saveTabs()

        self.__unbindEvents()


    def __bindEvents (self):
        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onPageUpdate += self.__updateCurrentPage
        self._application.onPageSelect += self.__updateCurrentPage
        self._application.onPageCreate += self.__updateCurrentPage
        self._application.onTreeUpdate += self.__updateCurrentPage
        self._application.onPageRename += self.__onPageRename
        self._application.onEndTreeUpdate += self.__updateCurrentPage

        self.__bindGuiEvents()


    def __bindGuiEvents (self):
        self._tabsCtrl.Bind (fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.__onTabChanged)
        self._tabsCtrl.Bind (fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.__onTabClose)


    def __unbindEvents (self):
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onPageUpdate -= self.__updateCurrentPage
        self._application.onPageSelect -= self.__updateCurrentPage
        self._application.onPageCreate -= self.__updateCurrentPage
        self._application.onTreeUpdate -= self.__updateCurrentPage
        self._application.onPageRename -= self.__onPageRename
        self._application.onEndTreeUpdate -= self.__updateCurrentPage

        self.__unbindGuiEvents()


    def __unbindGuiEvents (self):
        self._tabsCtrl.Unbind (fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, handler=self.__onTabChanged)
        self._tabsCtrl.Unbind (fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, handler=self.__onTabClose)


    def __onTabClose (self, event):
        selectedTabIndex = self._tabsCtrl.GetSelection()
        tabsCount = self._tabsCtrl.GetPageCount()

        if tabsCount == 1:
            event.Veto()
            return

        self.__saveTabs()


    def __onTabChanged (self, event):
        newindex = event.GetSelection()
        page = self._tabsCtrl.GetPage(newindex)
        self._application.selectedPage = page
        self.__saveTabs()


    def __loadTabs (self, wikiroot):
        self.__unbindGuiEvents()
        self._tabsCtrl.Clear()

        if wikiroot == None:
            self.__bindGuiEvents()
            return

        tabsList = self.__createStringListConfig(wikiroot.params).value

        for tab in tabsList:
            page = wikiroot[tab]
            if page != None:
                self._tabsCtrl.AddPage (self.__getTitle (page), page)

        selectedTab = IntegerOption (wikiroot.params, 
                self._tabSelectedSection, 
                self._tabSelectedOption,
                0).value

        pageCount = self._tabsCtrl.GetPageCount()

        if selectedTab < 0 or selectedTab >= pageCount:
            selectedTab = 0

        if pageCount < 1:
            self.__createCurrentTab()

        self._tabsCtrl.SetSelection (selectedTab)
        self._application.selectedPage = self._tabsCtrl.GetPage (selectedTab)

        self.__bindGuiEvents()


    def __saveTabs (self):
        if self._application.wikiroot != None:
            pageSubpathList = [page.subpath for page in self._tabsCtrl.GetPages() if page != None]
            self.__createStringListConfig (self._application.wikiroot.params).value = pageSubpathList

            selectedTab = self._tabsCtrl.GetSelection()
            self._application.wikiroot.params.set (self._tabSelectedSection, self._tabSelectedOption, str (selectedTab))


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
        selectedTab = self._tabsCtrl.GetSelection()
        self._tabsCtrl.InsertPage (selectedTab + 1, self.__getTitle (page), page)
        self.__saveTabs()


    def __updateCurrentPage (self, page):
        self._tabsCtrl.RenameCurrentTab (self.__getTitle (self._application.selectedPage))
        self._tabsCtrl.SetCurrentPage (self._application.selectedPage)
        self.__saveTabs()
