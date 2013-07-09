#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.commands import getCurrentVersion, MessageBox
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


    def _prepareUpdates (self, verList, updateDialog):
        """
        Сверяем полученные номера версий с теми, что установлены сейчас и заполняем диалог изменениями (updateDialog)
        Возвращает True, если есть какие-нибудь обновления
        """
        currentVersion = getCurrentVersion()
        stableVersion = verList.getStableVersion()
        unstableVersion = verList.getUnstableVersion()

        # Есть ли какие-нибудь обновления?
        hasUpdates = False

        updateDialog.setCurrentOutWikerVersion (currentVersion)

        if stableVersion != None:
            hasUpdates = hasUpdates or (currentVersion < stableVersion)
            updateDialog.setLatestStableOutwikerVersion (stableVersion, currentVersion < stableVersion)
        else:
            updateDialog.setLatestStableOutwikerVersion (currentVersion, False)

        if unstableVersion != None:
            hasUpdates = hasUpdates or (currentVersion < unstableVersion)
            updateDialog.setLatestUnstableOutwikerVersion (unstableVersion, currentVersion < unstableVersion)
        else:
            updateDialog.setLatestUnstableOutwikerVersion (currentVersion, False)

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
                updateDialog.addPluginInfo (plugin,
                        pluginVersion,
                        verList.getPluginUrl (plugin.name))
                hasUpdates = True

        return hasUpdates


    def ShowModal (self):
        """
        Проверить обновления и показать диалог с результатами
        """
        verList = VersionList (self._application.plugins)

        progressRunner = LongProcessRunner (verList.updateVersions, 
                self._application.mainWindow,
                dialogTitle = u"UpdateNotifier",
                dialogText = _(u"Check for new versions..."))

        progressRunner.run()
        # verList.updateVersions()

        updateDialog = UpdateDialog (self._application.mainWindow)
        hasUpdates = self._prepareUpdates (verList, updateDialog)

        if hasUpdates:
            updateDialog.ShowModal()
        else:
            MessageBox (_(u"Updates not found"),
                    u"UpdateNotifier")
