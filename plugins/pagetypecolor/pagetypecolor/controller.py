# -*- coding: UTF-8 -*-

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from .i18n import get_

from config import PageTypeColorConfig
from preferencepanel import PreferencePanel


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._colors = {}


    def _updateColors (self):
        config = PageTypeColorConfig (self._application.config)
        self._colors = {
            u'wiki': config.wikiColor.value,
            u'html': config.htmlColor.value,
            u'text': config.textColor.value,
            u'search': config.searchColor.value,
        }


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._updateColors()
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self._application.onPreferencesDialogClose += self.__onPreferencesDialogClose


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self._application.onPreferencesDialogClose -= self.__onPreferencesDialogClose


    def __onPageDialogPageTypeChanged (self, page, params):
        color = self._colors.get (params.pageType, 'white')
        params.dialog.generalPanel.titleTextCtrl.SetBackgroundColour (color)


    def __onPreferencesDialogCreate (self, dialog):
        """
        Add preferences page to dialog
        """
        prefPanel = PreferencePanel (dialog.treeBook, self._application.config)

        panelName = _(u"PageTypeColor [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)


    def __onPreferencesDialogClose (self, dialog):
        self._updateColors()
