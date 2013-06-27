#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.commands import getCurrentVersion

from .versionlist import VersionList
from .updatedialog import UpdateDialog


class UpdateDialogController (object):
    """
    Контроллер для управления UpdateDialog.
    Сюда вынесена вся логика.
    """
    def __init__ (self, application):
        self._application = application
        self._updateDialog = UpdateDialog (self._application.mainWindow)


    def _updateVersions (self):
        verList = VersionList (self._application.plugins)
        verList.updateVersions()

        self._updateDialog.setCurrentOutWikerVersion (getCurrentVersion())
        self._updateDialog.setLatestStableOutwikerVersion (verList.getStableVersion())
        self._updateDialog.setLatestUnstableOutwikerVersion (verList.getUnstableVersion())

        for plugin in self._application.plugins:
            self._updateDialog.addPluginInfo (plugin, verList.getPluginVersion (plugin.name))
        

    def ShowModal (self):
        self._updateVersions()
        return self._updateDialog.ShowModal()
