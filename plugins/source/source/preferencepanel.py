#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.gui.preferences.configelements import StringElement, IntegerElement
from outwiker.core.system import getOS

from .sourceconfig import SourceConfig


class PreferencePanel (wx.Panel):
    """
    Панель с настройками
    """
    def __init__ (self, parent, config, lang):
        """
        parent - родитель панели (должен быть wx.Treebook)
        config - настройки из plugin._application.config
        lang - функция для локализации, созданная с помощью plugin._init_i18n
        """
        wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)

        self._ = lang

        self.__createGui()
        self.__controller = PrefPanelController (self, config)


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
        languageLabel = wx.StaticText(self, -1, self._(u"Default Programming Language"))
        self.languageComboBox = wx.ComboBox (self, style=wx.CB_DROPDOWN | wx.CB_READONLY )
        self.languageComboBox.SetMinSize (wx.Size (100, -1))

        mainSizer.Add (
                languageLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        mainSizer.Add (
                self.languageComboBox, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2
                )


    def __createTabWidthGui (self, mainSizer):
        """
        Создать интерфейс, связанный с размером табуляции
        """
        tabWidthLabel = wx.StaticText(self, -1, self._(u"Default Tab Width"))
        self.tabWidthSpin = wx.SpinCtrl (
                self, 
                style=wx.SP_ARROW_KEYS|wx.TE_AUTO_URL
                )
        self.tabWidthSpin.SetMinSize (wx.Size (100, -1))


        mainSizer.Add (
                tabWidthLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        mainSizer.Add (
                self.tabWidthSpin, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2
                )


    def LoadState(self):
        self.__controller.loadState()


    def Save (self):
        self.__controller.save()



class PrefPanelController (object):
    """
    Контроллер для панели настроек
    """
    def __init__ (self, owner, config):
        self.__owner = owner
        self.__config = SourceConfig (config)

        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50


    def __getLangList (self):
        """
        Прочитать список поддерживаемых языков
        """
        fname = u"languages.txt"
        cmd_folder = unicode (os.path.dirname(os.path.abspath(__file__)), getOS().filesEncoding )
        fullpath = os.path.join (cmd_folder, fname)

        try:
            with open (fullpath) as fp:
                return [item.strip() for item in fp.readlines()]
        except IOError:
            return [u"text"]


    def loadState (self):
        self.__tabWidthOption = IntegerElement (
                self.__config.tabWidth, 
                self.__owner.tabWidthSpin, 
                self.MIN_TAB_WIDTH, 
                self.MAX_TAB_WIDTH
                )

        languages = self.__getLangList()
        self.__owner.languageComboBox.Clear()
        self.__owner.languageComboBox.AppendItems (languages)

        try:
            selindex = languages.index (self.__config.defaultLanguage.value.lower().strip())
            self.__owner.languageComboBox.SetSelection (selindex)
        except ValueError:
            self.__owner.languageComboBox.SetSelection (0)


    def save (self):
        self.__tabWidthOption.save()
        self.__config.defaultLanguage.value = self.__owner.languageComboBox.GetValue()
