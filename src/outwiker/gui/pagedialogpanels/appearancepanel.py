# -*- coding: UTF-8 -*-

import os
import os.path

import wx
import wx.combo

from outwiker.core.style import Style
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList
from outwiker.core.commands import MessageBox
from outwiker.core.events import PageDialogPageStyleChangedParams
from outwiker.gui.guiconfig import PageDialogConfig

from basecontroller import BasePageDialogController


class AppearancePanel (wx.Panel):
    def __init__ (self, parent):
        super (AppearancePanel, self).__init__ (parent)

        self.styleText = wx.StaticText (self, -1, _("Page style"))
        self.styleCombo = wx.ComboBox (self,
                                       -1,
                                       choices=[],
                                       style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)

        self.__layout ()


    def __layout (self):
        styleSizer = wx.FlexGridSizer (1, 2, 0, 0)
        styleSizer.AddGrowableCol (1)
        styleSizer.Add (self.styleText, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        styleSizer.Add (self.styleCombo, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 4)

        self.SetSizer (styleSizer)
        self.Layout()


class AppearanceController (BasePageDialogController):
    def __init__ (self, appearancePanel, application, dialog):
        super (AppearanceController, self).__init__ (application)
        self._dialog = dialog
        self._appearancePanel = appearancePanel

        self._currentPage = None
        self._stylesList = None

        self.config = PageDialogConfig (self._application.config)

        self._appearancePanel.styleCombo.Bind (wx.EVT_COMBOBOX,
                                               handler=self.__onStyleChanged)


    def saveParams (self):
        styleName = self._appearancePanel.styleCombo.GetStringSelection()

        # Не будем изменять стиль по умолчанию в случае,
        # если изменяется существующая страница
        if (self._currentPage is None):
            self.config.recentStyle.value = styleName


    def setPageProperties (self, page):
        """
        Return True if success and False otherwise
        """
        if self._appearancePanel.IsShown():
            try:
                Style().setPageStyle (page, self.style)
            except EnvironmentError as e:
                MessageBox (_(u"Can't set page style\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)
                return False

        return True


    def initBeforeCreation (self, parentPage):
        self._initStyleList (None)


    def initBeforeEditing (self, currentPage):
        self._currentPage = currentPage
        self._initStyleList (currentPage)


    def _initStyleList (self, currentPage):
        self._stylesList = StylesList (getStylesDirList ())
        self._fillStyleCombo (self._stylesList, currentPage)


    def _fillStyleCombo (self, styleslist, currentPage=None):
        """
        Заполняет self.appearancePanel.styleCombo списком стилей
        styleslist - список путей до загруженных стилей
        currentPage - страница, для которой вызывается диалог.
        Если currentPage is not None, то первый стиль в списке - это стиль данной страницы
        """
        names = []
        if currentPage is not None:
            names.append (_(u"Do not change"))

        names.append (_(u"Default"))
        style_names = [os.path.basename (style) for style in styleslist]

        names += style_names

        self._appearancePanel.styleCombo.Clear()
        self._appearancePanel.styleCombo.AppendItems (names)

        # Определение последнего используемого стиля
        recentStyle = self.config.recentStyle.value
        names_lower = [name.lower() for name in names]
        try:
            currentStyleIndex = names_lower.index (recentStyle.lower())
        except ValueError:
            currentStyleIndex = 0

        if currentPage is not None:
            # Для уже существующих страниц по умолчанию использовать уже установленный стиль
            currentStyleIndex = 0

        self._appearancePanel.styleCombo.SetSelection (currentStyleIndex)


    def __onStyleChanged (self, event):
        eventParams = PageDialogPageStyleChangedParams (
            self._dialog,
            self.style)

        self._application.onPageDialogPageStyleChanged (
            self._application.selectedPage,
            eventParams)


    def _getStyleByEditing (self):
        selItem = self._appearancePanel.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getPageStyle (self._currentPage)
        elif selItem == 1:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 2]


    def _getStyleByCreation (self):
        selItem = self._appearancePanel.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 1]


    @property
    def style (self):
        style = (self._getStyleByEditing()
                 if self._currentPage is not None
                 else self._getStyleByCreation())

        return style
