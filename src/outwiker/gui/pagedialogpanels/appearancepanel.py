# -*- coding: UTF-8 -*-

import os
import os.path

import wx
import wx.combo

from outwiker.core.style import Style
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList
from outwiker.gui.guiconfig import PageDialogConfig

from basepanel import BasePageDialogPanel


class AppearancePanel (BasePageDialogPanel):
    def __init__ (self, parent, application):
        super (AppearancePanel, self).__init__ (parent, application)

        self._currentPage = None
        self._stylesList = None
        self.config = PageDialogConfig (self._application.config)

        self.styleText = wx.StaticText (self, -1, _("Page style"))
        self.styleCombo = wx.ComboBox (self,
                                       -1,
                                       choices=[],
                                       style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)

        self.__layout ()


    @property
    def title (self):
        return _(u'Appearance')


    def __layout (self):
        styleSizer = wx.FlexGridSizer (1, 2, 0, 0)
        styleSizer.AddGrowableCol (1)
        styleSizer.Add (self.styleText, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        styleSizer.Add (self.styleCombo, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 4)

        self.SetSizer (styleSizer)
        self.Layout()


    def initBeforeCreation (self, parentPage):
        self._initStyleList (None)


    def initBeforeEditing (self, currentPage):
        self._currentPage = currentPage
        self._initStyleList (currentPage)


    def _initStyleList (self, currentPage):
        self._stylesList = StylesList (getStylesDirList ())
        self._fillStyleCombo (self._stylesList, currentPage)


    def _getStyleByEditing (self):
        selItem = self.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getPageStyle (self._currentPage)
        elif selItem == 1:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 2]


    def _getStyleByCreation (self):
        selItem = self.styleCombo.GetSelection()
        if selItem == 0:
            return Style().getDefaultStyle()

        return self._stylesList[selItem - 1]


    @property
    def style (self):
        style = (self._getStyleByEditing()
                 if self._currentPage is not None
                 else self._getStyleByCreation())

        return style


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

        self.styleCombo.Clear()
        self.styleCombo.AppendItems (names)

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

        self.styleCombo.SetSelection (currentStyleIndex)


    def saveParams (self):
        styleName = self.styleCombo.GetStringSelection()

        # Не будем изменять стиль по умолчанию в случае,
        # если изменяется существующая страница
        if (self._currentPage is None):
            self.config.recentStyle.value = styleName
