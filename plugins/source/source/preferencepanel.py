#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

class PreferencePanel (wx.Panel):
    """
    Панель с настройками
    """
    def __init__ (self, parent):
        wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)

        self.DEFAULT_TAB_WIDTH = 4
        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50

        self.DEFAULT_LANGUAGE = u""

        self.__createGui()


    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (2, 2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        self.__createTabWidthGui (mainSizer)
        self.__createLanguageGui (mainSizer)
        self.SetSizer(mainSizer)


    def __createLanguageGui (self, mainSizer):
        """
        Создать интерфейс, связанный с языком программирования по умолчанию
        """
        languageLabel = wx.StaticText(self, -1, _("Default Programming Language"))
        self.languageTextCtrl = wx.TextCtrl (self, -1, self.DEFAULT_LANGUAGE)
        self.languageTextCtrl.SetMinSize (wx.Size (100, -1))

        mainSizer.Add (languageLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)

        mainSizer.Add (self.languageTextCtrl, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)


    def __createTabWidthGui (self, mainSizer):
        """
        Создать интерфейс, связанный с размером табуляции
        """
        tabWidthLabel = wx.StaticText(self, -1, _("Default Tab Width"))
        self.tabWidthSpin = wx.SpinCtrl(self, 
                -1, 
                str (self.DEFAULT_TAB_WIDTH), 
                min=self.MIN_TAB_WIDTH, 
                max=self.MAX_TAB_WIDTH, 
                style=wx.SP_ARROW_KEYS|wx.TE_AUTO_URL)


        mainSizer.Add (tabWidthLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)

        mainSizer.Add (self.tabWidthSpin, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)


    def LoadState(self):
        pass


    def Save (self):
        pass



class PrefPanelController (object):
    """
    Контроллер для панели настроек
    """
    def __init__ (self, owner):
        self.__owner = owner
