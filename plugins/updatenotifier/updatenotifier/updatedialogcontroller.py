#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version

from .versionlist import VersionList
from .updatedialog import UpdateDialog
from .longprocessrunner import LongProcessRunner
from .i18n import get_


class UpdateDialogController (object):
    """
    Контроллер для управления UpdateDialog.
    Сюда вынесена вся логика.
    """
    def __init__ (self, application):
        global _
        _ = get_()

        self._application = application
        self._updateDialog = UpdateDialog (self._application.mainWindow)


    def _updateVersions (self):
        verList = VersionList (self._application.plugins)
        verList.updateVersions()

        currentVersion = getCurrentVersion()
        stableVersion = verList.getStableVersion()
        unstableVersion = verList.getUnstableVersion()

        self._updateDialog.setCurrentOutWikerVersion (currentVersion)
        self._updateDialog.setLatestStableOutwikerVersion (stableVersion, currentVersion < stableVersion)
        self._updateDialog.setLatestUnstableOutwikerVersion (unstableVersion, currentVersion < unstableVersion)

        for plugin in self._application.plugins:
            pluginVersion = verList.getPluginVersion (plugin.name)

            try:
                currentPluginVersion = Version.parse (plugin.version)
            except ValueError:
                continue

            try:
                pluginUrl = verList.getPluginUrl (plugin.name)
            except KeyError:
                continue

            if (pluginVersion != None and
                    pluginVersion > currentPluginVersion):
                self._updateDialog.addPluginInfo (plugin,
                        pluginVersion,
                        verList.getPluginUrl (plugin.name))


    def ShowModal (self):
        # self._updateVersions()

        progressRunner = LongProcessRunner (self._updateVersions, 
                self._application.mainWindow,
                dialogTitle = u"UpdateNotifier",
                dialogText = _(u"Check for new versions..."))

        progressRunner.run()

        return self._updateDialog.ShowModal()
