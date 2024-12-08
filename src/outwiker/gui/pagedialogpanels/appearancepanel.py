# -*- coding: utf-8 -*-

import os
import os.path
from typing import List

import wx

from outwiker.core.tree import WikiPage
from outwiker.gui.dialogs.messagebox import MessageBox
from outwiker.core.style import Style
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList
from outwiker.core.events import PageDialogPageStyleChangedParams, PAGE_UPDATE_COLOR
from outwiker.gui.controls.colorcombobox import ColorComboBox
from outwiker.gui.guiconfig import PageDialogConfig
from outwiker.gui.pagedialogpanels.basecontroller import BasePageDialogController


class AppearancePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self._createStyleGui()
        self._createTitleColorGui()
        self._layout()

    def _createTitleColorGui(self):
        self.titleColorText = wx.StaticText(self, label=_("Title color"))
        self.titleColorBox = ColorComboBox(self)
        self.titleColorBox.SetMinSize((200, -1))

    def _createStyleGui(self):
        self.styleText = wx.StaticText(self, label=_("Page style"))
        self.styleCombo = wx.ComboBox(
            self, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY
        )
        self.styleCombo.SetMinSize((200, -1))

    def _layout(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(1)

        # Page style
        mainSizer.Add(self.styleText, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add(
            self.styleCombo,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=4,
        )

        # Title color
        mainSizer.Add(
            self.titleColorText, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4
        )
        mainSizer.Add(
            self.titleColorBox,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=4,
        )

        self.SetSizer(mainSizer)
        self.Layout()


class AppearanceController(BasePageDialogController):
    def __init__(self, appearancePanel: AppearancePanel, application, dialog):
        super().__init__(application)
        self._dialog = dialog
        self._appearancePanel = appearancePanel

        self._currentPage = None
        self._stylesList = None

        self.config = PageDialogConfig(self._application.config)
        self._initTitleColorsList()

        self._appearancePanel.styleCombo.Bind(
            wx.EVT_COMBOBOX, handler=self.__onStyleChanged
        )

    def _initTitleColorsList(self):
        pageTitleColors = [
            wx.Colour(color_txt)
            for color_txt in self.config.PageTitleColors.value
            if wx.Colour(color_txt).IsOk()
        ]

        self._appearancePanel.titleColorBox.AddColors(pageTitleColors)

    def _getColorsAsStrings(self, colors: List[wx.Colour]) -> List[str]:
        return [color.GetAsString(wx.C2S_HTML_SYNTAX) for color in colors]

    def saveParams(self):
        styleName = self._appearancePanel.styleCombo.GetStringSelection()

        # Не будем изменять стиль по умолчанию в случае,
        # если изменяется существующая страница
        if self._currentPage is None:
            self.config.recentStyle.value = styleName

        # Store page title colors
        pageTitleColors = self._getColorsAsStrings(
            self._appearancePanel.titleColorBox.GetColors()
        )
        self.config.PageTitleColors.value = pageTitleColors

    def setPageProperties(self, page: WikiPage):
        """
        Return True if success and False otherwise
        """
        try:
            Style().setPageStyle(page, self.style)
        except EnvironmentError as e:
            MessageBox(
                _("Can't set page style\n") + str(e), _("Error"), wx.ICON_ERROR | wx.OK
            )
            return False

        oldTitleColor = wx.Colour(page.params.titleColorOption.value)
        newTitleColor = self._appearancePanel.titleColorBox.GetSelectedColor()
        if oldTitleColor != newTitleColor:
            page.params.titleColorOption.value = (
                newTitleColor.GetAsString(wx.C2S_HTML_SYNTAX)
                if newTitleColor is not None
                else ""
            )
            page.root.onPageUpdate(page, change=PAGE_UPDATE_COLOR)
        return True

    def initBeforeCreation(self, parentPage):
        self._initStyleList(None)

    def initBeforeEditing(self, currentPage: WikiPage):
        self._currentPage = currentPage
        self._initStyleList(currentPage)
        titleColor = wx.Colour(currentPage.params.titleColorOption.value)
        if titleColor.IsOk():
            titleColorIndex = self._appearancePanel.titleColorBox.FindColor(titleColor)
            if titleColorIndex is not None:
                self._appearancePanel.titleColorBox.SetSelection(titleColorIndex)
            else:
                self._appearancePanel.titleColorBox.InsertColor(1, titleColor)
                self._appearancePanel.titleColorBox.SetSelection(1)

    def clear(self):
        self._dialog = None
        self._iconsPanel = None

    def _initStyleList(self, currentPage):
        self._stylesList = StylesList(getStylesDirList())
        self._fillStyleCombo(self._stylesList, currentPage)

    def _fillStyleCombo(self, styleslist, currentPage=None):
        """
        Заполняет self.appearancePanel.styleCombo списком стилей
        styleslist - список путей до загруженных стилей
        currentPage - страница, для которой вызывается диалог.
        Если currentPage is not None, то первый стиль в списке - это стиль
            данной страницы
        """
        names = []
        if currentPage is not None:
            names.append(_("Do not change"))

        names.append(_("Default"))
        style_names = [os.path.basename(style) for style in styleslist]

        names += style_names

        self._appearancePanel.styleCombo.Clear()
        self._appearancePanel.styleCombo.AppendItems(names)

        # Определение последнего используемого стиля
        recentStyle = self.config.recentStyle.value
        names_lower = [name.lower() for name in names]
        try:
            currentStyleIndex = names_lower.index(recentStyle.lower())
        except ValueError:
            currentStyleIndex = 0

        if currentPage is not None:
            # Для уже существующих страниц по умолчанию использовать
            # уже установленный стиль
            currentStyleIndex = 0

        self._appearancePanel.styleCombo.SetSelection(currentStyleIndex)

    def __onStyleChanged(self, event):
        eventParams = PageDialogPageStyleChangedParams(self._dialog, self.style)

        self._application.onPageDialogPageStyleChanged(
            self._application.selectedPage, eventParams
        )

    def _getStyleByEditing(self):
        selItem = self._appearancePanel.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getPageStyle(self._currentPage)
        elif selItem == 1:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 2]

    def _getStyleByCreation(self):
        selItem = self._appearancePanel.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 1]

    @property
    def style(self):
        style = (
            self._getStyleByEditing()
            if self._currentPage is not None
            else self._getStyleByCreation()
        )

        return style
