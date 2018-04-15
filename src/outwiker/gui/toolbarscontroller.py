# -*- coding: utf-8 -*-

import wx
import wx.aui

from outwiker.gui.defines import TOOLBAR_ORDER_PLUGIN


class ToolBarInfo (object):
    def __init__(self, toolbar, menu_item, order):
        """
        toolbar - экземпляр класса панели инструментов ToolBar2
        menu_item - экземпляр класса wx.menu_item, представляющий элемент меню,
            соответствующий данной панели инструментов
        order - порядок следования панелей инструментов
        """
        self.toolbar = toolbar
        self.menu_item = menu_item
        self.order = order


class ToolBarsController(object):
    """
    Класс для управления панелями инструментов и меню, связанными с ними
    """
    def __init__(self, parentMenu, toolbarcontainer, application):
        self._toolbarcontainer = toolbarcontainer
        self._application = application

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        parentMenu.Append(-1, _(u"Toolbars"), self._toolbarsMenu)

    def __getitem__(self, toolbarname):
        return self._toolbarcontainer[toolbarname]

    def createToolBar(self, toolbar_id,
                      title, order=TOOLBAR_ORDER_PLUGIN):
        toolbar = self._toolbarcontainer.createToolBar(toolbar_id, order=order)
        menu_item = self._addMenu(toolbar, title)
        self._toolbars[toolbar_id] = ToolBarInfo(toolbar, menu_item, order)

    def _addMenu(self, toolbar, title):
        newitem = self._toolbarsMenu.AppendCheckItem(wx.ID_ANY, title)
        newitem.Check(toolbar.IsShown())

        self._toolbarsMenu.Bind(wx.EVT_MENU, self._onToolBarMenuClick, newitem)
        return newitem

    def _removeMenu(self, toolbarinfo):
        self._toolbarsMenu.Delete(toolbarinfo.menu_item)
        self._toolbarsMenu.Unbind(wx.EVT_MENU,
                                  source=toolbarinfo.menu_item,
                                  handler=self._onToolBarMenuClick)

    def _onToolBarMenuClick(self, event):
        toolbarinfo = self._getToolBarByMenuId(event.GetId())
        assert toolbarinfo is not None

        if toolbarinfo.menu_item.IsChecked():
            toolbarinfo.toolbar.Show()
        else:
            toolbarinfo.toolbar.Hide()

    def _getToolBarByMenuId(self, menuid):
        """
        Найти панель инструментов по идентификатору меню
        """
        for toolbar_info in self._toolbars.values():
            if menuid == toolbar_info.menu_item.GetId():
                return toolbar_info

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

    def getMenuItem(self, toolbar_id):
        return self._toolbars[toolbar_id].menu_item

    def __contains__(self, toolbarname):
        return toolbarname in self._toolbars

    # TODO: Deprecated.
    # There is for backward compatibility with the WebPage plugin.
    def updatePanesInfo(self):
        pass
