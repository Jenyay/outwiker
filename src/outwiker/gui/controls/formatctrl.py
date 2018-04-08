# -*- coding: utf-8 -*-

import wx


class FormatCtrl(wx.Panel):
    """
    Контрол для ввода форматов данных с кнопкой-подсказкой
    """
    def __init__(self, parent, defaultFormat, hintsList, hintButtonBitmap):
        """
        defaultFormat - значение по умолчанию
        hintsList - список кортежей. Первый элемент - подстановочный символ,
            второй элемент - комментарий
        hintButtonBitmap - Картинка для кнопки - экземпляр класса wx.Bitmap
        """
        super(FormatCtrl, self).__init__(parent)

        # Список кортежей.
        # Первый элемент - подстановочный символ
        # Второй элемент - комментарий
        self._hints = hintsList[:]

        # Ключ - ID пункта меню, значение - элемент списка self._hints
        self._menuItemsId = {}

        self.formatCtrl = wx.TextCtrl(self, -1, defaultFormat)
        self.hintBtn = wx.BitmapButton(self, wx.ID_ANY, hintButtonBitmap)

        self.__createMenu()
        self.__layout()

        self.hintBtn.Bind(wx.EVT_BUTTON, self.__onHintClick)
        self.hintBtn.Bind(wx.EVT_MENU, self.__onHintMenuClick)

    def __onHintMenuClick(self, event):
        hint = self._menuItemsId[event.GetId()]
        (sel_from, sel_to) = self.formatCtrl.GetSelection()
        self.formatCtrl.Replace(sel_from, sel_to, hint[0])
        self.formatCtrl.SetFocus()
        self.formatCtrl.SetSelection(sel_from + len(hint[0]),
                                     sel_from + len(hint[0]))

    def GetValue(self):
        return self.formatCtrl.GetValue()

    def SetValue(self, text):
        self.formatCtrl.SetValue(text)

    def __onHintClick(self, event):
        self.hintBtn.PopupMenu(self._menu)

    def __createMenu(self):
        self._menu = wx.Menu()
        self._menuItemsId = {}

        for hint in self._hints:
            text = u"{0} - {1}".format(hint[0], hint[1])
            newid = self._menu.Append(wx.ID_ANY, text).GetId()
            self._menuItemsId[newid] = hint

    def __layout(self):
        mainSizer = wx.FlexGridSizer(1, 2, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(self.formatCtrl,
                      0,
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                      border=2)
        mainSizer.Add(self.hintBtn,
                      0,
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
                      border=0)

        self.SetSizer(mainSizer)
