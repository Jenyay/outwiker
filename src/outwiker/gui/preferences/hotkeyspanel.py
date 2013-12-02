#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.hotkeyeditor import HotkeyEditor, EVT_HOTKEY_EDIT


class HotKeysPanel (wx.Panel):
    """
    Панель с настройками, связанными с редактором
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        super (HotKeysPanel, self).__init__ (*args, **kwds)

        # Новые горячие клавиши
        # Ключ - strid, значение - горячая клавиша
        self.__hotkeys = {}

        self.__createGui ()
        self.LoadState()

        self.__filterText.Bind (wx.EVT_TEXT, self.__onFilterEdit)
        self.__actionsList.Bind (wx.EVT_LISTBOX, self.__onActionSelect)
        self.__hotkey.Bind (EVT_HOTKEY_EDIT, self.__onHotkeyEdit)


    def __onHotkeyEdit (self, event):
        index = self.__actionsList.GetSelection ()
        if index == wx.NOT_FOUND:
            return

        strid = self.__actionsList.GetClientData (index)
        self.__hotkeys[strid] = event.hotkey


    def __createGui (self):
        # Сайзер, делящий панель на две части
        # Слева будет список actions с фильтром, справа - выбранная горячая клавиша
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0, 1)
        mainSizer.AddGrowableCol (1, 1)
        mainSizer.AddGrowableRow (0)

        # Сайзер, размещающий элементы левой части панели
        # Верхняя часть - список actions
        # Нижняя часть - фильтр
        leftSizer = wx.FlexGridSizer (rows=2)
        leftSizer.AddGrowableCol (0)
        leftSizer.AddGrowableRow (0)

        # Список с именами actions
        self.__actionsList = wx.ListBox (self)

        leftSizer.Add (self.__actionsList, flag=wx.EXPAND | wx.ALL, border=2)

        # Фильтр
        self.__filterText = wx.TextCtrl (self)

        leftSizer.Add (self.__filterText, flag=wx.EXPAND | wx.ALL, border=2)


        # Сайзер для размещения элементов в правой части: 
        # выбор горячей клавиши и описание action
        rightSizer = wx.FlexGridSizer (rows=2)
        rightSizer.AddGrowableCol (0)
        rightSizer.AddGrowableRow (1)

        # Горячая клавиша
        self.__hotkey = HotkeyEditor (self)
        self.__hotkey.Disable()

        # Описание action
        self.__descriptionText = wx.TextCtrl (self, 
                style=wx.TE_WORDWRAP | wx.TE_MULTILINE | wx.TE_READONLY )
        self.__descriptionText.SetMinSize ((200, -1))

        rightSizer.Add (self.__hotkey, flag=wx.EXPAND | wx.ALL, border=2)
        rightSizer.Add (self.__descriptionText, flag=wx.EXPAND | wx.ALL, border=2)

        mainSizer.Add (leftSizer, flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add (rightSizer, flag=wx.EXPAND | wx.ALL, border=2)
        self.SetSizer (mainSizer)


    def LoadState(self):
        self.__fillActionsList ()
        self.__initHotKeys ()


    def __initHotKeys (self):
        """
        Заполнить словарь __hotkeys текущими значениями
        """
        actionController = Application.actionController
        strIdList = actionController.getActionsStrId()
        for strid in strIdList:
            self.__hotkeys[strid] = actionController.getHotKey (strid)


    def __onFilterEdit (self, event):
        self.__fillActionsList()


    def __onActionSelect (self, event):
        self.__descriptionText.Value = u""

        strid = event.GetClientData()
        if strid != None:
            self.__descriptionText.Value = Application.actionController.getAction(strid).description
            self.__hotkey.Enable()
            self.__hotkey.setHotkey (Application.actionController.getHotKey(strid))


    def __fillActionsList (self):
        """
        Заполнить список actions зарегистрированными действиями
        """
        actionController = Application.actionController
        strIdList = actionController.getActionsStrId()

        # Список кортежей (заголовок, strid)
        # Отбросим те actions, что не удовлетворяют фильтру
        titleStridList = [(actionController.getTitle (strid), strid) for strid in strIdList
                if self.__filter (actionController.getTitle (strid))]
        titleStridList.sort()

        self.__actionsList.Clear()
        for (title, strid) in titleStridList:
            self.__actionsList.Append (title, strid)


    def __filter (self, title):
        if len (self.__filterText.Value.strip()) == 0:
            return True

        return self.__filterText.Value.lower() in title.lower()


    def Save (self):
        for strid, hotkey in self.__hotkeys.iteritems():
            if Application.actionController.getHotKey (strid) != hotkey:
                Application.actionController.setHotKey (strid, hotkey)

        if Application.mainWindow != None:
            Application.mainWindow.updateShortcuts()

