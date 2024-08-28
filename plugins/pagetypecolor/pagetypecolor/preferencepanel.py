# -*- coding: utf-8 -*-

import wx

from outwiker.api.core.events import PageDialogPageFactoriesNeededParams
from outwiker.api.gui.preferences import BasePrefPanel

from pagetypecolor.i18n import get_
from pagetypecolor.colorslist import ColorsList


class PreferencePanel(BasePrefPanel):
    """
    Панель с настройками
    """

    def __init__(self, parent, application):
        """
        parent - родитель панели (должен быть wx.Treebook)
        """
        super().__init__(parent)
        self._application = application

        global _
        _ = get_()

        # Key - page type string, value - ColorPicker instance
        self._colorPickers = {}
        self._colorsList = ColorsList(self._application)

        self._createGui()
        self.SetupScrolling()

    def _createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        descriptionLabel = wx.StaticText(
            self, -1, _("The colors for the various page types")
        )

        mainSizer.Add(
            descriptionLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        mainSizer.AddSpacer(0)

        eventParams = PageDialogPageFactoriesNeededParams(None, None)
        self._application.onPageDialogPageFactoriesNeeded(None, eventParams)

        for factory in eventParams.pageFactories:
            label, colorPicker = self._createLabelAndColorPicker(
                factory.title, mainSizer
            )
            self._colorPickers[factory.getPageTypeString()] = colorPicker

        self.SetSizer(mainSizer)

    def LoadState(self):
        self._colorsList.load()
        for pageType in self._colorsList.getPageTypes():
            if pageType in self._colorPickers:
                color = self._colorsList.getColor(pageType)
                self._colorPickers[pageType].SetColour(color)

    def Save(self):
        self._colorsList.load()
        for pageType in self._colorsList.getPageTypes():
            if pageType in self._colorPickers:
                color = (
                    self._colorPickers[pageType]
                    .GetColour()
                    .GetAsString(wx.C2S_HTML_SYNTAX)
                )
                self._colorsList.setColor(pageType, color)
