#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

import configelements
import outwiker.core.i18n
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.gui.guiconfig import TrayConfig, GeneralGuiConfig, MainWindowConfig
from outwiker.gui.formatctrl import FormatCtrl


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
        self.__createDateTimeFormatGui(self.generalConfig)
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
                str (generalConfig.AUTOSAVE_INTERVAL_DEFAULT), 
                min=self.MIN_AUTOSAVE_INTERVAL, 
                max=self.MAX_AUTOSAVE_INTERVAL, 
                style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_AUTO_URL)

        self.autosaveSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.autosaveSizer.Add(autosaveLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.autosaveSizer.Add(self.autosaveSpin, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        self.autosaveSizer.AddGrowableRow(0)
        self.autosaveSizer.AddGrowableCol(0)
        self.autosaveSizer.AddGrowableCol(1)


    def __createDateTimeFormatGui (self, generalConfig):
        """
        Создать элементы, связанные с выбором формата даты и времени
        """
        dateTimeLabel = wx.StaticText(self, -1, _("Date and time format"))

        hints = [(u"%a", _(u"Abbreviated weekday name")),
                (u"%A", _(u"Full weekday name")),
                (u"%b", _(u"Abbreviated month name")),
                (u"%B", _(u"Full month name")),
                (u"%c", _(u"Appropriate date and time representation")),
                (u"%d", _(u"Day of the month as a decimal number [01,31]")),
                (u"%H", _(u"Hour (24-hour clock) as a decimal number [00,23]")),
                (u"%I", _(u"Hour (12-hour clock) as a decimal number [01,12]")),
                (u"%m", _(u"Month as a decimal number [01,12]")),
                (u"%M", _(u"Minute as a decimal number [00,59]")),
                (u"%p", _(u"AM or PM")),
                (u"%S", _(u"Second as a decimal number [00,61]")),
                (u"%x", _(u"Appropriate date representation")),
                (u"%X", _(u"Appropriate time representation")),
                (u"%y", _(u"Year without century [00,99]")),
                (u"%Y", _(u"Year with century")),
                (u"%%", _(u"A literal '%' character")),
                ]
        self.dateTimeFormatCtrl = FormatCtrl (self, generalConfig.dateTimeFormat.value, hints)

        self.dateTimeSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.dateTimeSizer.AddGrowableRow(0)
        self.dateTimeSizer.AddGrowableCol(1)

        self.dateTimeSizer.Add(dateTimeLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        self.dateTimeSizer.Add(self.dateTimeFormatCtrl, 0, wx.ALL | wx.EXPAND, border=2)


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
        self.minimizeOnCloseCheckBox = wx.CheckBox(self, -1, _("Minimize on close window"))


    def __createHistoryGui (self, generalConfig):
        """
        Создать элементы интерфейса, связанные с историей открытых файлов
        """
        history_label = wx.StaticText(self, -1, _("Recent files history length (restart required)"))
        self.historySpin = wx.SpinCtrl(self, 
                -1, 
                str (generalConfig.RECENT_WIKI_COUNT_DEFAULT), 
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
        main_sizer.Add(self.minimizeOnCloseCheckBox, 0, wx.ALL, 2)
        main_sizer.Add(self.askBeforeExitCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        main_sizer.Add (self.autosaveSizer, 1, wx.EXPAND, 0)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.historySizer, 1, wx.EXPAND, 0)
        main_sizer.Add(self.autoopenCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.titleFormatSizer, 1, wx.EXPAND, 0)
        main_sizer.Add(self.titleMacrosLabel, 0, wx.ALL, 0)

        self.__addStaticLine (main_sizer)
        main_sizer.Add (self.dateTimeSizer, 1, wx.EXPAND, 0)

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
        self.historyLength = configelements.IntegerElement (
                self.generalConfig.historyLength, 
                self.historySpin, 
                self.MIN_HISTORY_LENGTH, 
                self.MAX_HISTORY_LENGTH
                )

        # Открывать последнюю вики при запуске?
        self.autoopen = configelements.BooleanElement (
                self.generalConfig.autoopen, 
                self.autoopenCheckBox
                )


    def __loadGeneralOptions (self):
        """
        Опции для сворачивания окна в трей
        """
        # Сворачивать в трей?
        self.minimizeToTray = configelements.BooleanElement (
                self.trayConfig.minimizeToTray, 
                self.minimizeCheckBox
                )

        # Всегда показывать иконку в трее
        self.alwaysInTray = configelements.BooleanElement (
                self.trayConfig.alwaysShowTrayIcon, 
                self.alwaysInTrayCheckBox
                )

        # Сворачивать при закрытии
        self.minimizeOnClose = configelements.BooleanElement (
                self.trayConfig.minimizeOnClose,
                self.minimizeOnCloseCheckBox
                )

        # Запускаться свернутым?
        self.startIconized = configelements.BooleanElement (
                self.trayConfig.startIconized, 
                self.startIconizedCheckBox
                )

        # Задавать вопрос перед выходом из программы?
        self.askBeforeExit = configelements.BooleanElement (
                self.generalConfig.askBeforeExit, 
                self.askBeforeExitCheckBox
                )

        # Формат заголовка страницы
        self.titleFormat = configelements.StringElement (
                self.mainWindowConfig.titleFormat, 
                self.titleFormatText
                )

        self.dateTimeFormat = configelements.StringElement (
                self.generalConfig.dateTimeFormat, 
                self.dateTimeFormatCtrl
                )

        # Автосохранение
        self.autosaveInterval = configelements.IntegerElement (
                self.generalConfig.autosaveInterval, 
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
        self.minimizeOnClose.save()
        self.askBeforeExit.save()
        self.historyLength.save()
        self.autoopen.save()
        self.autosaveInterval.save()
        self.dateTimeFormat.save()
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
