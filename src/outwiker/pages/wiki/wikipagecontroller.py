# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController
from outwiker.gui.pagedialogpanels.appearancepanel import (AppearancePanel,
                                                           AppearanceController)
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from wikipage import WikiWikiPage
from wikipreferences import WikiPrefGeneralPanel


class WikiPageController (BaseController):
    """GUI controller for wiki page"""
    def __init__(self, application):
        super(WikiPageController, self).__init__()
        self._application = application
        self._appearancePanel = None
        self._appearanceController = None


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate


    def _addTab (self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel (dialog.getPanelsParent())
            dialog.addPanel (self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController (
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController (self._appearanceController)


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == WikiWikiPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController (self._appearanceController)
            params.dialog.removePanel (self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None


    def __onPageDialogDestroy (self, page, params):
        self._appearancePanel = None
        self._appearanceController = None


    def __onPreferencesDialogCreate (self, dialog):
        panel = WikiPrefGeneralPanel (dialog.treeBook)
        prefPanelInfo = PreferencePanelInfo (panel, _(u"General"))

        dialog.appendPreferenceGroup (_(u'Wiki Page'), [prefPanelInfo])
