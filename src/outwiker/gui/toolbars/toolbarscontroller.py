# -*- coding: utf-8 -*-

from .toolbarinfo import ToolBarInfo

import wx
import wx.aui


class ToolBarsController(object):
    """
    Класс для управления панелями инструментов и меню, связанными с ними
    """
    def __init__(self, mainWindow):
        self._mainWindow = mainWindow

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        self._mainWindow.mainMenu.viewMenu.Append(-1, _(u"Toolbars"),
                                                      self._toolbarsMenu)
        self._mainWindow.auiManager.Bind(wx.aui.EVT_AUI_PANE_CLOSE,
                                         self.__onPaneClose)
        self._mainWindow.Bind(wx.EVT_SIZE, self.__onSizeChanged)

    def __onSizeChanged(self, event):
        self.layout()

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
        self.layout()

    def addToolbar(self, toolbar):
        '''
        Added in outwiker.gui 1.4
        '''
        self[toolbar.name] = toolbar

    def _addMenu(self, toolbar):
        newitem = self._toolbarsMenu.AppendCheckItem(wx.ID_ANY,
                                                     toolbar.caption)
        newitem.Check(toolbar.pane.IsShown())

        self._mainWindow.Bind(wx.EVT_MENU, self.__onToolBarMenuClick, newitem)
        return newitem

    def _removeMenu(self, toolbarinfo):
        self._toolbarsMenu.Delete(toolbarinfo.menuitem)
        self._mainWindow.Unbind(wx.EVT_MENU,
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
        self._mainWindow.UpdateAuiManager()

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
        self._mainWindow.auiManager.DetachPane(toolbarinfo.toolbar)

        toolbarinfo.toolbar.Destroy()
        del self._toolbars[toolbarname]
        self._mainWindow.UpdateAuiManager()

    def destroyAllToolBars(self):
        """
        Уничтожить все панели инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        self.updatePanesInfo()

        self._mainWindow.auiManager.Unbind(wx.aui.EVT_AUI_PANE_CLOSE,
                                           handler=self.__onPaneClose)
        self._mainWindow.Unbind(wx.EVT_SIZE, handler=self.__onSizeChanged)

        for toolbarname in list(self._toolbars):
            self.destroyToolBar(toolbarname)

    def __contains__(self, toolbarname):
        return toolbarname in self._toolbars

    def updatePanesInfo(self):
        [toolbar.toolbar.updatePaneInfo() for toolbar in self._toolbars.values()]

    def layout(self):
        '''
        Fix toolbars positions in the window to all toolbars were visible.
        '''
        mainWindowWidth = self._mainWindow.GetClientSize()[0]
        if mainWindowWidth == 0:
            return

        for name, toolbar_info in self._toolbars.items():
            toolbar = toolbar_info.toolbar
            toolbar_rect = toolbar.GetRect()
            if toolbar_rect.GetLeft() >= mainWindowWidth:
                self._moveToolbar(name)

        self._packToolbarsRows()
        self._mainWindow.UpdateAuiManager()

    def _getPaneInfo(self, name):
        auiManager = self._mainWindow.auiManager
        toolbar = self[name]
        pane_info = auiManager.GetPane(toolbar)
        return pane_info

    def _getToolbarRow(self, name):
        toolbar = self[name]
        pane_info = self._mainWindow.auiManager.GetPane(toolbar)
        return pane_info.dock_row

    def _getRowsCount(self):
        maxIndex = -1
        for name in self._toolbars:
            toolbar_row = self._getToolbarRow(name)
            if toolbar_row > maxIndex:
                maxIndex = toolbar_row

        return maxIndex + 1

    def _moveToolbarTo(self, name, row, pos):
        moved_pane_info = self._getPaneInfo(name)
        moved_pane_info.Position(pos).Row(row)

        moved_toolbar = self[name]
        moved_toolbar.updatePaneInfo()

    def _packToolbarsRows(self):
        '''
        Remove unused rows numbers
        '''
        rows = [1] * self._getRowsCount()

        for name in self._toolbars:
            toolbar_row = self._getToolbarRow(name)
            rows[toolbar_row] = 0

        for name in self._toolbars:
            toolbar = self[name]
            toolbar_row = self._getToolbarRow(name)
            delta = sum(rows[:toolbar_row])
            if delta == 0:
                continue

            row_new = toolbar_row - delta

            pane_info = self._getPaneInfo(name)
            pane_info.Row(row_new)
            toolbar.updatePaneInfo()

    def _getRowSpaces(self, moved_toolbar_name):
        mainWindowWidth = self._mainWindow.GetClientSize()[0]

        # Calculate empty space for each row
        rows_spaces = [-1] * self._getRowsCount()
        for toolbar_name in self._toolbars:
            if toolbar_name == moved_toolbar_name:
                continue

            toolbar = self[toolbar_name]
            toolbar_rect = toolbar.GetRect()
            toolbar_row = self._getToolbarRow(toolbar_name)
            space = mainWindowWidth - toolbar_rect.GetRight()

            if (rows_spaces[toolbar_row] == -1 or
                    space < rows_spaces[toolbar_row]):
                rows_spaces[toolbar_row] = space

        return rows_spaces

    def _moveToolbar(self, name):
        '''
        Find location for toolbar and move it there.
        '''
        margin = 24
        mainWindowWidth = self._mainWindow.GetClientSize()[0]

        # Calculate empty space for each row
        rows_spaces = self._getRowSpaces(name)

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
            toolbar_pos = mainWindowWidth - rows_spaces[row_index] + 1

        self._moveToolbarTo(name, row_index, toolbar_pos)
