# -*- coding: UTF-8 -*-

import wx

from i18n import get_
from config import PageTypeColorConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class PreferencePanel(BasePrefPanel):
    """
    Панель с настройками
    """
    def __init__(self, parent, config):
        """
        parent - родитель панели(должен быть wx.Treebook)
        config - настройки из plugin._application.config
        """
        super(PreferencePanel, self).__init__(parent)

        global _
        _ = get_()

        self.__createGui()
        self.__controller = PrefPanelController(self, config)
        self._setScrolling()

    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        descriptionLabel = wx.StaticText(
            self,
            -1,
            _(u'The colors for the various page types')
        )

        mainSizer.Add(descriptionLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.AddSpacer(0)

        wikiLabel, self._wikiColorPicker = self._createLabelAndColorPicker(
            _(u'Wiki page'),
            mainSizer
        )

        htmlLabel, self._htmlColorPicker = self._createLabelAndColorPicker(
            _(u'HTML page'),
            mainSizer
        )

        textLabel, self._textColorPicker = self._createLabelAndColorPicker(
            _(u'Text page'),
            mainSizer
        )

        searchLabel, self._searchColorPicker = self._createLabelAndColorPicker(
            _(u'Search page'),
            mainSizer
        )

        self.SetSizer(mainSizer)

    @property
    def wikiColor(self):
        return self._wikiColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

    @wikiColor.setter
    def wikiColor(self, value):
        self._wikiColorPicker.SetColour(value)

    @property
    def htmlColor(self):
        return self._htmlColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

    @htmlColor.setter
    def htmlColor(self, value):
        self._htmlColorPicker.SetColour(value)

    @property
    def textColor(self):
        return self._textColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

    @textColor.setter
    def textColor(self, value):
        self._textColorPicker.SetColour(value)

    @property
    def searchColor(self):
        return self._searchColorPicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

    @searchColor.setter
    def searchColor(self, value):
        self._searchColorPicker.SetColour(value)

    def LoadState(self):
        self.__controller.loadState()

    def Save(self):
        self.__controller.save()


class PrefPanelController(object):
    """
    Контроллер для панели настроек
    """
    def __init__(self, ownerPanel, config):
        self._panel = ownerPanel
        self._config = PageTypeColorConfig(config)

    def loadState(self):
        self._panel.wikiColor = self._config.wikiColor.value
        self._panel.htmlColor = self._config.htmlColor.value
        self._panel.textColor = self._config.textColor.value
        self._panel.searchColor = self._config.searchColor.value

    def save(self):
        self._config.wikiColor.value = self._panel.wikiColor
        self._config.htmlColor.value = self._panel.htmlColor
        self._config.textColor.value = self._panel.textColor
        self._config.searchColor.value = self._panel.searchColor
