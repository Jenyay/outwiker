# -*- coding: utf-8 -*-

import wx
import wx.aui

from outwiker.core.config import BooleanOption
from outwiker.gui.defines import TOOLBAR_ORDER_PLUGIN
from outwiker.core.defines import (CONFIG_TOOLBARS_SECTION,
                                   CONFIG_TOOLBARS_VISIBLE_SUFFIX)


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

    def __str__(self):
        return '{title}: order={order}'.format(
            title=self.menu_item.GetText(),
            order=self.order
        )


class ToolBarsController(object):
    """
    Класс для управления панелями инструментов и меню, связанными с ними
    """
    def __init__(self, parentMenu, toolbarcontainer, config):
        self._toolbarcontainer = toolbarcontainer
        self._config = config

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        parentMenu.Append(-1, _(u"Toolbars"), self._toolbarsMenu)

    def getMenu(self):
        return self._toolbarsMenu

    def __getitem__(self, toolbarname):
        return self._toolbarcontainer[toolbarname]

    def createToolBar(self, toolbar_id,
                      title, order=TOOLBAR_ORDER_PLUGIN):
        toolbar = self._toolbarcontainer.createToolBar(toolbar_id, order=order)
        menu_item_index = self._getMenuItemIndex(order)
        menu_item = self._addMenu(toolbar, title, menu_item_index)
        self._toolbars[toolbar_id] = ToolBarInfo(toolbar, menu_item, order)

        is_visible = self._getVisibleOption(toolbar_id).value
        menu_item.Check(is_visible)
        toolbar.Show(is_visible)

    def _getMenuItemIndex(self, order):
        menu_items = sorted(self._toolbars.values(),
                            key=lambda item: item.order,
                            reverse=True)
        index = 0

        for n, item in enumerate(menu_items):
            if order >= item.order:
                break

            index += 1

        index = len(menu_items) - index
        return index

    def _addMenu(self, toolbar, title, index):
        menu_item = self._toolbarsMenu.InsertCheckItem(index, wx.ID_ANY, title)
        menu_item.Check(toolbar.IsShown())

        self._toolbarsMenu.Bind(wx.EVT_MENU,
                                self._onToolBarMenuClick,
                                menu_item)
        return menu_item

    def _removeMenu(self, toolbarinfo):
        self._toolbarsMenu.Delete(toolbarinfo.menu_item)
        self._toolbarsMenu.Unbind(wx.EVT_MENU,
                                  source=toolbarinfo.menu_item,
                                  handler=self._onToolBarMenuClick)

    def _onToolBarMenuClick(self, event):
        toolbar_id, toolbarinfo = self._getToolBarByMenuId(event.GetId())

        visible_option = self._getVisibleOption(toolbar_id)

        if toolbarinfo.menu_item.IsChecked():
            toolbarinfo.toolbar.Show()
            visible_option.value = True
        else:
            toolbarinfo.toolbar.Hide()
            visible_option.value = False

    def _getVisibleOption(self, toolbar_id):
        param_name = toolbar_id + CONFIG_TOOLBARS_VISIBLE_SUFFIX

        visible_option = BooleanOption(self._config,
                                       CONFIG_TOOLBARS_SECTION,
                                       param_name,
                                       True)
        return visible_option

    def _getToolBarByMenuId(self, menuid):
        """
        Найти панель инструментов по идентификатору меню
        """
        for toolbar_id, toolbar_info in self._toolbars.items():
            if menuid == toolbar_info.menu_item.GetId():
                return (toolbar_id, toolbar_info)

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
