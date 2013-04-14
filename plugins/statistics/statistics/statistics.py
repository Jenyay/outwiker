#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_
from .pagestat import PageStat


if getCurrentVersion() < Version (1, 7, 0, 684, status=StatusSet.DEV):
    print ("Spoiler plugin. OutWiker version requirement: 1.7.0.684")
else:
    class PluginStatistics (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)

            self.ID_PAGE_STAT = wx.NewId()

            self._separatorMenuItem = None
            self._pageStatMenuItem = None


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Statistics"

        
        @property
        def description (self):
            return _(u"Plugin to display statistics")


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net")
        
        
        def initialize(self):
            self._initlocale(u"statistics")
            self._addMenuItems ()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._removeMenu ()

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e

            set_(_)


        @property
        def toolsMenu (self):
            return self._application.mainWindow.mainMenu.toolsMenu


        def _addMenuItems (self):
            """
            Добавить пункты, связанные со статистикой в меню 'Инструменты'
            """
            assert self._separatorMenuItem == None
            assert self._pageStatMenuItem == None

            self._separatorMenuItem = self.toolsMenu.AppendSeparator()
            self._pageStatMenuItem = self.toolsMenu.Append (self.ID_PAGE_STAT, _(u"Page statistic"))

            self._application.mainWindow.Bind (wx.EVT_MENU, self._onPageStat, id=self.ID_PAGE_STAT)


        def _removeMenu (self):
            """
            Удалить добавленные пункты меню
            """
            assert self._separatorMenuItem != None
            assert self._pageStatMenuItem != None

            self._application.mainWindow.Unbind (wx.EVT_MENU, handler=self._onPageStat)

            self.toolsMenu.RemoveItem (self._separatorMenuItem)
            self.toolsMenu.RemoveItem (self._pageStatMenuItem)

            self._separatorMenuItem = None
            self._pageStatMenuItem = None


        def getPageStat (self, page):
            return PageStat (page)


        def _onPageStat (self, event):
            print "Statistics"
