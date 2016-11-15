# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
from outwiker.gui.controls.hotkeyctrl import HotkeyCtrl, EVT_HOTKEY_EDIT


class HotKeysPanel (BasePrefPanel):
    """
    Панель с настройками, связанными с редактором
    """
    def __init__(self, parent):
        super (type (self), self).__init__ (parent)

        # Новые горячие клавиши
        # Ключ - strid, значение - горячая клавиша
        self.__hotkeys = {}

        self.__createGui ()
        self.LoadState()

        self.__filterText.Bind (wx.EVT_TEXT, self.__onFilterEdit)
        self.__actionsList.Bind (wx.EVT_LISTBOX, self.__onActionSelect)
        self.__hotkey.Bind (EVT_HOTKEY_EDIT, self.__onHotkeyEdit)
        self.__setHotKeyBtn.Bind(wx.EVT_BUTTON, self.__onSetHotkey)
        self._setScrolling()


    def __onHotkeyEdit (self, event):
        strid = self.__getSelectedStrid()
        if strid is not None:
            self.__hotkeys[strid] = event.hotkey
            self.__findConflicts ()


    def __getSelectedStrid (self):
        """
        Возвращает strid выбранного действия или None, если в списке ничего не выбрано
        """
        index = self.__actionsList.GetSelection ()
        if index == wx.NOT_FOUND:
            return None

        return self.__actionsList.GetClientData (index)



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
        self.__actionsList.SetMinSize ((200, -1))

        leftSizer.Add (self.__actionsList, flag=wx.EXPAND | wx.ALL, border=2)

        # Фильтр
        self.__filterText = wx.TextCtrl (self)

        leftSizer.Add (self.__filterText, flag=wx.EXPAND | wx.ALL, border=2)

        # Сайзер для размещения элементов в правой части:
        # выбор горячей клавиши и описание action
        rightSizer = wx.FlexGridSizer (cols=1)
        rightSizer.AddGrowableCol (0)
        rightSizer.AddGrowableRow (2)

        # Comment to hotkeysCtrl
        self.__hotkeyText = wx.StaticText(
            self,
            -1,
            _(u'Hot key.\nPress the Backspace key to clear'))

        # Горячая клавиша
        self.__hotkey = HotkeyCtrl(self)
        self.__hotkey.Disable()

        # Описание action
        self.__descriptionText = wx.TextCtrl (self,
                                              style=wx.TE_WORDWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.__descriptionText.SetMinSize ((200, -1))

        # Список actions с такими же горячими клавишами
        self.__conflictLabel = wx.StaticText (self, label=_(u"Actions with the same hotkey"))
        self.__conflictActionsText = wx.TextCtrl (self,
                                                  style=wx.TE_WORDWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.__conflictActionsText.SetMinSize ((-1, 100))

        # The button the set hotkey
        self.__setHotKeyBtn = wx.Button(self, label=_(u'Set hot key'))

        rightSizer.Add (self.__hotkeyText, flag=wx.EXPAND | wx.ALL, border=2)
        rightSizer.Add (self.__hotkey, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        rightSizer.Add (self.__descriptionText, flag=wx.EXPAND | wx.ALL, border=2)
        rightSizer.Add (self.__conflictLabel, flag=wx.EXPAND | wx.ALL, border=2)
        rightSizer.Add (self.__conflictActionsText, flag=wx.EXPAND | wx.ALL, border=2)
        rightSizer.Add (self.__setHotKeyBtn, flag=wx.EXPAND | wx.ALL, border=2)

        mainSizer.Add (leftSizer, flag=wx.EXPAND | wx.ALL, border=2)
        mainSizer.Add (rightSizer, flag=wx.EXPAND | wx.ALL, border=2)
        self.SetSizer (mainSizer)


    def __findConflicts (self):
        """
        Заполнить список действий с такой же горячей клавишей
        """
        self.__conflictActionsText.Value = u""
        stridCurrent = self.__getSelectedStrid ()
        hotkeyCurrent = self.__hotkey.GetValue()

        for strid, hotkey in self.__hotkeys.iteritems():
            if stridCurrent == strid or hotkey is None:
                continue
            if hotkey == hotkeyCurrent:
                self.__conflictActionsText.Value += Application.actionController.getTitle (strid) + "\n"


    def LoadState(self):
        self.__fillActionsList()
        self.__initHotKeys()
        self.__findConflicts()


    def __initHotKeys (self):
        """
        Заполнить словарь __hotkeys текущими значениями
        """
        actionController = Application.actionController
        strIdList = actionController.getActionsStrId()
        for strid in strIdList:
            self.__hotkeys[strid] = actionController.getHotKey(strid)


    def __onFilterEdit (self, event):
        self.__fillActionsList()


    def __onActionSelect (self, event):
        self.__descriptionText.Value = u""

        strid = event.GetClientData()
        if strid is not None:
            self.__descriptionText.Value = Application.actionController.getAction(strid).description
            self.__hotkey.Enable()
            self.__hotkey.SetValue(self.__hotkeys[strid])
            self.__findConflicts ()


    def __fillActionsList (self):
        """
        Заполнить список actions зарегистрированными действиями
        """
        actionController = Application.actionController
        strIdList = actionController.getActionsStrId()

        # Список кортежей (заголовок, strid)
        # Отбросим те actions, что не удовлетворяют фильтру
        titleStridList = [
            (actionController.getTitle (strid), strid)
            for strid in strIdList
            if self.__filter (actionController.getAction (strid))
        ]
        titleStridList.sort()

        self.__actionsList.Clear()
        for (title, strid) in titleStridList:
            self.__actionsList.Append (title, strid)


    def __filter (self, action):
        if len (self.__filterText.Value.strip()) == 0:
            return True

        filterText = self.__filterText.Value.lower()

        return (filterText in action.title.lower() or
                filterText in action.description.lower())

    def __onSetHotkey(self, event):
        from outwiker.actions.preferences import PreferencesAction

        stridCurrent = self.__getSelectedStrid()
        hotkeyCurrent = self.__hotkey.GetValue()

        # Не будем менять до перезапуска горячую клавишу для вызова настроек.
        # Это связано с тем, что потом придется удалять этот пункт меню, чтобы
        # расставить подчеркивания с помощью Shortcuter, но возникнут проблемы,
        # т.к. в это место кода мы попадаем из обработчика события, связанного
        # с этим пунктом меню
        Application.actionController.setHotKey(
            stridCurrent,
            hotkeyCurrent,
            stridCurrent != PreferencesAction.stringId)

        for strid, hotkey in self.__hotkeys.iteritems():
            if hotkey == hotkeyCurrent and stridCurrent != strid:
                Application.actionController.setHotKey(
                    strid,
                    None,
                    strid != PreferencesAction.stringId)
        self.__initHotKeys()
        self.__findConflicts()

    def Save(self):
        pass
