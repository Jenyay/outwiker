# -*- coding: utf-8 -*-

import wx

from outwiker.api.core.plugins import Plugin
from outwiker.api.gui.defines import MENU_TOOLS

from .i18n import set_
from .pagestat import PageStat
from .treestat import TreeStat
from .pagestatdialog import PageStatDialog
from .treestatdialog import TreeStatDialog


class PluginStatistics(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)

        self._separatorMenuItem = None
        self._pageStatMenuItem = None
        self._treeStatMenuItem = None

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "Statistics"

    @property
    def description(self):
        return _(
            """The plugin to display statistics. 
                
Statistics plugin append menu items <b>Tools -> Page Statistic</b> and <b>Tools -> Tree Statistic</b>."""
        )

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/StatisticsEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        if self._application.mainWindow is not None:
            self._addMenuItems()

    def destroy(self):
        if self._application.mainWindow is not None:
            self._removeMenu()

    #############################################

    @property
    def toolsMenu(self):
        return self._application.mainWindow.menuController[MENU_TOOLS]

    def _addMenuItems(self):
        """
        Добавить пункты, связанные со статистикой в меню 'Инструменты'
        """
        assert self._separatorMenuItem is None
        assert self._pageStatMenuItem is None
        assert self._treeStatMenuItem is None

        self._separatorMenuItem = self.toolsMenu.AppendSeparator()

        self._pageStatMenuItem = self.toolsMenu.Append(wx.ID_ANY, _("Page Statistic"))

        self._application.mainWindow.Bind(
            wx.EVT_MENU, self._onPageStat, id=self._pageStatMenuItem.GetId()
        )

        self._treeStatMenuItem = self.toolsMenu.Append(wx.ID_ANY, _("Tree Statistic"))
        self._application.mainWindow.Bind(
            wx.EVT_MENU, self._onTreeStat, id=self._treeStatMenuItem.GetId()
        )

    def _removeMenu(self):
        """
        Удалить добавленные пункты меню
        """
        assert self._separatorMenuItem is not None
        assert self._pageStatMenuItem is not None
        assert self._treeStatMenuItem is not None

        self._application.mainWindow.Unbind(wx.EVT_MENU, handler=self._onPageStat)
        self._application.mainWindow.Unbind(wx.EVT_MENU, handler=self._onTreeStat)

        self.toolsMenu.Remove(self._separatorMenuItem)
        self.toolsMenu.Remove(self._pageStatMenuItem)
        self.toolsMenu.Remove(self._treeStatMenuItem)

        self._separatorMenuItem = None
        self._pageStatMenuItem = None
        self._treeStatMenuItem = None

    def _onPageStat(self, event):
        if self._application.selectedPage is not None:
            pageStat = PageStat(self._application.selectedPage)

            with PageStatDialog(self._application.mainWindow, pageStat) as dlg:
                dlg.ShowModal()

    def _onTreeStat(self, event):
        if self._application.wikiroot is not None:
            treeStat = TreeStat(self._application.wikiroot)
            with TreeStatDialog(
                self._application.mainWindow, self._application, treeStat
            ) as dlg:
                dlg.ShowModal()
