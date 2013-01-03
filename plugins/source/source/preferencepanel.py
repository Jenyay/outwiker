#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.gui.preferences.configelements import IntegerElement
from outwiker.core.system import getOS

from .sourceconfig import SourceConfig
from .i18n import get_
from .utilites import getLangList


class PreferencePanel (wx.Panel):
    """
    Панель с настройками
    """
    def __init__ (self, parent, config):
        """
        parent - родитель панели (должен быть wx.Treebook)
        config - настройки из plugin._application.config
        """
        wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)

        global _
        _ = get_()

        self.__createGui()
        self.__controller = PrefPanelController (self, config)


    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (0, 1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)

        languageLabel = wx.StaticText(self, -1, _(u"Used Languages"))
        mainSizer.Add (
                languageLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)

        self.__createLangGui (mainSizer)
        self.SetSizer(mainSizer)


    def __createLangGui (self, mainSizer):
        """
        Создание элементов управления, связанных с выбором используемых языков
        """
        # Сайзер для расположения списка языков и кнопок
        langSizer = wx.FlexGridSizer (0, 2)
        langSizer.AddGrowableRow (0)
        langSizer.AddGrowableCol (0)

        self.langList = wx.CheckListBox (self, -1)
        langSizer.Add (
                self.langList,
                proportion=1,
                flag = wx.ALL | wx.EXPAND,
                border=2)

        # Кнопки
        buttonsSizer = wx.BoxSizer (wx.VERTICAL)
        self.selectAllButton = wx.Button (self, label=_(u"Select All"))
        self.clearButton = wx.Button (self, label=_(u"Clear"))

        buttonsSizer.Add (
                self.selectAllButton,
                proportion=1,
                flag=wx.ALL,
                border=2)

        buttonsSizer.Add (
                self.clearButton,
                proportion=1,
                flag=wx.ALL,
                border=2)

        langSizer.Add (
                buttonsSizer,
                proportion=1,
                flag=wx.ALL,
                border=2)

        mainSizer.Add (
                langSizer,
                proportion=1,
                flag=wx.ALL | wx.EXPAND,
                border=2)


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

        self.__owner.selectAllButton.Bind (wx.EVT_BUTTON, self._onSelectAll)
        self.__owner.clearButton.Bind (wx.EVT_BUTTON, self._onClear)


    def loadState (self):
        allLanguages = self._getAllLanguages ()
        self.__owner.langList.Clear()
        self.__owner.langList.AppendItems (allLanguages)

        # Уберем языки, которых нет в списке
        selectedLanguages = [item for item in self.__config.languageList.value if item in allLanguages]

        self.__owner.langList.SetCheckedStrings (selectedLanguages)


    def save (self):
        self.__config.languageList.value = self.__owner.langList.GetCheckedStrings()


    def _onSelectAll (self, event):
        self.__owner.langList.SetChecked (range (self.__owner.langList.GetCount()))


    def _onClear (self, event):
        self.__owner.langList.SetChecked ([])


    def _getAllLanguages (self):
        """
        Получить список всех языков, о которых знает pygments
        """
        from .pygments.lexers._mapping import LEXERS
        languages = [self._getLongestName (lexer[2]).lower() for lexer in LEXERS.values()]

        # Сделаем некоторые замены
        languages = self._replaceLangItem (languages, "php3", "php")

        languages.sort()
        return languages


    def _replaceLangItem (self, items, oldname, newname):
        """
        Заменить элемент в списке
        Возвращает новый список
        """
        return [newname if item == oldname else item for item in items]


    @staticmethod
    def _getLongestName (namelist):
        """
        Возвращает самое длинное название языка из списка имен одного и того же языка
        """
        maxlen = 0
        bestname = u""

        for name in namelist:
            if len (name) > maxlen:
                maxlen = len (name)
                bestname = name

        return bestname


