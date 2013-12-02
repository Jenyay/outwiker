#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx


class HotkeyEditor (wx.Panel):
    """Контрол для представления и редактирвоания горячей клавиши"""
    def __init__(self, parent):
        super(HotkeyEditor, self).__init__(parent)

        hotkeys = r"""F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12
0 1 2 3 4 5 6 7 8 9
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z,
Insert Enter Delete Home End Pageup Pagedown 
Up Down Left Right
/ \ * - + . _ = `"""

        self._hotkeysList = [_("None")] + [item for item in hotkeys.split() if len (item) != 0]

        self.__createGui()


    def setHotkey (self, hotkey):
        """
        Установить горячую клавишу для контрола
        hotkey - экземпляр класса HotKey или None
        """
        self.clear()
        if hotkey == None:
            return

        self._ctrl.Value = hotkey.ctrl
        self._shift.Value = hotkey.shift
        self._alt.Value = hotkey.alt


    def clear (self):
        self._ctrl.Value = False
        self._alt.Value = False
        self._shift.Value = False
        self._key.SetSelection (0)


    def __createGui (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        self._ctrl = wx.CheckBox (self, label=_(u"Ctrl"))
        self._shift = wx.CheckBox (self, label=_(u"Shift"))
        self._alt = wx.CheckBox (self, label=_(u"Alt"))

        self._key = wx.ComboBox (self, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self._key.AppendItems (self._hotkeysList)
        self._key.SetSelection (0)

        mainSizer.Add (self._ctrl, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.AddSpacer (1)
        mainSizer.Add (self._shift, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.Add (self._key, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=2)
        mainSizer.Add (self._alt, flag=wx.ALL | wx.EXPAND, border=2)

        self.SetSizer (mainSizer)
        self.Layout()
