#-*- coding: utf-8 -*-

import os.path

import wx
import wx.lib.agw.flatnotebook as fnb

from outwiker.core.config import StringListSection, IntegerOption
from outwiker.core.tree import RootWikiPage
from outwiker.core.commands import MessageBox
from .mainid import MainId
from .pagepopupmenu import PagePopupMenu


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

        self.NEXT_TAB = wx.NewId()

        self.__bindEvents()


    def openInTab (self, page, select):
        """
        Открыть страницу в новой вкладке
        page - страница, которую надо открыть в новой вкладке
        select - нужно ли сразу выбрать новую вкладку
        """
        selectedTab = self._tabsCtrl.GetSelection()
        self._tabsCtrl.InsertPage (selectedTab + 1, self.__getTitle (page), page, select)
        self.__saveTabs()


    def closeTab (self, index):
        """
        Закыть вкладку с индексом index
        """
        if index < 0 or index >= self.getTabsCount():
            raise ValueError

        self._tabsCtrl.DeletePage (index)


    def getTabsCount (self):
        """
        Возвращает количество открытых вкладок
        """
        return self._tabsCtrl.GetPageCount()


    def getTabTitle (self, index):
        """
        Возвращает заголовок вкладки с номером index
        """
        if index < 0 or index >= self.getTabsCount():
            raise ValueError

        return self._tabsCtrl.GetPageText(index)


    def getSelection (self):
        return self._tabsCtrl.GetSelection()


    def setSelection (self, index):
        if index < 0 or index >= self.getTabsCount():
            raise ValueError

        self._tabsCtrl.SetSelection (index)
        self._application.selectedPage = self._tabsCtrl.GetPage (index)
        self.__saveTabs()


    def getPage (self, index):
        if index < 0 or index >= self.getTabsCount():
            raise ValueError

        return self._tabsCtrl.GetPage (index)


    def cloneTab (self):
        if self.getTabsCount() != 0:
            self.__createCurrentTab()


    def nextTab (self):
        self._tabsCtrl.NextPage()


    def previousTab (self):
        self._tabsCtrl.PreviousPage()


    def __createStringListConfig (self, config):
        return StringListSection (config, self._tabsSection, self._tabsParamName)


    def destroy (self):
        """
        Вызывать перед удалением контроллера
        """
        self.__saveTabs()
        self.__unbindEvents()


    def historyBack (self):
        """
        Перейти на предыдущую страницу на данной вкладке
        """
        self._tabsCtrl.HistoryBack()


    def historyForward (self):
        """
        Перейти на предыдущую страницу на данной вкладке
        """
        self._tabsCtrl.HistoryForward()


    def __bindGuiEvents (self):
        self._tabsCtrl.Bind (fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.__onTabChanged)
        self._tabsCtrl.Bind (fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.__onTabClose)
        self._tabsCtrl.Bind (fnb.EVT_FLATNOTEBOOK_PAGE_DROPPED, self.__onTabDropped)
        self._tabsCtrl.Bind (fnb.EVT_FLATNOTEBOOK_PAGE_CONTEXT_MENU, self.__onPopupMenu)


    def __unbindGuiEvents (self):
        self._tabsCtrl.Unbind (fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, handler=self.__onTabChanged)
        self._tabsCtrl.Unbind (fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, handler=self.__onTabClose)
        self._tabsCtrl.Unbind (fnb.EVT_FLATNOTEBOOK_PAGE_DROPPED, handler=self.__onTabDropped)
        self._tabsCtrl.Unbind (fnb.EVT_FLATNOTEBOOK_PAGE_CONTEXT_MENU, handler=self.__onPopupMenu)


    def __bindEvents (self):
        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onPageUpdate += self.__onPageUpdate
        self._application.onPageSelect += self.__onPageUpdate
        self._application.onPageCreate += self.__onPageUpdate
        self._application.onTreeUpdate += self.__onPageUpdate
        self._application.onPageRemove += self.__onPageUpdate
        self._application.onPageRename += self.__onPageRename
        self._application.onEndTreeUpdate += self.__onPageUpdate

        self.__bindGuiEvents()


    def __unbindEvents (self):
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onPageUpdate -= self.__onPageUpdate
        self._application.onPageSelect -= self.__onPageUpdate
        self._application.onPageCreate -= self.__onPageUpdate
        self._application.onTreeUpdate -= self.__onPageUpdate
        self._application.onPageRemove -= self.__onPageUpdate
        self._application.onPageRename -= self.__onPageRename
        self._application.onEndTreeUpdate -= self.__onPageUpdate

        self.__unbindGuiEvents()


    def __onPopupMenu (self, event):
        popupPage = self.getPage (event.GetSelection())
        popupMenu = PagePopupMenu (self._tabsCtrl, popupPage, self._application)
        self._tabsCtrl.PopupMenu (popupMenu.menu)


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


    def __onTabDropped (self, event):
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
            try:
                pageSubpathList = [page.subpath for page in self._tabsCtrl.GetPages() if page != None]
                self.__createStringListConfig (self._application.wikiroot.params).value = pageSubpathList

                selectedTab = self._tabsCtrl.GetSelection()
                self._application.wikiroot.params.set (self._tabSelectedSection, self._tabSelectedOption, str (selectedTab))
            except IOError, e:
                MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)


    def __onPageRename (self, page, oldSubpath):
        self.__onPageUpdate (self._application.selectedPage)


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
        self.openInTab (self._application.selectedPage, True)


    def __onPageUpdate (self, page, **kwargs):
        self._tabsCtrl.RenameCurrentTab (self.__getTitle (self._application.selectedPage))
        self._tabsCtrl.SetCurrentPage (self._application.selectedPage)
        self.__checkInvalidTabs ()
        self.__saveTabs()


    def __checkInvalidTabs (self):
        """
        Проверить табы на неправильность отображения
        """
        index = 0
        while index < self.getTabsCount():
            selectedIndex = self.getSelection()
            page = self.getPage (index)

            if (page == None or page.isRemoved) and index != selectedIndex:
                self._tabsCtrl.DeletePage (index)
                index -= 1
            elif page == None or page.title != self.getTabTitle (index):
                self._tabsCtrl.RenameTab (index, self.__getTitle (page))

            index += 1
