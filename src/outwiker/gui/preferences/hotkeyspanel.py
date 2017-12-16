# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
from outwiker.gui.controls.hotkeyctrl import HotkeyCtrl, EVT_HOTKEY_EDIT
from outwiker.core.commands import MessageBox


class HotKeysPanel(BasePrefPanel):
    """
    Панель с настройками, связанными с редактором
    """
    def __init__(self, parent):
        super(type(self), self).__init__(parent)

        # Новые горячие клавиши
        # Ключ - strid, значение - горячая клавиша
        self.__hotkeys = {}

        self.__createGui()
        self.LoadState()

        self.__filterText.Bind(wx.EVT_TEXT, self.__onFilterEdit)
        self.__actionsList.Bind(wx.EVT_LISTBOX, self.__onActionSelect)
        self.__hotkeyCtrl.Bind(EVT_HOTKEY_EDIT, self.__onHotkeyEdit)
        self._setScrolling()

    def __onHotkeyEdit(self, event):
        newActionStrId = self.__getSelectedStrid()
        if newActionStrId is None:
            return

        newhotkey = event.hotkey
        oldActionStrId = self.__findConflict(newhotkey)

        if oldActionStrId is not None:
            newAction = Application.actionController.getTitle(newActionStrId)
            oldAction = Application.actionController.getTitle(oldActionStrId)

            text = _(u'{hotkey} hotkey assigned for "{old}".\nAssign this hotkey for "{new}"?').format(
                hotkey=newhotkey,
                old=oldAction,
                new=newAction)

            if (MessageBox(text,
                           _(u'Hotkeys conflict'),
                           wx.ICON_QUESTION | wx.YES | wx.NO) == wx.YES):
                self.__hotkeys[oldActionStrId] = None
            else:
                self.__hotkeyCtrl.SetValue(self.__hotkeys[newActionStrId])
                return

        self.__hotkeys[newActionStrId] = newhotkey

    def __getSelectedStrid(self):
        """
        Возвращает strid выбранного действия или None,
        если в списке ничего не выбрано
        """
        index = self.__actionsList.GetSelection()
        if index == wx.NOT_FOUND:
            return None

        return self.__actionsList.GetClientData(index)

    def __createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableRow(0)
        # mainSizer.AddGrowableRow(3)
        mainSizer.AddGrowableCol(0)

        # Список с именами actions
        self.__actionsList = wx.ListBox(self)
        self.__actionsList.SetMinSize((200, -1))

        # Фильтр
        filterSizer = wx.FlexGridSizer(cols=2)
        filterSizer.AddGrowableCol(1)

        filterLabel = wx.StaticText(self, label=_(u'Search'))
        self.__filterText = wx.TextCtrl(self)

        filterSizer.Add(filterLabel,
                        flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                        border=2)

        filterSizer.Add(self.__filterText,
                        flag=wx.EXPAND | wx.ALL,
                        border=2)

        # Sizer for hotkey and label for it
        hotkeySizer = wx.FlexGridSizer(cols=2)
        hotkeySizer.AddGrowableCol(1)

        # Comment to hotkeysCtrl
        hotkeyLabel = wx.StaticText(
            self,
            -1,
            _(u'Hot key.\nPress the Backspace key to clear'))

        # Горячая клавиша
        self.__hotkeyCtrl = HotkeyCtrl(self)
        self.__hotkeyCtrl.Disable()
        self.__hotkeyCtrl.SetMinSize((200, -1))

        hotkeySizer.Add(hotkeyLabel,
                        flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                        border=2)

        hotkeySizer.Add(
            self.__hotkeyCtrl,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_RIGHT,
            border=2)

        # Описание action
        self.__descriptionText = wx.TextCtrl(
            self,
            style=wx.TE_WORDWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.__descriptionText.SetMinSize((-1, 75))
        self.__descriptionText.Disable()

        mainSizer.Add(self.__actionsList, flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add(self.__descriptionText,
                      flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add(filterSizer, flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add(hotkeySizer, flag=wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(mainSizer)

    def __findConflict(self, hotkey):
        if hotkey is None or hotkey.isEmpty():
            return None

        stridCurrent = self.__getSelectedStrid()

        for strid, hotkeyCurrent in self.__hotkeys.items():
            if stridCurrent == strid or hotkey is None:
                continue
            if hotkey == hotkeyCurrent:
                return strid

        return None

    def LoadState(self):
        self.__fillActionsList()
        self.__initHotKeys()

    def __initHotKeys(self):
        """
        Заполнить словарь __hotkeys текущими значениями
        """
        actionController = Application.actionController
        strIdList = actionController.getActionsStrId()
        for strid in strIdList:
            self.__hotkeys[strid] = actionController.getHotKey(strid)

    def __onFilterEdit(self, event):
        self.__fillActionsList()

    def __onActionSelect(self, event):
        self.__descriptionText.Value = u""

        strid = event.GetClientData()
        if strid is not None:
            self.__descriptionText.Value = Application.actionController.getAction(strid).description
            self.__hotkeyCtrl.Enable()
            self.__hotkeyCtrl.SetValue(self.__hotkeys[strid])

    def __fillActionsList(self):
        """
        Заполнить список actions зарегистрированными действиями
        """
        actionController = Application.actionController
        strIdList = actionController.getActionsStrId()

        # Список кортежей(заголовок, strid)
        # Отбросим те actions, что не удовлетворяют фильтру
        titleStridList = [
           (actionController.getTitle(strid), strid)
           for strid in strIdList
           if self.__filter(actionController.getAction(strid))
        ]
        titleStridList.sort()

        self.__actionsList.Clear()
        for(title, strid) in titleStridList:
            self.__actionsList.Append(title, strid)

    def __filter(self, action):
        if len(self.__filterText.Value.strip()) == 0:
            return True

        filterText = self.__filterText.Value.lower()

        return (filterText in action.title.lower() or
                filterText in action.description.lower())

    def Save(self):
        actionController = Application.actionController

        for strid, hotkey in self.__hotkeys.items():
            if actionController.getHotKey(strid) != hotkey:
                actionController.setHotKey(strid, hotkey, True)
