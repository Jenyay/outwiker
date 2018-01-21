# -*- coding: utf-8 -*-

from configparser import NoSectionError

import wx
import wx.aui

from outwiker.gui.defines import MENU_VIEW


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
    def __init__(self, mainWindow, application):
        self._mainWindow = mainWindow
        self._application = application

        # Ключ - строка для нахождения панели инструментов
        # Значение - экземпляр класса ToolBarInfo
        self._toolbars = {}

        # Подменю для показа скрытия панелей
        self._toolbarsMenu = wx.Menu()
        viewMenu = self._mainWindow.menuController[MENU_VIEW]
        viewMenu.Append(-1, _(u"Toolbars"), self._toolbarsMenu)

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

    def createToolBar(self, toolbar_id, title):
        if toolbar_id in self._toolbars:
            raise KeyError()

        toolbar = ToolBar(self._mainWindow,
                          self._mainWindow.auiManager,
                          self._application.config,
                          toolbar_id,
                          title)
        newitem = self._addMenu(toolbar)
        self._toolbars[toolbar_id] = ToolBarInfo(toolbar, newitem)
        toolbar.UpdateToolBar()
        self.layout()

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
        [toolbar.toolbar.updatePaneInfo()
         for toolbar in self._toolbars.values()]

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


class ToolBar(wx.aui.AuiToolBar):
    """
    The base class for a toolbars.
    """
    def __init__(self, parent, auiManager, config, name, caption):
        super().__init__(parent)
        self._SECTION_NAME = 'Toolbars'

        self._parent = parent
        self._auiManager = auiManager
        self._config = config
        self._name = name
        self._caption = caption
        self._pane = self._loadPaneInfo()

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

    def _createPane(self):
        return (wx.aui.AuiPaneInfo()
                .Name(self.name)
                .Caption(self.caption)
                .ToolbarPane()
                .Top()
                .Position(0)
                .Row(0))

    def _loadPaneInfo(self):
        try:
            paneinfo = self._config.get(self._SECTION_NAME, self.name)
            pane = wx.aui.AuiPaneInfo()
            self._auiManager.LoadPaneInfo(paneinfo, pane)
            pane.Caption(self.caption)
            pane.Dock()
        except (BaseException, NoSectionError):
            pane = self._createPane()

        return pane

    def savePaneInfo(self):
        paneinfo = self._auiManager.SavePaneInfo(self.pane)
        self._config.set(self._SECTION_NAME, self.name, paneinfo)

    def DeleteTool(self, toolid, fullUpdate=True):
        self.Freeze()
        super().DeleteTool(toolid)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()
        self.Thaw()

    def AddTool(self,
                tool_id,
                label,
                bitmap,
                short_help_string=wx.EmptyString,
                kind=wx.ITEM_NORMAL,
                fullUpdate=True):
        self.Freeze()
        item = super().AddTool(tool_id, label, bitmap, short_help_string, kind)
        self.UpdateToolBar()
        if fullUpdate:
            self._parent.UpdateAuiManager()
            self.updatePaneInfo()

        self.Thaw()
        return item

    @property
    def pane(self):
        return self._pane

    def updatePaneInfo(self):
        currentpane = self._auiManager.GetPane(self)
        (self.pane
         .Position(currentpane.dock_pos)
         .Row(currentpane.dock_row)
         .Direction(currentpane.dock_direction)
         .Layer(currentpane.dock_layer)
         )

    def UpdateToolBar(self):
        self.Realize()
        self._auiManager.DetachPane(self)
        self._auiManager.AddPane(self, self.pane)
        self.updatePaneInfo()

    def FindById(self, toolid):
        return self.FindTool(toolid)

    def Hide(self):
        self.updatePaneInfo()
        self.pane.Hide()
        super().Hide()

    def Show(self):
        self.pane.Show()
        super().Show()

    def Destroy(self):
        self.savePaneInfo()
        super().Destroy()
