# -*- coding: utf-8 -*-

from outwiker.api.gui.defines import PREF_PANEL_PLUGINS

from .i18n import get_

from .preferencepanel import PreferencePanel
from .colorslist import ColorsList


class Controller:
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        """ """
        self._plugin = plugin
        self._application = application

        self._colorsList = ColorsList(self._application)

    def _updateColors(self):
        self._colorsList.load()

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        self._application.onPageDialogInit += self.__onPageDialogInit
        self._application.onPageDialogPageTypeChanged += (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onPageDialogInit -= self.__onPageDialogInit
        self._application.onPageDialogPageTypeChanged -= (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

    def __onPageDialogPageTypeChanged(self, page, params):
        color = self._colorsList.getColor(params.pageType)
        params.dialog.generalPanel.titleTextCtrl.SetBackgroundColour(color)
        params.dialog.generalPanel.titleTextCtrl.Refresh()

    def __onPreferencesDialogCreate(self, dialog):
        """
        Add preferences page to dialog
        """
        prefPanel = PreferencePanel(dialog.treeBook, self._application)

        panelName = _("PageTypeColor [Plugin]")
        dialog.addPage(prefPanel, _("PageTypeColor [Plugin]"), parent_page_tag=PREF_PANEL_PLUGINS)

    def __onPageDialogInit(self, page, params):
        self._updateColors()
