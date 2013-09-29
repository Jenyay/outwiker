#!/usr/bin/python
# -*- coding: UTF-8 -*-


import wx


class ActionInfo (object):
    """
    Класс для внутреннего использования в WxActionController
    Хранит информацию о добавленных действиях
    """
    def __init__ (self, action, hotkey):
        """
        action - действие
        menuItem - пункт меню, связанный с действием
        """
        self.action = action
        self.hotkey = hotkey
        self.menuItem = None
        self.toolbar = None
        self.toolItemId = None


class WxActionController (object):
    """
    Класс для управления Actions - добавление / удаление пунктов меню и кнопок на панели инструментов
    """
    def __init__ (self, mainWindow):
        self._mainWindow = mainWindow

        # Словарь для хранения информации о действиях
        # Ключ - строковый идентификатор действия, значение - экземпляр класса ActionInfo
        self._actionsInfo = {}


    def getActionsStrId (self):
        """
        Возвращает все зарегистрированные strid
        """
        return self._actionsInfo.keys()


    def getAction (self, strid):
        return self._actionsInfo[strid].action


    def getActionInfo (self, strid):
        """
        Возвращает всю информацию о зарегистрированном action.
        Используется только для тестирования!!!
        """
        return self._actionsInfo[strid]


    def register (self, action, hotkey=u""):
        """
        Добавить действие в словарь. При этом никаких элементов интерфейса не создается
        action - регистрируемое действие
        hotkey - горячая клавиша по умолчанию для этого действия. Если в настройках задана другая горячая клавиша, то приоритет отдается клавише из настроек
        """
        # Не должно быть одинаковых идентификаторов действий
        assert action.strid not in self._actionsInfo

        actionInfo = ActionInfo (action, hotkey)
        self._actionsInfo[action.strid] = actionInfo


    def appendMenuItem (self, strid, menu):
        """
        Добавить действие в меню menu
        Действие должно быть уже зарегистрировано с помощью метода register
        """
        newid = wx.NewId()
        action = self._actionsInfo[strid].action

        menuItem = menu.Append (newid, self._getMenuItemTitle (strid))
        self._actionsInfo[strid].menuItem = menuItem

        self._mainWindow.Bind (wx.EVT_MENU, handler=lambda event: action.run(None), id=newid)


    def appendMenuCheckItem (self, strid, menu):
        """
        Добавить действие в меню menu
        Действие должно быть уже зарегистрировано с помощью метода register
        """
        newid = wx.NewId()
        action = self._actionsInfo[strid].action

        menuItem = menu.AppendCheckItem (newid, self._getMenuItemTitle (strid))
        self._actionsInfo[strid].menuItem = menuItem

        self._mainWindow.Bind (wx.EVT_MENU, handler=lambda event: self._onCheck (action, event.Checked()), id=newid)


    def removeAction (self, strid):
        """
        Удалить действие из интерфейса.
        strid - строковый идентификатор удаляемого действия
        """
        self.removeToolbarButton (strid)
        self.removeMenuItem (strid)

        del self._actionsInfo[strid]


    def removeToolbarButton (self, strid):
        """
        Убрать кнопку с панели инструментов
        Если кнопка не была добавлена, то метод ничего не делает
        """
        actionInfo = self._actionsInfo[strid]

        if actionInfo.toolbar != None:
            toolid = self._actionsInfo[strid].toolItemId
            self._actionsInfo[strid].toolbar.DeleteTool (toolid)
            self._mainWindow.Unbind (wx.EVT_TOOL, id=toolid)
            actionInfo.toolbar = None
            actionInfo.toolItemId = None


    def removeMenuItem (self, strid):
        actionInfo = self._actionsInfo[strid]

        if actionInfo.menuItem != None:
            actionInfo.menuItem.Menu.DeleteItem (actionInfo.menuItem)
            self._mainWindow.Unbind (wx.EVT_MENU, id=actionInfo.menuItem.GetId())
            actionInfo.menuItem = None


    def appendToolbarButton (self, strid, toolbar, image, fullUpdate=True):
        """
        Добавить кнопку на панель инструментов.
        Действие уже должно быть зарегистрировано с помощью метода register
        strid - строковый идентификатор действия, для которого создается кнопка на панели инструментов
        toolbar - панель инструментов, куда будет добавлена кнопка (класс, производный от BaseToolBar)
        image - путь до картинки, которая будет помещена на кнопку
        fullUpdate - нужно ли полностью обновить панель после добавления кнопки
        """
        actionid = wx.NewId()
        buttonType = wx.ITEM_NORMAL
        action = self._actionsInfo[strid].action

        self._appendToolbarItem (strid, toolbar, image, buttonType, actionid, fullUpdate)
        self._mainWindow.Bind (wx.EVT_TOOL, handler=lambda event: action.run(None), id=actionid)


    def appendToolbarCheckButton (self, strid, toolbar, image, fullUpdate=True):
        """
        Добавить кнопку на панель инструментов.
        Действие уже должно быть зарегистрировано с помощью метода register
        strid - строковый идентификатор действия, для которого создается кнопка на панели инструментов
        toolbar - панель инструментов, куда будет добавлена кнопка (класс, производный от BaseToolBar)
        image - путь до картинки, которая будет помещена на кнопку
        fullUpdate - нужно ли полностью обновить панель после добавления кнопки
        """
        actionid = wx.NewId()
        buttonType = wx.ITEM_CHECK
        action = self._actionsInfo[strid].action

        self._appendToolbarItem (strid, toolbar, image, buttonType, actionid, fullUpdate)

        self._mainWindow.Bind (wx.EVT_TOOL, handler=lambda event: self._onCheck (action, event.Checked()), id=actionid)


    def check (self, strid, checked):
        """
        Установить или снять флажок и нажать/отжать кнопку, соответствующие действию
        """
        self._onCheck (self._actionsInfo[strid].action, checked)


    def _onCheck (self, action, checked):
        """
        Обработчик события нажатия залипающей кнопки или пункта меню с чекбоксом
        """
        # Установим флажки на соответствующем пункте меню и зажмем соответствующую кнопку
        menuItem = self._actionsInfo[action.strid].menuItem
        if (menuItem != None):
            menuItem.Check (checked)

        toolbar = self._actionsInfo[action.strid].toolbar
        if toolbar != None:
            toolbar.ToggleTool (self._actionsInfo[action.strid].toolItemId, checked)
            toolbar.Realize()

        action.run (checked)


    def _appendToolbarItem (self, strid, toolbar, image, buttonType, actionid, fullUpdate=True):
        """
        Общий метод для добавления кнопки на панель инструментов
        buttonType - тип кнопки (wx.ITEM_NORMAL для обычной кнопки и wx.ITEM_CHECK для зажимаемой кнопки)
        """
        assert strid in self._actionsInfo
        title = self._getToolbarItemTitle (strid)
        bitmap = wx.Bitmap (image)

        toolbar.AddTool(actionid,
            title,
            bitmap,
            short_help_string=title,
            kind=buttonType,
            fullUpdate=fullUpdate)

        self._actionsInfo[strid].toolbar = toolbar
        self._actionsInfo[strid].toolItemId = actionid


    def enableTools (self, strid, enabled=True):
        actionInfo = self._actionsInfo[strid]

        if actionInfo.toolItemId != None:
            actionInfo.toolbar.EnableTool (actionInfo.toolItemId, enabled)

        if actionInfo.menuItem != None:
            actionInfo.menuItem.Enable (enabled)


    def getHotKey (self, strid):
        """
        Возвращает горячую клавишу для действия по его strid
        """
        return self._actionsInfo[strid].hotkey


    def getTitle (self, strid):
        """
        Возвращает заголовок действия по его strid
        """
        return self._actionsInfo[strid].action.title


    def _getMenuItemTitle (self, strid):
        hotkey = self.getHotKey (strid)
        title = self.getTitle (strid)

        if len (hotkey) == 0:
            return title

        return u"{0}\t{1}".format (title, hotkey)


    def _getToolbarItemTitle (self, strid):
        hotkey = self.getHotKey (strid)
        title = self.getTitle (strid)

        if len (hotkey) == 0:
            return title

        return u"{0} ({1})".format (title, hotkey)
