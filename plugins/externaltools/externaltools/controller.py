# -*- coding: UTF-8 -*-

from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from i18n import get_
from menutoolscontroller import MenuToolsController


class Controller (object):
    """
    Этот класс отвечает за основную работу плагина
    """
    def __init__ (self, ownerPlugin):
        self._owner = ownerPlugin
        self._page = None
        self._menuToolsController = MenuToolsController (ownerPlugin.application)


    def initialize (self):
        global _
        _ = get_()

        self._menuToolsController.initialize()
        self._owner.application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate


    def destroy (self):
        self._menuToolsController.destroy()
        self._owner.application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate


    def __onPreferencesDialogCreate (self, dialog):
        from .preferencespanel import PreferencesPanel
        prefPanel = PreferencesPanel (dialog.treeBook, self._owner.application.config)

        panelName = _(u"External Tools [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)
