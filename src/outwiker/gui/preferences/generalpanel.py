# -*- coding: utf-8 -*-

import wx

from . import configelements
import outwiker.core.i18n
from outwiker.core.defines import URL_TRANSLATE
# from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.guiconfig import GeneralGuiConfig, MainWindowConfig
# from outwiker.gui.controls.datetimeformatctrl import DateTimeFormatCtrl
from outwiker.gui.controls.hyperlink import HyperLinkCtrl
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
from outwiker.gui.theme import get_theme


class GeneralPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)

        self.generalConfig = GeneralGuiConfig(application.config)
        self.mainWindowConfig = MainWindowConfig(application.config)
        self.i18nConfig = outwiker.core.i18n.I18nConfig(application.config)
        self._theme = get_theme(application)

        self.MIN_AUTOSAVE_INTERVAL = 0
        self.MAX_AUTOSAVE_INTERVAL = 3600

        self.MIN_HISTORY_LENGTH = 0
        self.MAX_HISTORY_LENGTH = 30

        self.MIN_ICON_HISTORY_LENGTH = 0
        self.MAX_ICON_HISTORY_LENGTH = 100

        self.PAGE_TAB_COMBO_WIDTH = 200
        self.LANG_COMBO_WIDTH = 200

        self.MIN_TOASTER_DELAY = 1
        self.MAX_TOASTER_DELAY = 600

        self.pageTabChoises = [
            (_("Recent used"), GeneralGuiConfig.PAGE_TAB_RECENT),
            (_("Preview"), GeneralGuiConfig.PAGE_TAB_RESULT),
            (_("Edit"), GeneralGuiConfig.PAGE_TAB_CODE),
        ]

        # Номер элемента при выборе "Авто" в списке языков
        self.__autoIndex = 0

        self._createGui()
        self._set_properties()
        self.LoadState()
        self.SetupScrolling()

    def _createGui(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createMiscGui(main_sizer)
        self._createAutosaveGui(main_sizer, self.generalConfig)
        self._addStaticLine(main_sizer)
        self._createHistoryGui(main_sizer, self.generalConfig)
        self._addStaticLine(main_sizer)
        # self._createTemplatesGui(main_sizer, self.generalConfig)
        # self._addStaticLine(main_sizer)
        self._createToasterDelayGui(main_sizer, self.generalConfig)
        self._createOpenPageTabGui(main_sizer)
        self._createLanguageGui(main_sizer)

        self.SetSizer(main_sizer)

    def _set_properties(self):
        DEFAULT_WIDTH = 520
        DEFAULT_HEIGHT = 420

        self.SetSize((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.SetFocus()
        self.SetScrollRate(0, 0)
        self.askBeforeExitCheckBox.SetValue(1)

    def _createAutosaveGui(self, main_sizer, generalConfig):
        """
        Создать элементы, связанные с автосохранением
        """
        autosaveLabel = wx.StaticText(
            self, -1, _("Autosave interval in seconds(0 - disabled)")
        )
        self.autosaveSpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.AUTOSAVE_INTERVAL_DEFAULT),
            min=self.MIN_AUTOSAVE_INTERVAL,
            max=self.MAX_AUTOSAVE_INTERVAL,
            style=wx.SP_ARROW_KEYS,
        )

        autosaveSizer = wx.FlexGridSizer(cols=2)
        autosaveSizer.AddGrowableRow(0)
        autosaveSizer.AddGrowableCol(0)
        autosaveSizer.AddGrowableCol(1)
        autosaveSizer.Add(autosaveLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        autosaveSizer.Add(self.autosaveSpin, 0, wx.ALL | wx.ALIGN_RIGHT, 2)

        main_sizer.Add(autosaveSizer, 1, wx.EXPAND, 0)

    def _createToasterDelayGui(self, main_sizer, generalConfig):
        delayLabel = wx.StaticText(self, label=_("Toaster delay in seconds"))

        self.toasterDelaySpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.TOASTER_DELAY_DEFAULT),
            min=self.MIN_TOASTER_DELAY,
            max=self.MAX_TOASTER_DELAY,
            style=wx.SP_ARROW_KEYS,
        )

        toasterDelaySizer = wx.FlexGridSizer(cols=2)
        toasterDelaySizer.AddGrowableRow(0)
        toasterDelaySizer.AddGrowableCol(0)
        toasterDelaySizer.AddGrowableCol(1)

        toasterDelaySizer.Add(
            delayLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )

        toasterDelaySizer.Add(
            self.toasterDelaySpin, flag=wx.ALL | wx.ALIGN_RIGHT, border=2
        )

        main_sizer.Add(toasterDelaySizer, 1, wx.EXPAND, 0)

    # def _createTemplatesGui(self, main_sizer, generalConfig):
    #     """
    #     Create GUI for selection date and time format
    #     and new page title template
    #     """
    #     # Config values
    #     initial_date_format = generalConfig.dateTimeFormat.value
    #     initial_page_title = generalConfig.pageTitleTemplate.value

    #     # Create labels
    #     dateTimeLabel = wx.StaticText(self, label=_("Date and time format"))
    #     pageTitleTemplateLabel = wx.StaticText(self, label=_("New page title template"))

    #     hintBitmap = wx.Bitmap(getBuiltinImagePath("wand.png"))

    #     # Create main controls
    #     self.dateTimeFormatCtrl = DateTimeFormatCtrl(
    #         self, hintBitmap, initial_date_format
    #     )

    #     self.pageTitleTemplateCtrl = DateTimeFormatCtrl(
    #         self, hintBitmap, initial_page_title
    #     )

    #     # Create common sizer
    #     templateSizer = wx.FlexGridSizer(cols=2)
    #     templateSizer.AddGrowableCol(1)

    #     templateSizer.Add(
    #         dateTimeLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
    #     )
    #     templateSizer.Add(
    #         self.dateTimeFormatCtrl, flag=wx.TOP | wx.BOTTOM | wx.EXPAND, border=2
    #     )

    #     templateSizer.Add(
    #         pageTitleTemplateLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
    #     )
    #     templateSizer.Add(
    #         self.pageTitleTemplateCtrl, flag=wx.TOP | wx.BOTTOM | wx.EXPAND, border=2
    #     )

    #     main_sizer.Add(templateSizer, flag=wx.EXPAND)

    def _createMiscGui(self, main_sizer):
        """
        Создать элементы интерфейса, которые не попали ни в какую другую
            категорию
        """
        self.askBeforeExitCheckBox = wx.CheckBox(self, -1, _("Ask before exit"))

        main_sizer.Add(
            self.askBeforeExitCheckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2
        )

    def _createHistoryGui(self, main_sizer, generalConfig):
        """
        Создать элементы интерфейса, связанные с историей открытых файлов
        """
        # Count of recently used icons
        recentIconsLabel = wx.StaticText(
            self, -1, _("Length of recently used icons history")
        )

        self.iconsHistoryLengthSpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.RECENT_ICONS_COUNT_DEFAULT),
            min=self.MIN_ICON_HISTORY_LENGTH,
            max=self.MAX_ICON_HISTORY_LENGTH,
            style=wx.SP_ARROW_KEYS,
        )

        # Recently opened files
        history_label = wx.StaticText(
            self, -1, _("Length of recently opened files history")
        )

        self.historySpin = wx.SpinCtrl(
            self,
            -1,
            str(generalConfig.RECENT_WIKI_COUNT_DEFAULT),
            min=self.MIN_HISTORY_LENGTH,
            max=self.MAX_HISTORY_LENGTH,
            style=wx.SP_ARROW_KEYS,
        )

        self.autoopenCheckBox = wx.CheckBox(
            self, -1, _("Automatically open the recent file")
        )

        historySizer = wx.FlexGridSizer(cols=2)
        historySizer.AddGrowableCol(0)
        historySizer.AddGrowableCol(1)

        historySizer.Add(
            recentIconsLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        historySizer.Add(
            self.iconsHistoryLengthSpin, flag=wx.ALL | wx.ALIGN_RIGHT, border=2
        )
        historySizer.Add(
            history_label, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        historySizer.Add(self.historySpin, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)

        main_sizer.Add(historySizer, flag=wx.EXPAND)
        main_sizer.Add(
            self.autoopenCheckBox, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )

    def _createLanguageGui(self, main_sizer):
        """
        Создать элементы интерфейса, связанные с выбором языка
        """
        languageSizer = wx.FlexGridSizer(cols=2)
        languageSizer.AddGrowableRow(0)
        languageSizer.AddGrowableCol(0)
        languageSizer.AddGrowableCol(1)

        self.langLabel, self.langCombo = self._createLabelAndComboBox(
            _("Language(restart required)"), languageSizer
        )
        self.langCombo.SetMinSize((self.LANG_COMBO_WIDTH, -1))

        self.helpTranslateHyperLink = HyperLinkCtrl(
            self, label=_("Help with translation"), URL=URL_TRANSLATE
        )
        self.helpTranslateHyperLink.SetColours(
            self._theme.colorHyperlink,
            self._theme.colorHyperlink,
            self._theme.colorHyperlink,
        )

        main_sizer.Add(languageSizer, flag=wx.EXPAND)
        main_sizer.Add(
            self.helpTranslateHyperLink,
            flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=2,
        )

    def _createOpenPageTabGui(self, main_sizer):
        """
        Создать элементы интерфейса для выбора вкладки страницы по умолчанию
            (Код / просмотр / последний используемый)
        """
        # Layout GUI elements
        pageTabSizer = wx.FlexGridSizer(cols=2)
        pageTabSizer.AddGrowableCol(0)
        pageTabSizer.AddGrowableCol(1)
        pageTabSizer.AddGrowableRow(0)

        pageTabLabel, self.pageTabComboBox = self._createLabelAndComboBox(
            _("Default opening page mode"), pageTabSizer
        )

        self.pageTabComboBox.SetMinSize((self.PAGE_TAB_COMBO_WIDTH, -1))
        self._fillPageTabComboBox()
        main_sizer.Add(pageTabSizer, 1, wx.EXPAND, 0)

    def _fillPageTabComboBox(self):
        # Fill pageTabComboBox
        for item in self.pageTabChoises:
            self.pageTabComboBox.Append(item[0])

        choise = self.generalConfig.pageTab.value
        selectedItem = 0
        for n, item in enumerate(self.pageTabChoises):
            if item[1] == choise:
                selectedItem = n

        self.pageTabComboBox.SetSelection(selectedItem)

    def _addStaticLine(self, main_sizer):
        static_line = wx.StaticLine(self, -1)
        main_sizer.Add(static_line, 0, wx.EXPAND, 0)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        self._loadGeneralOptions()
        self._loadRecentOptions()

    def _loadRecentOptions(self):
        """
        Опции, связанные с последними открытыми файлами
        """
        # Длина истории последних открытых файлов
        self.historyLength = configelements.IntegerElement(
            self.generalConfig.historyLength,
            self.historySpin,
            self.MIN_HISTORY_LENGTH,
            self.MAX_HISTORY_LENGTH,
        )

        self.iconsHistoryLength = configelements.IntegerElement(
            self.generalConfig.iconsHistoryLength,
            self.iconsHistoryLengthSpin,
            self.MIN_ICON_HISTORY_LENGTH,
            self.MAX_ICON_HISTORY_LENGTH,
        )

        # Открывать последнюю вики при запуске?
        self.autoopen = configelements.BooleanElement(
            self.generalConfig.autoopen, self.autoopenCheckBox
        )

    def _loadGeneralOptions(self):
        """
        Загрузка общих параметров программы
        """
        # Задавать вопрос перед выходом из программы?
        self.askBeforeExit = configelements.BooleanElement(
            self.generalConfig.askBeforeExit, self.askBeforeExitCheckBox
        )

        # self.dateTimeFormat = configelements.StringElement(
        #     self.generalConfig.dateTimeFormat, self.dateTimeFormatCtrl
        # )

        # self.pageTitleTemplate = configelements.StringElement(
        #     self.generalConfig.pageTitleTemplate, self.pageTitleTemplateCtrl
        # )

        # Автосохранение
        self.autosaveInterval = configelements.IntegerElement(
            self.generalConfig.autosaveInterval,
            self.autosaveSpin,
            self.MIN_AUTOSAVE_INTERVAL,
            self.MAX_AUTOSAVE_INTERVAL,
        )

        self._loadLanguages()
        self.toasterDelaySpin.SetValue(self.generalConfig.toasterDelay.value // 1000)

    def _loadLanguages(self):
        languages = outwiker.core.i18n.getLanguages()
        languages.sort()

        self.langCombo.Clear()
        self.langCombo.AppendItems(languages)
        self.langCombo.Insert(_("Auto"), self.__autoIndex)

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
        # self.dateTimeFormat.save()
        # self.pageTitleTemplate.save()
        self._saveLanguage()
        self._savePageTab()
        self.generalConfig.toasterDelay.value = self.toasterDelaySpin.GetValue() * 1000

    def _saveLanguage(self):
        index = self.langCombo.GetSelection()
        assert index != wx.NOT_FOUND

        if index == self.__autoIndex:
            lang = outwiker.core.i18n.AUTO_LANGUAGE
        else:
            lang = self.langCombo.GetString(index)

        self.i18nConfig.languageOption.value = lang

    def _savePageTab(self):
        selectedItem = self.pageTabComboBox.GetSelection()
        assert selectedItem < len(self.pageTabChoises)

        self.generalConfig.pageTab.value = self.pageTabChoises[selectedItem][1]
