# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_
from .pagestat import PageStat
from .treestat import TreeStat
from .pagestatdialog import PageStatDialog
from .treestatdialog import TreeStatDialog


__version__ = u"1.0.1"


if getCurrentVersion() < Version (1, 7, 0, 684, status=StatusSet.DEV):
    print ("Statistics plugin. OutWiker version requirement: 1.7.0.684")
else:
    class PluginStatistics (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)

            self.ID_PAGE_STAT = wx.NewId()
            self.ID_TREE_STAT = wx.NewId()

            self._separatorMenuItem = None
            self._pageStatMenuItem = None
            self._treeStatMenuItem = None


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Statistics"


        @property
        def description (self):
            return _(u"""The plugin to display statistics. 
                    
Statistics plugin append menu items <b>Tools -> Page Statistic</b> and <b>Tools -> Tree Statistic</b>.""")


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/StatisticsEn")


        def initialize(self):
            self._initlocale(u"statistics")

            if self._application.mainWindow is not None:
                self._addMenuItems ()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            if self._application.mainWindow is not None:
                self._removeMenu ()


        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException, e:
                print e

            set_(_)


        @property
        def toolsMenu (self):
            return self._application.mainWindow.mainMenu.toolsMenu


        def _addMenuItems (self):
            """
            Добавить пункты, связанные со статистикой в меню 'Инструменты'
            """
            assert self._separatorMenuItem is None
            assert self._pageStatMenuItem is None
            assert self._treeStatMenuItem is None

            self._separatorMenuItem = self.toolsMenu.AppendSeparator()

            self._pageStatMenuItem = self.toolsMenu.Append (self.ID_PAGE_STAT, _(u"Page Statistic"))
            self._application.mainWindow.Bind (wx.EVT_MENU, self._onPageStat, id=self.ID_PAGE_STAT)

            self._treeStatMenuItem = self.toolsMenu.Append (self.ID_TREE_STAT, _(u"Tree Statistic"))
            self._application.mainWindow.Bind (wx.EVT_MENU, self._onTreeStat, id=self.ID_TREE_STAT)


        def _removeMenu (self):
            """
            Удалить добавленные пункты меню
            """
            assert self._separatorMenuItem is not None
            assert self._pageStatMenuItem is not None
            assert self._treeStatMenuItem is not None

            self._application.mainWindow.Unbind (wx.EVT_MENU, handler=self._onPageStat)
            self._application.mainWindow.Unbind (wx.EVT_MENU, handler=self._onTreeStat)

            self.toolsMenu.RemoveItem (self._separatorMenuItem)
            self.toolsMenu.RemoveItem (self._pageStatMenuItem)
            self.toolsMenu.RemoveItem (self._treeStatMenuItem)

            self._separatorMenuItem = None
            self._pageStatMenuItem = None
            self._treeStatMenuItem = None


        def _onPageStat (self, event):
            if self._application.selectedPage is not None:
                pageStat = PageStat (self._application.selectedPage)

                with PageStatDialog (self._application.mainWindow, pageStat) as dlg:
                    dlg.ShowModal()


        def _onTreeStat (self, event):
            if self._application.wikiroot is not None:
                treeStat = TreeStat (self._application.wikiroot)
                with TreeStatDialog (self._application.mainWindow, self._application, treeStat) as dlg:
                    dlg.ShowModal()


        def getPageStat (self, page):
            """
            Получить экземпляр класса для сбора статистики по странице. Используется в тестах
            """
            return PageStat (page)


        def getTreeStat (self, root):
            """
            Получить экземпляр класса для сбора статистики по дереву. Используется в тестах
            """
            return TreeStat (root)
