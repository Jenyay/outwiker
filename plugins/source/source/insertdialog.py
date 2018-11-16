# -*- coding: utf-8 -*-

import wx

from .i18n import get_
from .misc import getImagePath


class InsertDialog (wx.Dialog):
    """
    Диалог для вставки команды (:source:)
    """

    def __init__(self, parent):
        global _
        _ = get_()

        super().__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            title=_(u"Source code"))

        # Размер отступа
        self._indent = 50
        self._fieldsWidth = 200

        self._createGui()
        self.fileCheckBox.SetFocus()
        self.Center(wx.BOTH)

    @property
    def language(self):
        return self.languageComboBox.GetValue()

    @property
    def tabWidth(self):
        return self.tabWidthSpin.GetValue()

    @property
    def languageIndex(self):
        return self.languageComboBox.GetCurrentSelection()

    @property
    def attachment(self):
        return self.attachmentComboBox.GetValue()

    @property
    def encoding(self):
        return self.encodingComboBox.GetValue()

    @property
    def insertFromFile(self):
        return self.fileCheckBox.IsChecked()

    @property
    def style(self):
        return self.styleComboBox.GetValue()

    @property
    def parentbg(self):
        return self.parentBgCheckBox.GetValue()

    @property
    def lineNum(self):
        return self.lineNumCheckBox.GetValue()

    def _createGui(self):
        """
        Создать элементы управления
        """
        self.notebook = wx.Notebook(self, -1)

        mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)

        mainSizer.Add(
            self.notebook,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=2
        )

        self.generalPanel = self._createGeneralPanel()
        self.appearancePanel = self._createAppearancePanel()
        self._createOkCancelButtons(mainSizer)

        self.notebook.AddPage(self.generalPanel, _(u"General"))
        self.notebook.AddPage(self.appearancePanel, _(u"Appearance"))

        self.SetSizer(mainSizer)
        self.Layout()
        self.Fit()

    def _createGeneralPanel(self):
        generalPanel = wx.Panel(self.notebook)

        generalSizer = wx.FlexGridSizer(cols=1)
        generalSizer.AddGrowableCol(0)
        generalPanel.SetSizer(generalSizer)

        self._createFileGui(generalSizer, generalPanel)
        self._createLanguageGui(generalSizer, generalPanel)

        return generalPanel

    def _createAppearancePanel(self):
        appearancePanel = wx.Panel(self.notebook)

        appearanceSizer = wx.FlexGridSizer(cols=1)
        appearanceSizer.AddGrowableCol(0)
        appearancePanel.SetSizer(appearanceSizer)

        self._createStyleGui(appearanceSizer, appearancePanel)
        self._createTabWidthGui(appearanceSizer, appearancePanel)
        self._createLineNumGui(appearanceSizer, appearancePanel)
        self._createParentBgGui(appearanceSizer, appearancePanel)

        return appearancePanel

    def _createOkCancelButtons(self, mainSizer):
        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(
            okCancel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
            border=2
        )

    def _createParentBgGui(self, mainSizer, parent):
        """
        Создать элементы интерфейса для опции
            "Использовать фон страницы для блока кода"
        """
        self.parentBgCheckBox = wx.CheckBox(
            parent, -1, _(u"Use the page background for the code block"))

        mainSizer.Add(
            self.parentBgCheckBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=4
        )

    def _createLineNumGui(self, mainSizer, parent):
        """
        Создать элементы интерфейса для добавления номеров строк
        """
        self.lineNumCheckBox = wx.CheckBox(
            parent, -1, _(u"Enable line numbers"))

        mainSizer.Add(
            self.lineNumCheckBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=4
        )

    def _createLanguageGui(self, mainSizer, parent):
        """
        Создать интерфейс, связанный с языком программирования
        """
        langSizer = wx.FlexGridSizer(cols=2)
        langSizer.AddGrowableCol(1)

        languageLabel = wx.StaticText(parent, -1, _(u"Language"))
        self.languageComboBox = wx.ComboBox(
            parent,
            style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.languageComboBox.SetMinSize(wx.Size(self._fieldsWidth, -1))

        langSizer.Add(
            languageLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2
        )

        langSizer.Add(
            self.languageComboBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_RIGHT,
            border=2
        )

        mainSizer.Add(
            langSizer,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=2
        )

    def _createTabWidthGui(self, mainSizer, parent):
        """
        Создать интерфейс, связанный с размером табуляции
        """
        tabSizer = wx.FlexGridSizer(0, 2, 0, 0)
        tabSizer.AddGrowableCol(1)

        tabWidthLabel = wx.StaticText(
            parent, -1, _(u"Tab Width (0 - Default Value)"))
        self.tabWidthSpin = wx.SpinCtrl(
            parent,
            style=wx.SP_ARROW_KEYS | wx.TE_AUTO_URL
        )
        self.tabWidthSpin.SetMinSize(wx.Size(self._fieldsWidth, -1))

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
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
            border=2
        )

    def _createStyleGui(self, mainSizer, parent):
        """
        Создать интерфейс, связанный с выбором стиля оформления
        """
        styleSizer = wx.FlexGridSizer(0, 2, 0, 0)
        styleSizer.AddGrowableCol(1)

        styleLabel = wx.StaticText(parent, -1, _(u"Style"))
        self.styleComboBox = wx.ComboBox(parent,
                                         style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.styleComboBox.SetMinSize(wx.Size(self._fieldsWidth, -1))

        styleSizer.Add(
            styleLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2
        )

        styleSizer.Add(
            self.styleComboBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_RIGHT,
            border=2
        )

        mainSizer.Add(
            styleSizer,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=2
        )

    def _createFileGui(self, mainSizer, parent):
        """
        Создать интерфейс, связанный со вставкой исходников из вложенных файлов
        """
        self.fileCheckBox = wx.CheckBox(
            parent,
            label=_(u"Insert source from file"))

        mainSizer.Add(
            self.fileCheckBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
            border=2
        )

        fileSizer = wx.FlexGridSizer(cols=4)
        fileSizer.AddGrowableCol(2)

        # Список для выбора прикрепленных файлов
        self.attachmentLabel = wx.StaticText(parent, -1, _(u"Attached file"))
        self.attachmentComboBox = wx.ComboBox(
            parent,
            style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.attachmentComboBox.SetMinSize((self._fieldsWidth, -1))

        fileSizer.Add((self._indent, 0))

        fileSizer.Add(
            self.attachmentLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2
        )

        # Кнопка для прикрепления нового файла
        attachImage = wx.Bitmap(getImagePath("attach.png"))
        self.attachButton = wx.BitmapButton(parent, -1, attachImage)
        self.attachButton.SetToolTip(_(u"Attach new files"))

        fileSizer.Add(
            self.attachButton,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2
        )

        fileSizer.Add(
            self.attachmentComboBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2
        )

        # Выбор кодировки файла
        self.encodingLabel = wx.StaticText(parent, -1, _(u"File encoding"))
        self.encodingComboBox = wx.ComboBox(parent,
                                            style=wx.CB_DROPDOWN)

        self.encodingComboBox.SetMinSize((self._fieldsWidth, -1))

        fileSizer.Add((self._indent, 0))

        fileSizer.Add(
            self.encodingLabel,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border=2
        )

        fileSizer.Add((self._indent, 0))

        fileSizer.Add(
            self.encodingComboBox,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2
        )

        mainSizer.Add(
            fileSizer,
            proportion=1,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
            border=2
        )
