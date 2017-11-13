# -*- coding: utf-8 -*-

import os

import wx

import configelements
import outwiker.core.i18n
from outwiker.core.application import Application
from outwiker.core.system import getImagesDir
from outwiker.gui.guiconfig import (GeneralGuiConfig,
                                    MainWindowConfig)
from outwiker.gui.controls.formatctrl import FormatCtrl
from outwiker.gui.controls.datetimeformatctrl import DateTimeFormatCtrl
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class GeneralPanel(BasePrefPanel):
    def __init__(self, parent):
        super(GeneralPanel, self).__init__(parent)

        self.generalConfig = GeneralGuiConfig(Application.config)
        self.mainWindowConfig = MainWindowConfig(Application.config)
        self.i18nConfig = outwiker.core.i18n.I18nConfig(Application.config)

        self.MIN_AUTOSAVE_INTERVAL = 0
        self.MAX_AUTOSAVE_INTERVAL = 3600

        self.MIN_HISTORY_LENGTH = 0
        self.MAX_HISTORY_LENGTH = 30

        self.MIN_ICON_HISTORY_LENGTH = 0
        self.MAX_ICON_HISTORY_LENGTH = 100

        self.PAGE_TAB_COMBO_WIDTH = 200
        self.LANG_COMBO_WIDTH = 200

        self.pageTabChoises = [
           (_(u'Recent used'), GeneralGuiConfig.PAGE_TAB_RECENT),
           (_(u'Preview'), GeneralGuiConfig.PAGE_TAB_RESULT),
           (_(u'Edit'), GeneralGuiConfig.PAGE_TAB_CODE),
        ]

        # Номер элемента при выборе "Авто" в списке языков
        self.__autoIndex = 0

        self.__createMiscGui()
        self.__createAutosaveGui(self.generalConfig)
        self.__createHistoryGui(self.generalConfig)
        self.__createTitleFormatGui()
        self.__createDateTimeFormatGui(self.generalConfig)
        self.__createOpenPageTabGui()
        self.__createLanguageGui()

        self.__set_properties()
        self.__do_layout()

        self.LoadState()
        self._setScrolling()

    def __set_properties(self):
        DEFAULT_WIDTH = 520
        DEFAULT_HEIGHT = 420

        self.SetSize((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.SetFocus()
        self.SetScrollRate(0, 0)
        self.askBeforeExitCheckBox.SetValue(1)

    def __createAutosaveGui(self, generalConfig):
        """
        Создать элементы, связанные с автосохранением
        """
        autosaveLabel = wx.StaticText(
            self,
            -1,
            _("Autosave interval in seconds(0 - disabled)"))
        self.autosaveSpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.AUTOSAVE_INTERVAL_DEFAULT),
            min=self.MIN_AUTOSAVE_INTERVAL,
            max=self.MAX_AUTOSAVE_INTERVAL,
            style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_AUTO_URL)

        self.autosaveSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.autosaveSizer.Add(autosaveLabel,
                               0,
                               wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               2)

        self.autosaveSizer.Add(self.autosaveSpin,
                               0,
                               wx.ALL | wx.ALIGN_RIGHT,
                               2)
        self.autosaveSizer.AddGrowableRow(0)
        self.autosaveSizer.AddGrowableCol(0)
        self.autosaveSizer.AddGrowableCol(1)

    def __createDateTimeFormatGui(self, generalConfig):
        """
        Создать элементы, связанные с выбором формата даты и времени
        """
        initial = generalConfig.dateTimeFormat.value
        dateTimeLabel = wx.StaticText(self, -1, _("Date and time format"))

        hintBitmap = wx.Bitmap(os.path.join(getImagesDir(), u"wand.png"))
        self.dateTimeFormatCtrl = DateTimeFormatCtrl(self, hintBitmap, initial)

        self.dateTimeSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.dateTimeSizer.AddGrowableRow(0)
        self.dateTimeSizer.AddGrowableCol(1)

        self.dateTimeSizer.Add(dateTimeLabel,
                               0,
                               wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                               border=2)
        self.dateTimeSizer.Add(self.dateTimeFormatCtrl,
                               0,
                               wx.ALL | wx.EXPAND,
                               border=2)

    def __createMiscGui(self):
        """
        Создать элементы интерфейса, которые не попали ни в какую другую
            категорию
        """
        self.askBeforeExitCheckBox = wx.CheckBox(self,
                                                 -1,
                                                 _("Ask before exit"))

    def __createHistoryGui(self, generalConfig):
        """
        Создать элементы интерфейса, связанные с историей открытых файлов
        """
        # Count of recently used icons
        recent_icons_label = wx.StaticText(
            self,
            -1,
            _("Length of recently used icons history"))

        self.iconsHistoryLengthSpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.RECENT_ICONS_COUNT_DEFAULT),
            min=self.MIN_ICON_HISTORY_LENGTH,
            max=self.MAX_ICON_HISTORY_LENGTH,
            style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_AUTO_URL)

        # Recently opened files
        history_label = wx.StaticText(
            self,
            -1,
            _("Length of recently opened files history"))

        self.historySpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.RECENT_WIKI_COUNT_DEFAULT),
            min=self.MIN_HISTORY_LENGTH,
            max=self.MAX_HISTORY_LENGTH,
            style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_AUTO_URL)

        self.autoopenCheckBox = wx.CheckBox(
            self,
            -1,
            _("Automatically open the recent file"))

        self.historySizer = wx.FlexGridSizer(cols=2)
        self.historySizer.AddGrowableCol(0)
        self.historySizer.AddGrowableCol(1)

        self.historySizer.Add(recent_icons_label,
                              0,
                              wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                              2)

        self.historySizer.Add(self.iconsHistoryLengthSpin,
                              0,
                              wx.ALL | wx.ALIGN_RIGHT,
                              2)

        self.historySizer.Add(history_label,
                              0,
                              wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                              2)

        self.historySizer.Add(self.historySpin,
                              0,
                              wx.ALL | wx.ALIGN_RIGHT,
                              2)

    def __createTitleFormatGui(self):
        """
        Создать элементы интерфейса, связанные с форматом заголовка
            главного окна
        """

        hints = [
            (u"{file}", _(u"Wiki file name")),
            (u"{page}", _(u"Page title")),
            (u"{subpath}", _(u"Relative path to current page")),
        ]

        self.titleFormatLabel = wx.StaticText(self,
                                              -1,
                                              _("Main window title format"))

        hintBitmap = wx.Bitmap(os.path.join(getImagesDir(), u"wand.png"))
        self.titleFormatText = FormatCtrl(
            self,
            self.mainWindowConfig.titleFormat.value,
            hints,
            hintBitmap)

        self.titleFormatSizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.titleFormatSizer.Add(self.titleFormatLabel,
                                  0,
                                  wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                  2)

        self.titleFormatSizer.Add(self.titleFormatText,
                                  0,
                                  wx.ALL | wx.EXPAND,
                                  2)

        self.titleFormatSizer.AddGrowableCol(1)

    def __createLanguageGui(self):
        """
        Создать элементы интерфейса, связанные с выбором языка
        """
        self.languageSizer = wx.FlexGridSizer(cols=2)
        self.languageSizer.AddGrowableRow(0)
        self.languageSizer.AddGrowableCol(0)
        self.languageSizer.AddGrowableCol(1)

        self.langLabel, self.langCombo = self._createLabelAndComboBox(
            _("Language(restart required)"),
            self.languageSizer
        )
        self.langCombo.SetMinSize((self.LANG_COMBO_WIDTH, -1))

    def __createOpenPageTabGui(self):
        """
        Создать элементы интерфейса для выбора вкладки страницы по умолчанию
            (Код / просмотр / последний используемый)
        """
        # Layout GUI elements
        self.pageTabSizer = wx.FlexGridSizer(cols=2)
        self.pageTabSizer.AddGrowableCol(0)
        self.pageTabSizer.AddGrowableCol(1)
        self.pageTabSizer.AddGrowableRow(0)

        pageTabLabel, self.pageTabComboBox = self._createLabelAndComboBox(
            _(u'Default opening page mode'),
            self.pageTabSizer)

        self.pageTabComboBox.SetMinSize((self.PAGE_TAB_COMBO_WIDTH, -1))
        self.__fillPageTabComboBox()

    def __fillPageTabComboBox(self):
        # Fill pageTabComboBox
        for item in self.pageTabChoises:
            self.pageTabComboBox.Append(item[0])

        choise = self.generalConfig.pageTab.value
        selectedItem = 0
        for n, item in enumerate(self.pageTabChoises):
            if item[1] == choise:
                selectedItem = n

        self.pageTabComboBox.SetSelection(selectedItem)

    def __addStaticLine(self, main_sizer):
        static_line = wx.StaticLine(self, -1)
        main_sizer.Add(static_line, 0, wx.EXPAND, 0)

    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        main_sizer.Add(self.askBeforeExitCheckBox,
                       0,
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       2)

        main_sizer.Add(self.autosaveSizer, 1, wx.EXPAND, 0)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.historySizer, 1, wx.EXPAND, 0)

        main_sizer.Add(self.autoopenCheckBox,
                       0,
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       2)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.titleFormatSizer, 1, wx.EXPAND, 0)
        main_sizer.Add(self.dateTimeSizer, 1, wx.EXPAND, 0)

        self.__addStaticLine(main_sizer)
        main_sizer.Add(self.pageTabSizer, 1, wx.EXPAND, 0)
        main_sizer.Add(self.languageSizer, 1, wx.EXPAND, 0)

        self.SetSizer(main_sizer)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        self.__loadGeneralOptions()
        self.__loadRecentOptions()

    def __loadRecentOptions(self):
        """
        Опции, связанные с последними открытыми файлами
        """
        # Длина истории последних открытых файлов
        self.historyLength = configelements.IntegerElement(
            self.generalConfig.historyLength,
            self.historySpin,
            self.MIN_HISTORY_LENGTH,
            self.MAX_HISTORY_LENGTH
        )

        self.iconsHistoryLength = configelements.IntegerElement(
            self.generalConfig.iconsHistoryLength,
            self.iconsHistoryLengthSpin,
            self.MIN_ICON_HISTORY_LENGTH,
            self.MAX_ICON_HISTORY_LENGTH
        )

        # Открывать последнюю вики при запуске?
        self.autoopen = configelements.BooleanElement(
            self.generalConfig.autoopen,
            self.autoopenCheckBox
        )

    def __loadGeneralOptions(self):
        """
        Загрузка общих параметров программы
        """
        # Задавать вопрос перед выходом из программы?
        self.askBeforeExit = configelements.BooleanElement(
            self.generalConfig.askBeforeExit,
            self.askBeforeExitCheckBox
        )

        # Формат заголовка страницы
        self.titleFormat = configelements.StringElement(
            self.mainWindowConfig.titleFormat,
            self.titleFormatText
        )

        self.dateTimeFormat = configelements.StringElement(
            self.generalConfig.dateTimeFormat,
            self.dateTimeFormatCtrl
        )

        # Автосохранение
        self.autosaveInterval = configelements.IntegerElement(
            self.generalConfig.autosaveInterval,
            self.autosaveSpin,
            self.MIN_AUTOSAVE_INTERVAL,
            self.MAX_AUTOSAVE_INTERVAL
        )

        self.__loadLanguages()

    def __loadLanguages(self):
        languages = outwiker.core.i18n.getLanguages()
        languages.sort()

        self.langCombo.Clear()
        self.langCombo.AppendItems(languages)
        self.langCombo.Insert(_(u"Auto"), self.__autoIndex)

        currlang = self.i18nConfig.languageOption.value

        try:
            # "+1" за счет того, что добавляется пункт "Auto"
            currindex = languages.index(currlang) + 1
        except ValueError:
            # Индекс для автоопределения языка
            currindex = self.__autoIndex

        self.langCombo.SetSelection(currindex)

    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        self.askBeforeExit.save()
        self.historyLength.save()
        self.iconsHistoryLength.save()
        self.autoopen.save()
        self.autosaveInterval.save()
        self.dateTimeFormat.save()
        self.titleFormat.save()
        self.__saveLanguage()
        self.__savePageTab()

    def __saveLanguage(self):
        index = self.langCombo.GetSelection()
        assert index != wx.NOT_FOUND

        if index == self.__autoIndex:
            lang = outwiker.core.i18n.AUTO_LANGUAGE
        else:
            lang = self.langCombo.GetString(index)

        self.i18nConfig.languageOption.value = lang

    def __savePageTab(self):
        selectedItem = self.pageTabComboBox.GetSelection()
        assert selectedItem < len(self.pageTabChoises)

        self.generalConfig.pageTab.value = self.pageTabChoises[selectedItem][1]
