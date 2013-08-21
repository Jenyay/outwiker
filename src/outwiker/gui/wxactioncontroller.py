#!/usr/bin/python
# -*- coding: UTF-8 -*-


import wx


class ActionInfo (object):
    """
    Класс для внутреннего использования в WxActionController
    Хранит информацию о добавленных действиях
    """
    def __init__ (self, action, parentMenu, menuItem):
        """
        action - действие
        parentMenu - меню, куда добавляется пункт действия
        menuItem - пункт меню, связанный с действием
        """
        self.action = action
        self.parentMenu = parentMenu
        self.menuItem = menuItem


class WxActionController (object):
    """
    Класс для управления Actions - добавление / удаление пунктов меню и кнопок на панели инеструментов
    """
    def __init__ (self, mainWindow):
        self._mainWindow = mainWindow

        # Словарь для хранения информации о действиях
        # Ключ - строковый идентификатор действия, значение - экземпляр класса ActionInfo
        self._actionsInfo = {}


    def appendAction (self, action, menu):
        """
        Добавить действие в меню menu
        """
        newid = wx.NewId()
        menuItem = menu.Append (newid, action.title)

        actionInfo = ActionInfo (action, menu, menuItem)
        self._mainWindow.Bind (wx.EVT_MENU, handler=lambda event: action.run(), id=newid)

        # Не должно быть одинаковых идентификаторов действий
        assert action.strid not in self._actionsInfo
        self._actionsInfo[action.strid] = actionInfo


    def removeAction (self, actionStrId):
        """
        Удалить действие из интерфейса.
        actionStrId - строковый идентификатор удаляемого действия
        """
        assert actionStrId in self._actionsInfo

        actionInfo = self._actionsInfo[actionStrId]
        actionInfo.parentMenu.DeleteItem (actionInfo.menuItem)
