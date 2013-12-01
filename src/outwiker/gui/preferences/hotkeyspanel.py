#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application


class HotKeysPanel (wx.Panel):
    """
    Панель с настройками, связанными с редактором
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        super (HotKeysPanel, self).__init__ (*args, **kwds)

        self.__createGui ()
        self.LoadState()


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
        self.__actionsList.Bind (wx.EVT_LISTBOX, self.__onActionSelect)

        leftSizer.Add (self.__actionsList, flag=wx.EXPAND | wx.ALL, border=2)

        # Фильтр
        self.__filterText = wx.TextCtrl (self)
        self.__filterText.Bind (wx.EVT_TEXT, self.__onFilterEdit)

        leftSizer.Add (self.__filterText, flag=wx.EXPAND | wx.ALL, border=2)


        # Сайзер для размещения элементов в парвой части: 
        # выбор горячей клавиши и описание action
        rightSizer = wx.FlexGridSizer (rows=2)
        rightSizer.AddGrowableCol (0)
        rightSizer.AddGrowableRow (0)

        # Описание action
        self.__descriptionText = wx.TextCtrl (self, 
                style=wx.TE_WORDWRAP | wx.TE_MULTILINE | wx.TE_READONLY )
        self.__descriptionText.Disable()
        self.__descriptionText.SetMinSize ((200, -1))

        rightSizer.Add (self.__descriptionText, flag=wx.EXPAND | wx.ALL, border=2)

        mainSizer.Add (leftSizer, flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add (rightSizer, flag=wx.EXPAND | wx.ALL, border=2)
        self.SetSizer (mainSizer)


    def LoadState(self):
        self.__fillActionsList ()


    def __onFilterEdit (self, event):
        self.__fillActionsList()


    def __onActionSelect (self, event):
        self.__descriptionText.Value = u""

        strid = event.GetClientData()
        if strid != None:
            self.__descriptionText.Value = Application.actionController.getAction(strid).description


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
        pass

