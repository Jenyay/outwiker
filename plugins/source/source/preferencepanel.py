# -*- coding: utf-8 -*-

import wx

from outwiker.gui.preferences.configelements import IntegerElement
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel

from .sourceconfig import SourceConfig
from .i18n import get_
from .misc import fillStyleComboBox
from .langlist import LangList


class PreferencePanel(BasePrefPanel):
    """
    Панель с настройками
    """

    def __init__(self, parent, config):
        """
        parent - родитель панели(должен быть wx.Treebook)
        config - настройки из plugin._application.config
        """
        super().__init__(parent)

        global _
        _ = get_()

        self.__createGui()
        self.__controller = PrefPanelController(self, config)
        self.SetupScrolling()

    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(3)

        self.__createTabWidthGui(mainSizer)
        self.__createDefaultStyleGui(mainSizer)
        self.__createLangGui(mainSizer)
        self.SetSizer(mainSizer)

    def __createTabWidthGui(self, mainSizer):
        """
        Создать элементы управления, связанные
            с выбором размера табуляции по умолчанию
        """
        tabSizer = wx.FlexGridSizer(0, 2, 0, 0)
        tabSizer.AddGrowableCol(1)

        tabWidthLabel = wx.StaticText(self, -1, _(u"Default Tab Width"))

        self.tabWidthSpin = wx.SpinCtrl(
            self,
            style=wx.SP_ARROW_KEYS
        )
        self.tabWidthSpin.SetMinSize(wx.Size(150, -1))

        tabSizer.Add(
            tabWidthLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2
        )

        tabSizer.Add(
            self.tabWidthSpin,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2
        )

        mainSizer.Add(
            tabSizer,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2)

    def __createDefaultStyleGui(self, mainSizer):
        """
        Создать элементы управления, связанные с выбором стиля по умолчанию
        """
        styleSizer = wx.FlexGridSizer(0, 2, 0, 0)
        styleSizer.AddGrowableCol(1)

        styleLabel = wx.StaticText(self, -1, _(u"Default Style"))

        self.styleComboBox = wx.ComboBox(self,
                                         -1,
                                         style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.styleComboBox.SetMinSize((150, -1))

        styleSizer.Add(
            styleLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2
        )

        styleSizer.Add(
            self.styleComboBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2
        )

        mainSizer.Add(
            styleSizer,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2)

    def __createLangGui(self, mainSizer):
        """
        Создание элементов управления, связанных с выбором используемых языков
        """
        # Метка с комментарием о том, что это за языки в списке
        languageLabel = wx.StaticText(self, -1, _(u"Used Languages"))
        mainSizer.Add(
            languageLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2)

        # Сайзер для расположения списка языков и кнопок
        langSizer = wx.FlexGridSizer(0, 2, 0, 0)
        langSizer.AddGrowableRow(0)
        langSizer.AddGrowableCol(0)

        self.langList = wx.CheckListBox(self, -1)
        langSizer.Add(
            self.langList,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2)

        # Кнопки
        buttonsSizer = wx.BoxSizer(wx.VERTICAL)
        self.selectAllButton = wx.Button(self, label=_(u"Select All"))
        self.clearButton = wx.Button(self, label=_(u"Clear"))

        buttonsSizer.Add(
            self.selectAllButton,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2)

        buttonsSizer.Add(
            self.clearButton,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2)

        langSizer.Add(
            buttonsSizer,
            proportion=1,
            flag=wx.ALL,
            border=2)

        mainSizer.Add(
            langSizer,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2)

    def LoadState(self):
        self.__controller.loadState()

    def Save(self):
        self.__controller.save()


class PrefPanelController(object):
    """
    Контроллер для панели настроек
    """

    def __init__(self, owner, config):
        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50
        self._langList = LangList(get_())

        self._owner = owner
        self._config = SourceConfig(config)

        self._owner.selectAllButton.Bind(wx.EVT_BUTTON, self._onSelectAll)
        self._owner.clearButton.Bind(wx.EVT_BUTTON, self._onClear)

    def loadState(self):
        self._tabWidthOption = IntegerElement(
            self._config.tabWidth,
            self._owner.tabWidthSpin,
            self.MIN_TAB_WIDTH,
            self.MAX_TAB_WIDTH
        )

        fillStyleComboBox(self._config,
                          self._owner.styleComboBox,
                          self._config.defaultStyle.value.strip())

        allLanguages = self._getAllLanguages()
        self._owner.langList.Clear()
        self._owner.langList.AppendItems(allLanguages)

        selectedLanguages = [self._langList.getLangName(designation)
                             for designation
                             in self._config.languageList.value]

        self._owner.langList.SetCheckedStrings(selectedLanguages)

    def save(self):
        self._tabWidthOption.save()
        self._config.defaultStyle.value = self._owner.styleComboBox.GetValue()

        designations = [self._langList.getDesignation(name)
                        for name in self._owner.langList.GetCheckedStrings()]
        self._config.languageList.value = designations

    def _onSelectAll(self, event):
        self._owner.langList.SetChecked(
            range(self._owner.langList.GetCount()))

    def _onClear(self, event):
        self._owner.langList.SetChecked([])

    def _getAllLanguages(self):
        """
        Получить список всех языков, о которых знает pygments
        """
        return sorted(self._langList.allNames())
