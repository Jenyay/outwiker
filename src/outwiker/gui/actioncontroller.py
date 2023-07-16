# -*- coding: utf-8 -*-

import logging
from typing import List, Optional, Tuple, Dict

import wx

from outwiker.gui.controls.toolbar2 import ToolBar2
from outwiker.gui.hotkey import HotKey
from outwiker.gui.hotkeyoption import HotKeyOption
from outwiker.gui.hotkeyparser import HotKeyParser


logger = logging.getLogger('outwiker.gui.actioncontroller')


class ActionInfoInternal(object):
    """
    Класс для внутреннего использования в ActionController
    Хранит информацию о добавленных действиях
    """

    def __init__(self,
                 action,
                 hotkey: Optional[HotKey],
                 area: Optional[str],
                 hidden: bool = False):
        """
        action - действие
        """
        self.action = action
        self.hotkey = hotkey
        self.area = area
        self.hidden = hidden
        self.menuItem = None
        self.toolbar = None
        self.toolItemId = None

        # Used for hotkey binding
        self.hotkeyId = None
        self.isHotkeyActive = False

        # Window, which is assigned to a hotkey
        self.window = None


class ActionController:
    """
    Класс для управления Actions - добавление / удаление пунктов меню
    и кнопок на панели инструментов
    """

    def __init__(self, mainWindow: wx.Window, config):
        self._mainWindow = mainWindow
        self._config = config

        # Словарь для хранения информации о действиях
        # Ключ - строковый идентификатор действия,
        # значение - экземпляр класса ActionInfoInternal
        self._actionsInfo = {}          # type: Dict[str, ActionInfoInternal]

        self._configSection = "HotKeys"
        self._enabledGui = True

    def enableGui(self, enabled):
        self._enabledGui = enabled

    def destroy(self):
        self._mainWindow = None
        self._config = None
        self._actionsInfo = {}

    @property
    def configSection(self):
        return self._configSection

    def getActionsStrId(self):
        """
        Возвращает все зарегистрированные strid
        """
        return list(self._actionsInfo.keys())

    def getAction(self, strid):
        return self._actionsInfo[strid].action

    def getActionInfo(self, strid):
        """
        Возвращает всю информацию о зарегистрированном action.
        Используется только для тестирования!!!
        """
        return self._actionsInfo[strid]

    def register(self,
                 action,
                 hotkey: HotKey = None,
                 area: str = None,
                 hidden: bool = False):
        """
        Добавить действие в словарь.
        При этом никаких элементов интерфейса не создается
        action - регистрируемое действие
        hotkey - горячая клавиша по умолчанию для этого действия
        (Экземпляр класса HotKey).
        Если в настройках задана другая горячая клавиша,
        то приоритет отдается клавише из настроек
        """
        # Не должно быть одинаковых идентификаторов действий
        assert action.stringId not in self._actionsInfo

        actionInfo = ActionInfoInternal(
            action,
            hotkey=self._getHotKeyForAction(action, hotkey),
            area=area,
            hidden=hidden
        )
        self._actionsInfo[action.stringId] = actionInfo
        logging.debug('Action registered: "%s" (%s)',
                      action.title, str(hotkey))

    def _getHotKeyForAction(self, action, defaultHotKey: Optional[HotKey]) -> HotKey:
        """
        Получить горячую клавишу.
        Горячая клавиша берется из конфига, или defaultHotKey
        """
        return HotKeyOption(self._config,
                            self.configSection,
                            action.stringId,
                            defaultHotKey).value

    def appendMenuItem(self, strid, menu):
        """
        Добавить действие в меню menu
        Действие должно быть уже зарегистрировано с помощью метода register
        """
        if not self._enabledGui:
            return 

        menuItem = menu.Append(wx.ID_ANY, self._getMenuItemTitle(strid))
        self._actionsInfo[strid].menuItem = menuItem

        self._mainWindow.Bind(wx.EVT_MENU,
                              handler=self._onMenuItemHandler,
                              id=menuItem.GetId())

    def appendMenuCheckItem(self, strid, menu):
        """
        Добавить действие в меню menu
        Действие должно быть уже зарегистрировано с помощью метода register
        """
        if not self._enabledGui:
            return 

        menuItem = menu.AppendCheckItem(wx.ID_ANY,
                                        self._getMenuItemTitle(strid))
        self._actionsInfo[strid].menuItem = menuItem

        self._mainWindow.Bind(wx.EVT_MENU,
                              handler=self._onCheckMenuItemHandler,
                              id=menuItem.GetId())

    def saveHotKeys(self):
        """
        Сохранить все горячие клавиши в конфиг
        """
        for actionInfo in self._actionsInfo.values():
            option = HotKeyOption(self._config,
                                  self.configSection,
                                  actionInfo.action.stringId,
                                  None)
            option.value = actionInfo.hotkey

    def changeHotkeys(self, newHotkeys: List[Tuple[str, HotKey]]):
        '''
        newHotkeys - list of tuples with two elements: action id and hotkey for the strid
        '''
        for strid, hotkey in newHotkeys:
            actionInfo = self._actionsInfo[strid]
            if actionInfo.hotkey == hotkey:
                continue

            actionInfo.hotkey = hotkey

            if actionInfo.isHotkeyActive:
                self._unbindHotkey(actionInfo)
                self._bindHotkey(actionInfo)

            if actionInfo.menuItem is not None:
                actionInfo.menuItem.SetItemLabel(self._getMenuItemTitle(strid))

            if (actionInfo.toolbar is not None and
                    actionInfo.toolItemId is not None):
                title = self._getToolbarItemTitle(strid)
                actionInfo.toolbar.SetToolShortHelp(actionInfo.toolItemId,
                                                    title)

        self._updateAcceleratorTables()
        self.saveHotKeys()

    def _bindHotkey(self, actionInfo: ActionInfoInternal):
        if actionInfo.hotkey is not None:
            assert actionInfo.window is not None
            hotkeyId = wx.NewIdRef()
            actionInfo.hotkeyId = hotkeyId
            logger.debug('Bind hotkey for action "%s": "%s"',
                         actionInfo.action.title,
                         str(actionInfo.hotkey))
            actionInfo.window.Bind(wx.EVT_MENU,
                                   handler=self._onHotKeyItemHandler,
                                   id=hotkeyId)

    def _unbindHotkey(self, actionInfo: ActionInfoInternal):
        if actionInfo.hotkeyId is not None:
            logger.debug('Unbind hotkey for action "%s": "%s"',
                         actionInfo.action.title,
                         str(actionInfo.hotkey))
            actionInfo.window.Unbind(wx.EVT_MENU,
                                     handler=self._onHotKeyItemHandler,
                                     id=actionInfo.hotkeyId)
            actionInfo.hotkeyId = None

    def appendHotkey(self, strid: str, window: wx.Window = None):
        """
        Create hotkey binding for action
        """
        if not self._enabledGui:
            return 

        actionInfo = self._actionsInfo[strid]
        actionInfo.isHotkeyActive = True
        actionInfo.window = window if window is not None else self._mainWindow
        if actionInfo.hotkey is not None:
            self._bindHotkey(actionInfo)
            self._updateAcceleratorTables()

    def removeHotkey(self, strid):
        actionInfo = self._actionsInfo.get(strid)
        if actionInfo is not None:
            if actionInfo.hotkeyId is not None:
                self._unbindHotkey(actionInfo)
                self._updateAcceleratorTables()

            actionInfo.isHotkeyActive = False
            actionInfo.window = None

    def _updateAcceleratorTables(self):
        # Key - window, value - list of the wx.AcceleratorEntry instances
        entries = {}

        for actionInfo in self._actionsInfo.values():
            if actionInfo.hotkeyId is not None:
                assert actionInfo.hotkey is not None
                entry = wx.AcceleratorEntry(cmd=actionInfo.hotkeyId)
                entry.FromString(str(actionInfo.hotkey))
                if entry.IsOk():
                    if actionInfo.window not in entries:
                        entries[actionInfo.window] = []

                    entries[actionInfo.window].append(entry)

        for window in entries.keys():
            accelTable = wx.AcceleratorTable(entries[window])
            window.SetAcceleratorTable(accelTable)

    def removeAction(self, strid):
        """
        Удалить действие из интерфейса.
        strid - строковый идентификатор удаляемого действия
        """
        self.removeGui(strid)
        del self._actionsInfo[strid]

    def removeGui(self, strid):
        self.removeToolbarButton(strid)
        self.removeMenuItem(strid)
        self.removeHotkey(strid)

    def removeToolbarButton(self, strid):
        """
        Убрать кнопку с панели инструментов
        Если кнопка не была добавлена, то метод ничего не делает
        """
        if strid in self._actionsInfo:
            actionInfo = self._actionsInfo[strid]

            if actionInfo.toolbar is not None:
                toolid = actionInfo.toolItemId
                toolbar = actionInfo.toolbar
                if issubclass(type(toolbar), ToolBar2):
                    toolbar.DeleteTool(toolid)
                elif issubclass(type(toolbar), wx.ToolBar):
                    toolbar.DeleteTool(toolid)
                else:
                    raise ValueError(u'Invalid toolbar type')

                self._mainWindow.Unbind(wx.EVT_TOOL, id=toolid)
                actionInfo.toolbar = None
                actionInfo.toolItemId = None

    def removeMenuItem(self, strid):
        if strid in self._actionsInfo:
            actionInfo = self._actionsInfo[strid]

            if actionInfo.menuItem is not None:
                self._mainWindow.Unbind(wx.EVT_MENU,
                                        id=actionInfo.menuItem.GetId())
                actionInfo.menuItem.Menu.DestroyItem(actionInfo.menuItem)
                actionInfo.menuItem = None

    def appendToolbarButton(self, strid, toolbar, image, fullUpdate=True):
        """
        Добавить кнопку на панель инструментов.
        Действие уже должно быть зарегистрировано с помощью метода register
        strid - строковый идентификатор действия, для которого создается
            кнопка на панели инструментов
        toolbar - панель инструментов, куда будет добавлена кнопка
            (класс, производный от ToolBar)
        image - путь до картинки, которая будет помещена на кнопку
        fullUpdate - нужно ли полностью обновить панель после добавления кнопки
        """
        if not self._enabledGui:
            return 

        assert strid in self._actionsInfo
        title = self._getToolbarItemTitle(strid)
        bitmap = wx.Bitmap(image)

        if issubclass(type(toolbar), ToolBar2):
            toolbarItemId = toolbar.AddButton(title, bitmap, wx.ID_ANY)
        elif issubclass(type(toolbar), wx.ToolBar):
            toolbarItem = toolbar.AddTool(wx.ID_ANY,
                                          title,
                                          bitmap,
                                          wx.NullBitmap,
                                          wx.ITEM_NORMAL,
                                          title,
                                          "")
            toolbarItemId = toolbarItem.GetId()
        else:
            raise ValueError(u'Invalid toolbar type')

        self._actionsInfo[strid].toolbar = toolbar
        self._actionsInfo[strid].toolItemId = toolbarItemId

        self._mainWindow.Bind(wx.EVT_TOOL,
                              handler=self._onToolItemHandler,
                              id=toolbarItemId)
        if fullUpdate:
            toolbar.Realize()

    def updateToolbars(self):
        if not self._enabledGui:
            return 

        toolbars = set([action_info.toolbar
                        for action_info in self._actionsInfo.values()
                        if action_info.toolbar is not None])

        for toolbar in toolbars:
            toolbar.Realize()

    def appendToolbarCheckButton(self, strid, toolbar, image,
                                 fullUpdate=True):
        """
        Добавить кнопку на панель инструментов.
        Действие уже должно быть зарегистрировано с помощью метода register
        strid - строковый идентификатор действия,
            для которого создается кнопка на панели инструментов
        toolbar - панель инструментов, куда будет добавлена кнопка
            (класс, производный от ToolBar)
        image - путь до картинки, которая будет помещена на кнопку
        fullUpdate - нужно ли полностью обновить панель после добавления кнопки
        """
        if not self._enabledGui:
            return 

        assert strid in self._actionsInfo
        title = self._getToolbarItemTitle(strid)
        bitmap = wx.Bitmap(image)

        if issubclass(type(toolbar), ToolBar2):
            toolbarItemId = toolbar.AddCheckButton(title, bitmap, wx.ID_ANY)
        elif issubclass(type(toolbar), wx.ToolBar):
            toolbarItem = toolbar.AddTool(wx.ID_ANY,
                                          title,
                                          bitmap,
                                          wx.NullBitmap,
                                          wx.ITEM_CHECK,
                                          title,
                                          "")
            toolbarItemId = toolbarItem.GetId()
        else:
            raise ValueError(u'Invalid toolbar type')

        self._actionsInfo[strid].toolbar = toolbar
        self._actionsInfo[strid].toolItemId = toolbarItemId

        self._mainWindow.Bind(wx.EVT_TOOL,
                              handler=self._onCheckToolItemHandler,
                              id=toolbarItemId)
        if fullUpdate:
            toolbar.Realize()

    def check(self, strid, checked):
        """
        Установить или снять флажок и нажать/отжать кнопку,
        соответствующие действию
        """
        self._onCheck(self._actionsInfo[strid].action, checked)

    def _getActionInfoByMenuItemId(self, menuItemId) -> Optional[ActionInfoInternal]:
        for actionInfo in self._actionsInfo.values():
            if (actionInfo.menuItem is not None and
                    actionInfo.menuItem.GetId() == menuItemId):
                return actionInfo

        return None

    def _getActionInfoByToolItemId(self, toolItemId) -> Optional[ActionInfoInternal]:
        for actionInfo in self._actionsInfo.values():
            if (actionInfo.toolItemId is not None and
                    actionInfo.toolItemId == toolItemId):
                return actionInfo

        return None

    def _getActionInfoByHotkeyId(self, itemId) -> Optional[ActionInfoInternal]:
        for actionInfo in self._actionsInfo.values():
            if (actionInfo.hotkeyId is not None and
                    actionInfo.hotkeyId == itemId):
                return actionInfo

        return None

    def _onCheckMenuItemHandler(self, event):
        actionInfo = self._getActionInfoByMenuItemId(event.GetId())
        assert actionInfo is not None
        self._onCheck(actionInfo.action, event.IsChecked())

    def _onCheckToolItemHandler(self, event):
        actionInfo = self._getActionInfoByToolItemId(event.GetId())
        assert actionInfo is not None
        self._onCheck(actionInfo.action, event.IsChecked())

    def _onMenuItemHandler(self, event):
        actionInfo = self._getActionInfoByMenuItemId(event.GetId())
        assert actionInfo is not None
        logger.debug('Run action with menu item: %s', actionInfo.action.title)
        actionInfo.action.run(None)

    def _onHotKeyItemHandler(self, event):
        actionInfo = self._getActionInfoByHotkeyId(event.GetId())
        assert actionInfo is not None

        logger.debug('Run action with hotkey: %s', actionInfo.action.title)
        actionInfo.action.run(None)

    def _onToolItemHandler(self, event):
        actionInfo = self._getActionInfoByToolItemId(event.GetId())
        assert actionInfo is not None
        logger.debug('Run action with tool button: %s',
                     actionInfo.action.title)
        actionInfo.action.run(None)

    def _onCheck(self, action, checked):
        """
        Run the checked action and refresh tool item
        """
        # Установим флажки на соответствующем пункте меню
        menuItem = self._actionsInfo[action.stringId].menuItem
        if (menuItem is not None):
            menuItem.Check(checked)

        toolbar = self._actionsInfo[action.stringId].toolbar
        if toolbar is not None:
            toolbar.ToggleTool(self._actionsInfo[action.stringId].toolItemId,
                               checked)
            toolbar.Refresh()

        action.run(checked)

    def enableTools(self, strid, enabled=True):
        if not self._enabledGui:
            return 

        actionInfo = self._actionsInfo[strid]

        if actionInfo.toolItemId is not None:
            actionInfo.toolbar.EnableTool(actionInfo.toolItemId, enabled)

        if actionInfo.menuItem is not None:
            actionInfo.menuItem.Enable(enabled)

    def getHotKey(self, strid):
        """
        Возвращает горячую клавишу для действия по его strid
        """
        return self._actionsInfo[strid].hotkey

    def getTitle(self, strid):
        """
        Возвращает заголовок действия по его strid
        """
        return self._actionsInfo[strid].action.title

    def getArea(self, strid):
        return self._actionsInfo[strid].area

    def isHidden(self, strid):
        return self._actionsInfo[strid].hidden

    def _getMenuItemTitle(self, strid):
        hotkey = self.getHotKey(strid)
        title = self.getTitle(strid)

        if hotkey is None:
            return title

        return '{0}\t{1}'.format(title, HotKeyParser.toString(hotkey))

    def _getToolbarItemTitle(self, strid):
        hotkey = self.getHotKey(strid)
        title = self.getTitle(strid)

        if hotkey is None:
            return title

        return '{0} ({1})'.format(title, HotKeyParser.toString(hotkey))
