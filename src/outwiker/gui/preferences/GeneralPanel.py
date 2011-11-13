#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

import ConfigElements
import outwiker.core.i18n
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.gui.guiconfig import TrayConfig, GeneralGuiConfig, MainWindowConfig


class GeneralPanel (wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)

        self.trayConfig = TrayConfig (Application.config)
        self.generalConfig = GeneralGuiConfig (Application.config)
        self.mainWindowConfig = MainWindowConfig (Application.config)
        self.i18nConfig = I18nConfig (Application.config)

        self.MIN_AUTOSAVE_INTERVAL = 0
        self.MAX_AUTOSAVE_INTERVAL = 3600

        self.MIN_HISTORY_LENGTH = 0
        self.MAX_HISTORY_LENGTH = 30

        # Номер элемента при выборе "Авто" в списке языков
        self.__autoIndex = 0

        self.__createTrayGui()
        self.__createMiscGui()
        self.__createAutosaveGui(self.generalConfig)
        self.__createHistoryGui(self.generalConfig)
        self.__createTitleFormatGui()
        self.__createLanguageGui()

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.onMinimizeToTray, self.minimizeCheckBox)

        self.LoadState()
        self.updateCheckState()


    def __set_properties(self):
        DEFAULT_WIDTH = 520
        DEFAULT_HEIGHT = 420

        self.SetSize((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.SetFocus()
        self.SetScrollRate(0, 0)
        self.askBeforeExitCheckBox.SetValue(1)

        LANG_COMBO_WIDTH = 130
        self.langCombo.SetMinSize((LANG_COMBO_WIDTH, -1))


    def __createAutosaveGui (self, generalConfig):
        """
        Создать элементы, связанные с автосохранением
        """
        autosaveLabel = wx.StaticText(self, -1, _("Autosave interval in seconds (0 - disabled)"))
        self.autosaveSpin = wx.SpinCtrl(self, 
                -1, 
                str (generalConfig.DEFAULT_AUTOSAVE_INTERVAL), 
                min=self.MIN_AUTOSAVE_INTERVAL, 
                max=self.MAX_AUTOSAVE_INTERVAL, 
                style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_AUTO_URL)

        self.autosaveSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.autosaveSizer.Add(autosaveLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.autosaveSizer.Add(self.autosaveSpin, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        self.autosaveSizer.AddGrowableRow(0)
        self.autosaveSizer.AddGrowableCol(0)
        self.autosaveSizer.AddGrowableCol(1)


    def __createMiscGui (self):
        """
        Создать элементы интерфейса, которые не попали ни в какую другую категорию
        """
        self.askBeforeExitCheckBox = wx.CheckBox(self, -1, _("Ask before exit"))


    def __createTrayGui (self):
        """
        Создать элементы интерфейса, связанные с треем
        """
        self.minimizeCheckBox = wx.CheckBox(self, -1, _("Minimize to tray"))
        self.startIconizedCheckBox = wx.CheckBox(self, -1, _("Start iconized"))
        self.alwaysInTrayCheckBox = wx.CheckBox(self, -1, _("Always show tray icon"))


    def __createHistoryGui (self, generalConfig):
        """
        Создать элементы интерфейса, связанные с историей открытых файлов
        """
        history_label = wx.StaticText(self, -1, _("Recent files history length (restart required)"))
        self.historySpin = wx.SpinCtrl(self, 
                -1, 
                str (generalConfig.DEFAULT_RECENT_WIKI_COUNT), 
                min=self.MIN_HISTORY_LENGTH, 
                max=self.MAX_HISTORY_LENGTH, 
                style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_AUTO_URL)

        self.autoopenCheckBox = wx.CheckBox(self, -1, _("Automatically open the recent file"))

        self.historySizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.historySizer.Add(history_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.historySizer.Add(self.historySpin, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        self.historySizer.AddGrowableRow(0)
        self.historySizer.AddGrowableCol(0)
        self.historySizer.AddGrowableCol(1)


    def __createTitleFormatGui (self):
        """
        Создать элементы интерфейса, связанные с форматом заголовка главного окна
        """
        self.titleMacrosLabel = wx.StaticText(self, -1, _("Macros for title:\n{file} - open wiki file name\n{page} - open page title"))

        self.titleFormatLabel = wx.StaticText(self, -1, _("Main window title format"))
        self.titleFormatText = wx.TextCtrl(self, -1, "")
        self.titleFormatSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.titleFormatSizer.Add(self.titleFormatLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.titleFormatSizer.Add(self.titleFormatText, 0, wx.ALL|wx.EXPAND, 2)
        self.titleFormatSizer.AddGrowableCol(1)


    def __createLanguageGui (self):
        """
        Создать элементы интерфейса, связанные с выбором языка
        """
        self.langLabel = wx.StaticText(self, -1, _("Language (restart required)"))
        self.langCombo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.languageSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.languageSizer.Add(self.langLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.languageSizer.Add(self.langCombo, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
        self.languageSizer.AddGrowableRow(0)
        self.languageSizer.AddGrowableCol(0)
        self.languageSizer.AddGrowableCol(1)


    def __addStaticLine (self, main_sizer):
        static_line = wx.StaticLine(self, -1)
        main_sizer.Add(static_line, 0, wx.EXPAND, 0)


    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(10, 1, 0, 0)
        main_sizer.AddGrowableCol(0)

        main_sizer.Add(self.minimizeCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        main_sizer.Add(self.startIconizedCheckBox, 0, wx.ALL, 2)
        main_sizer.Add(self.alwaysInTrayCheckBox, 0, wx.ALL, 2)
        main_sizer.Add(self.askBeforeExitCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        main_sizer.Add (self.autosaveSizer, 1, wx.EXPAND, 0)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.historySizer, 1, wx.EXPAND, 0)
        main_sizer.Add(self.autoopenCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.titleFormatSizer, 1, wx.EXPAND, 0)
        main_sizer.Add(self.titleMacrosLabel, 0, wx.ALL, 0)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.languageSizer, 1, wx.EXPAND, 0)

        self.SetSizer(main_sizer)
    

    def LoadState (self):
        """
        Загрузить состояние страницы из конфига
        """
        self.__loadGeneralOptions()
        self.__loadRecentOptions()

    
    def __loadRecentOptions (self):
        """
        Опции, связанные с последними открытыми файлами
        """
        # Длина истории последних открытых файлов
        self.historyLength = ConfigElements.IntegerElement (
                self.generalConfig.historyLengthOption, 
                self.historySpin, 
                self.MIN_HISTORY_LENGTH, 
                self.MAX_HISTORY_LENGTH
                )

        # Открывать последнюю вики при запуске?
        self.autoopen = ConfigElements.BooleanElement (
                self.generalConfig.autoopenOption, 
                self.autoopenCheckBox
                )


    def __loadGeneralOptions (self):
        """
        Опции для сворачивания окна в трей
        """
        # Сворачивать в трей?
        self.minimizeToTray = ConfigElements.BooleanElement (
                self.trayConfig.minimizeOption, 
                self.minimizeCheckBox
                )

        # Всегда показывать иконку в трее
        self.alwaysInTray = ConfigElements.BooleanElement (
                self.trayConfig.alwaysShowTrayIconOption, 
                self.alwaysInTrayCheckBox
                )

        # Запускаться свернутым?
        self.startIconized = ConfigElements.BooleanElement (
                self.trayConfig.startIconizedOption, 
                self.startIconizedCheckBox
                )

        # Задавать вопрос перед выходом из программы?
        self.askBeforeExit = ConfigElements.BooleanElement (
                self.generalConfig.askBeforeExitOption, 
                self.askBeforeExitCheckBox
                )

        # Формат заголовка страницы
        self.titleFormat = ConfigElements.StringElement (
                self.mainWindowConfig.titleFormatOption, 
                self.titleFormatText
                )

        # Автосохранение
        self.autosaveInterval = ConfigElements.IntegerElement (
                self.generalConfig.autosaveIntervalOption, 
                self.autosaveSpin, 
                self.MIN_AUTOSAVE_INTERVAL, 
                self.MAX_AUTOSAVE_INTERVAL
                )

        self.__loadLanguages()
    

    def __loadLanguages (self):
        languages = outwiker.core.i18n.getLanguages()
        languages.sort()

        self.langCombo.Clear ()
        self.langCombo.AppendItems (languages)
        self.langCombo.Insert (_(u"Auto"), self.__autoIndex)

        currlang = self.i18nConfig.languageOption.value

        try:
            # "+1" за счет того, что добавляется пункт "Auto"
            currindex = languages.index (currlang) + 1
        except ValueError:
            # Индекс для автоопределения языка
            currindex = self.__autoIndex

        self.langCombo.SetSelection (currindex)


    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        self.startIconized.save()
        self.minimizeToTray.save()
        self.askBeforeExit.save()
        self.historyLength.save()
        self.autoopen.save()
        self.autosaveInterval.save()
        self.__saveLanguage()

        if self.titleFormat.isValueChanged() or self.alwaysInTray.isValueChanged():
            self.alwaysInTray.save()
            self.titleFormat.save()
    

    def __saveLanguage (self):
        index = self.langCombo.GetSelection()
        assert index != wx.NOT_FOUND

        if index == self.__autoIndex:
            lang = outwiker.core.i18n.AUTO_LANGUAGE
        else:
            lang = self.langCombo.GetString (index)

        self.i18nConfig.languageOption.value = lang


    def onMinimizeToTray(self, event):
        self.updateCheckState()
    

    def updateCheckState (self):
        """
        Обновить стостояния чекбоксов
        """
        if not self.minimizeCheckBox.IsChecked():
            self.startIconizedCheckBox.SetValue(False)
            self.startIconizedCheckBox.Disable()
        else:
            self.startIconizedCheckBox.Enable()
