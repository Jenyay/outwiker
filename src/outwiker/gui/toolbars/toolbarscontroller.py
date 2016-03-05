# -*- coding: utf-8 -*-

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
        self._parent.mainMenu.viewMenu.AppendMenu (-1, _(u"Toolbars"), self._toolbarsMenu)
        self._parent.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)


    def __onPaneClose (self, event):
        for toolbarinfo in self._toolbars.values():
            if event.GetPane().name == toolbarinfo.toolbar.name:
                toolbarinfo.menuitem.Check (False)
                toolbarinfo.toolbar.Hide()
                return

        event.Skip()


    def __getitem__ (self, toolbarname):
        return self._toolbars[toolbarname].toolbar


    def __setitem__ (self, toolbarname, toolbar):
        if toolbarname in self._toolbars:
            raise KeyError()

        newitem = self._addMenu (toolbar)
        self._toolbars[toolbarname] = ToolBarInfo (toolbar, newitem)
        toolbar.UpdateToolBar()


    def _addMenu (self, toolbar):
        newitem = self._toolbarsMenu.AppendCheckItem (wx.NewId(), toolbar.caption)
        newitem.Check (toolbar.pane.IsShown())

        self._parent.Bind(wx.EVT_MENU, self.__onToolBarMenuClick, newitem)
        return newitem


    def _removeMenu (self, toolbarinfo):
        self._toolbarsMenu.DeleteItem (toolbarinfo.menuitem)
        self._parent.Unbind(wx.EVT_MENU, source=toolbarinfo.menuitem, handler=self.__onToolBarMenuClick)


    def __onToolBarMenuClick (self, event):
        toolbarinfo = self._getToolBar (event.GetId())
        assert toolbarinfo is not None

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
        toolbarinfo = self._toolbars[toolbarname]
        toolbarinfo.toolbar.updatePaneInfo()
        self._removeMenu (toolbarinfo)
        self._parent.auiManager.DetachPane (toolbarinfo.toolbar)

        toolbarinfo.toolbar.Destroy()
        del self._toolbars[toolbarname]
        self._parent.UpdateAuiManager()


    def destroyAllToolBars (self):
        """
        Уничтожить все панели инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        self.updatePanesInfo()

        self._parent.auiManager.Unbind (wx.aui.EVT_AUI_PANE_CLOSE, handler=self.__onPaneClose)

        for toolbarname in self._toolbars.keys():
            self.destroyToolBar (toolbarname)


    def __contains__ (self, toolbarname):
        return toolbarname in self._toolbars


    def updatePanesInfo (self):
        map (lambda toolbar: toolbar.toolbar.updatePaneInfo(), self._toolbars.values())
