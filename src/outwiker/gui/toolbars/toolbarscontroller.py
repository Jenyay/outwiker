# -*- coding: utf-8 -*-

from .toolbarinfo import ToolBarInfo

import wx
import wx.aui


class ToolBarsController(object):
    """
    Класс для управления панелями инструментов и меню, связанными с ними
    """
    def __init__(self, parent):
        self._parent = parent

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        self._parent.mainMenu.viewMenu.AppendMenu(-1, _(u"Toolbars"),
                                                  self._toolbarsMenu)
        self._parent.auiManager.Bind(wx.aui.EVT_AUI_PANE_CLOSE,
                                     self.__onPaneClose)

    def __onPaneClose(self, event):
        for toolbarinfo in self._toolbars.values():
            if event.GetPane().name == toolbarinfo.toolbar.name:
                toolbarinfo.menuitem.Check(False)
                toolbarinfo.toolbar.Hide()
                return

        event.Skip()

    def __getitem__(self, toolbarname):
        return self._toolbars[toolbarname].toolbar

    def __setitem__(self, toolbarname, toolbar):
        if toolbarname in self._toolbars:
            raise KeyError()

        newitem = self._addMenu(toolbar)
        self._toolbars[toolbarname] = ToolBarInfo(toolbar, newitem)
        toolbar.UpdateToolBar()

    def _addMenu(self, toolbar):
        newitem = self._toolbarsMenu.AppendCheckItem(wx.ID_ANY,
                                                     toolbar.caption)
        newitem.Check(toolbar.pane.IsShown())

        self._parent.Bind(wx.EVT_MENU, self.__onToolBarMenuClick, newitem)
        return newitem

    def _removeMenu(self, toolbarinfo):
        self._toolbarsMenu.DeleteItem(toolbarinfo.menuitem)
        self._parent.Unbind(wx.EVT_MENU,
                            source=toolbarinfo.menuitem,
                            handler=self.__onToolBarMenuClick)

    def __onToolBarMenuClick(self, event):
        toolbarinfo = self._getToolBar(event.GetId())
        assert toolbarinfo is not None

        if toolbarinfo.toolbar.IsShown():
            toolbarinfo.toolbar.Hide()
        else:
            toolbarinfo.toolbar.Show()

        toolbarinfo.toolbar.UpdateToolBar()
        self._parent.UpdateAuiManager()

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
        toolbarinfo.toolbar.updatePaneInfo()
        self._removeMenu(toolbarinfo)
        self._parent.auiManager.DetachPane(toolbarinfo.toolbar)

        toolbarinfo.toolbar.Destroy()
        del self._toolbars[toolbarname]
        self._parent.UpdateAuiManager()

    def destroyAllToolBars(self):
        """
        Уничтожить все панели инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        self.updatePanesInfo()

        self._parent.auiManager.Unbind(wx.aui.EVT_AUI_PANE_CLOSE,
                                       handler=self.__onPaneClose)

        for toolbarname in self._toolbars.keys():
            self.destroyToolBar(toolbarname)

    def __contains__(self, toolbarname):
        return toolbarname in self._toolbars

    def updatePanesInfo(self):
        map(lambda toolbar: toolbar.toolbar.updatePaneInfo(),
            self._toolbars.values())

    def layout(self):
        '''
        Fix toolbars positions in the window to all toolbars were visible.
        '''
        mainWindowWidth = self._parent.GetClientSize()[0]

        for name, toolbar_info in self._toolbars.items():
            toolbar = toolbar_info.toolbar
            toolbar_rect = toolbar.GetRect()
            if toolbar_rect.GetLeft() >= mainWindowWidth:
                self._moveToolbar(name)

    def _getPaneInfo(self, name):
        auiManager = self._parent.auiManager
        toolbar = self._getToolbar(name)
        pane_info = auiManager.GetPane(toolbar)
        return pane_info

    def _getToolbar(self, name):
        return self._toolbars[name].toolbar

    def _getToolbarRow(self, name):
        toolbar = self._getToolbar(name)
        pane_info = self._parent.auiManager.GetPane(toolbar)
        return pane_info.dock_row

    def _getRowsCount(self):
        maxIndex = -1
        for name in self._toolbars.keys():
            toolbar_row = self._getToolbarRow(name)
            if toolbar_row > maxIndex:
                maxIndex = toolbar_row

        return maxIndex + 1

    def _moveToolbar(self, name):
        '''
        Find location for toolbar and move it there.
        '''
        margin = 24
        mainWindowWidth = self._parent.GetClientSize()[0]
        auiManager = self._parent.auiManager

        # Calculate empty space for each row
        rows_spaces = [mainWindowWidth] * self._getRowsCount()
        for toolbar_name in self._toolbars.keys():
            if toolbar_name == name:
                continue

            toolbar = self._getToolbar(toolbar_name)
            toolbar_rect = toolbar.GetRect()
            toolbar_row = self._getToolbarRow(toolbar_name)
            space = mainWindowWidth - toolbar_rect.GetRight()

            if space < rows_spaces[toolbar_row]:
                rows_spaces[toolbar_row] = space

        # Find row to move the toolbar
        row_index = len(rows_spaces)
        for n, space in enumerate(rows_spaces):
            if space > margin:
                row_index = n
                break

        # Find position for toolbar
        if row_index == len(rows_spaces):
            toolbar_pos = 0
        else:
            toolbar_pos = mainWindowWidth - rows_spaces[row_index]

        # Move toolbar
        moved_pane_info = self._getPaneInfo(name)
        moved_pane_info.Position(toolbar_pos).Row(row_index)

        moved_toolbar = self._getToolbar(name)
        moved_toolbar.updatePaneInfo()

        auiManager.Update()
