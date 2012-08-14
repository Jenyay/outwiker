#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .toolbarinfo import ToolBarInfo

import wx
import wx.aui


class ToolBarsController (object):
    """
    Класс для управления панелями инструментов и меню, связанными с ними
    """
    def __init__ (self, parent):
        self._parent = parent

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        self._parent.mainMenu.viewMenu.InsertMenu (3, -1, _(u"Toolbars"), self._toolbarsMenu)
        self._parent.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)


    def __onPaneClose (self, event):
        for toolbarinfo in self._toolbars.values():
            if event.GetPane().name == toolbarinfo.toolbar.name:
                toolbarinfo.menuitem.Check (False)
                return

        event.Skip()


    def __getitem__ (self, toolbarname):
        return self._toolbars[toolbarname].toolbar


    def __setitem__ (self, toolbarname, toolbar):
        if toolbarname in self._toolbars:
            raise KeyError()

        newitem = self._toolbarsMenu.AppendCheckItem (wx.NewId(), toolbar.caption)
        newitem.Check (toolbar.IsShown())
        self._toolbars[toolbarname] = ToolBarInfo (toolbar, newitem)

        self._parent.Bind(wx.EVT_MENU, self.__onToolBarMenuClick, newitem)


    def __onToolBarMenuClick (self, event):
        toolbarinfo = self._getToolBar (event.GetId())
        assert toolbarinfo != None

        if toolbarinfo.toolbar.IsShown():
            toolbarinfo.toolbar.Hide()
        else:
            toolbarinfo.toolbar.Show()

        toolbarinfo.toolbar.UpdateToolBar()
        self._parent.UpdateAuiManager()


    def _getToolBar (self, menuid):
        """
        Найти панель инструментов по идентификатору меню
        """
        for toolbarinfo in self._toolbars.values():
            if menuid == toolbarinfo.menuitem.GetId():
                return toolbarinfo


    def destroyToolBar (self, toolbarname):
        """
        Уничтожить панель инструментов. Нужно вызывать до вызова auiManager.UnInit()
        """
        self._parent.auiManager.DetachPane (self._toolbars[toolbarname].toolbar)

        self._toolbars[toolbarname].toolbar.Destroy()
        del self._toolbars[toolbarname]
        self._parent.UpdateAuiManager()



    def destroyAllToolBars (self):
        """
        Уничтожить все панели инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        for toolbarname in self._toolbars.keys():
            self.destroyToolBar (toolbarname)


    def __contains__ (self, toolbarname):
        return toolbarname in self._toolbars
