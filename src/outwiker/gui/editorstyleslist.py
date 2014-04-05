#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

class EditorStylesList (wx.Panel):
    """
    Класс контрола для редактирования стилей редактора (цвет шрифта, жирность и т.п., цвет фона пока менять не будем)
    """
    def __init__ (self, parent):
        super (EditorStylesList, self).__init__ (parent)

        self.__createGui ()
        self.__layout()

        self._styles = []


    def __createGui (self):
        self._stylesList = wx.ListBox (self, style = wx.LB_SINGLE)
        self._stylesList.SetMinSize ((150, -1))

        self._colorPicker = wx.ColourPickerCtrl (self, style=wx.CLRP_SHOW_LABEL)
        self._bold = wx.CheckBox (self, label=_(u"Bold"))
        self._italic = wx.CheckBox (self, label=_(u"Italic"))
        self._underline = wx.CheckBox (self, label=_(u"Underline"))


    def __layout (self):
        styleSizer = wx.FlexGridSizer (cols=1)
        styleSizer.AddGrowableCol (0)
        styleSizer.Add (self._colorPicker, flag=wx.ALL | wx.EXPAND, border = 2)
        styleSizer.Add (self._bold, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        styleSizer.Add (self._italic, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        styleSizer.Add (self._underline, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)

        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableRow (0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        mainSizer.Add (self._stylesList, flag = wx.EXPAND | wx.ALL, border = 2)
        mainSizer.Add (styleSizer, flag = wx.EXPAND | wx.ALL, border = 2)

        self.SetSizer (mainSizer)
        self.Layout()


    def addStyle (self, title, style):
        """
        Добавить стиль в список
        title - название стиля
        style - экземпляр класса StcStyle
        """
        self._stylesList.Append (title)
        self._styles.append (style)

        if len (self._styles) == 1:
            self._stylesList.SetSelection (0)
