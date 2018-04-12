# -*- coding: utf-8 -*-

import wx
import wx.aui

from outwiker.gui.defines import MENU_VIEW, TOOLBAR_ORDER_PLUGIN


class ToolBarInfo (object):
    def __init__(self, toolbar, menuitem):
        """
        toolbar - экземпляр класса панели инструментов (производный от ToolBar)
        menuitem - экземпляр класса wx.MenuItem, представляющий элемент меню,
            соответствующий данной панели инструментов
        """
        self.toolbar = toolbar
        self.menuitem = menuitem


class ToolBarsController(object):
    """
    Класс для управления панелями инструментов и меню, связанными с ними
    """
    def __init__(self, mainWindow, toolbarcontainer, application):
        self._mainWindow = mainWindow
        self._toolbarcontainer = toolbarcontainer
        self._application = application

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        viewMenu = self._mainWindow.menuController[MENU_VIEW]
        viewMenu.Append(-1, _(u"Toolbars"), self._toolbarsMenu)

    def __getitem__(self, toolbarname):
        return self._toolbarcontainer[toolbarname]

    def createToolBar(self, toolbar_id,
                      title, order=TOOLBAR_ORDER_PLUGIN):
        toolbar = self._toolbarcontainer.createToolbar(toolbar_id, order=order)
        newitem = self._addMenu(toolbar, title)
        self._toolbars[toolbar_id] = ToolBarInfo(toolbar, newitem)
        # self.layout()

    def _addMenu(self, toolbar, title):
        newitem = self._toolbarsMenu.AppendCheckItem(wx.ID_ANY, title)
        newitem.Check(toolbar.IsShown())

        self._mainWindow.Bind(wx.EVT_MENU, self._onToolBarMenuClick, newitem)
        return newitem

    def _removeMenu(self, toolbarinfo):
        self._toolbarsMenu.Delete(toolbarinfo.menuitem)
        self._mainWindow.Unbind(wx.EVT_MENU,
                                source=toolbarinfo.menuitem,
                                handler=self._onToolBarMenuClick)

    def _onToolBarMenuClick(self, event):
        toolbarinfo = self._getToolBar(event.GetId())
        assert toolbarinfo is not None

        if toolbarinfo.toolbar.IsShown():
            toolbarinfo.toolbar.Hide()
        else:
            toolbarinfo.toolbar.Show()

    def _getToolBar(self, menuid):
        """
        Найти панель инструментов по идентификатору меню
        """
        for toolbarinfo in self._toolbars.values():
            if menuid == toolbarinfo.menuitem.GetId():
                return toolbarinfo

    def destroyToolBar(self, toolbarname):
        """
        Уничтожить панель инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        toolbarinfo = self._toolbars[toolbarname]
        self._removeMenu(toolbarinfo)
        del self._toolbars[toolbarname]
        self._toolbarcontainer.destroyToolBar(toolbarname)

    def destroyAllToolBars(self):
        """
        Уничтожить все панели инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        for toolbarname in list(self._toolbars):
            self.destroyToolBar(toolbarname)

    def __contains__(self, toolbarname):
        return toolbarname in self._toolbars

    # TODO: Deprecated.
    # There is for backward compatibility with the WebPage plugin.
    def updatePanesInfo(self):
        pass
