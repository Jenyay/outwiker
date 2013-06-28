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

        currentVersion = getCurrentVersion()
        stableVersion = verList.getStableVersion()
        unstableVersion = verList.getUnstableVersion()

        self._updateDialog.setCurrentOutWikerVersion (currentVersion)
        self._updateDialog.setLatestStableOutwikerVersion (stableVersion)
        self._updateDialog.setLatestUnstableOutwikerVersion (unstableVersion)

        self._updateDialog.showUpdateStableOutWiker (currentVersion < stableVersion)
        self._updateDialog.showUpdateUnstableOutWiker (currentVersion < unstableVersion)

        for plugin in self._application.plugins:
            self._updateDialog.addPluginInfo (plugin, verList.getPluginVersion (plugin.name))
        

    def ShowModal (self):
        self._updateVersions()
        return self._updateDialog.ShowModal()
