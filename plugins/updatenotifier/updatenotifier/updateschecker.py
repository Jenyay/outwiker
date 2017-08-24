# -*- coding: UTF-8 -*-

import datetime
import threading

import wx

from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version

from .longprocessrunner import LongProcessRunner
from .updatedialog import UpdateDialog
from .updatesconfig import UpdatesConfig
from .versionlist import VersionList
from .i18n import get_

# Событие срабатывает, когда завершается "молчаливое" обновление списка версий
# Параметр verList - экземпляр класса VersionList
UpdateVersionsEvent, EVT_UPDATE_VERSIONS = wx.lib.newevent.NewEvent()


class UpdatesChecker(object):
    """
    Контроллер для управления UpdateDialog.
    Сюда вынесена вся логика.
    """
    def __init__(self, application):
        global _
        _ = get_()

        self._application = application
        self._config = UpdatesConfig(self._application.config)

        # Экземпляр потока, который будет проверять новые версии
        self._silenceThread = None
        if self._application.mainWindow is not None:
            self._application.mainWindow.Bind(
                EVT_UPDATE_VERSIONS,
                handler=self._onSilenceVersionUpdate)

    def _showUpdates(self, verList):
        """
        Сверяем полученные номера версий с теми,
        что установлены сейчас и заполняем диалог изменениями(updateDialog)
        Возвращает True, если есть какие-нибудь обновления
        """
        setStatusText(u"")

        currentVersion = getCurrentVersion()
        stableVersion = verList.stableVersionInfo
        unstableVersion = verList.unstableVersionInfo

        updatedPlugins = self.getUpdatedPlugins(verList)

        updateDialog = UpdateDialog(self._application.mainWindow)
        updateDialog.setCurrentOutWikerVersion(currentVersion)

        if stableVersion is not None:
            updateDialog.setLatestStableOutwikerVersion(
                stableVersion.currentVersion,
                currentVersion < stableVersion.currentVersion)
        else:
            updateDialog.setLatestStableOutwikerVersion(currentVersion, False)

        if unstableVersion is not None:
            updateDialog.setLatestUnstableOutwikerVersion(
                unstableVersion.currentVersion,
                currentVersion < unstableVersion.currentVersion)
        else:
            updateDialog.setLatestUnstableOutwikerVersion(
                currentVersion,
                False)

        for plugin in updatedPlugins:
            pluginInfo = verList.getPluginInfo(plugin.name)

            updateDialog.addPluginInfo(
                plugin,
                pluginInfo.currentVersion,
                pluginInfo.appwebsite)

        updateDialog.ShowModal()
        updateDialog.Destroy()

    def hasUpdates(self, verList):
        """
        Возвращает True, если есть обновления в плагинах или самой программы
        """
        currentVersion = getCurrentVersion()
        stableVersion = verList.stableVersionInfo
        unstableVersion = verList.unstableVersionInfo

        updatedPlugins = self.getUpdatedPlugins(verList)

        # Обновилась ли нестабильная версия(или игнорируем ее)
        unstableUpdate = (unstableVersion is not None and
                          currentVersion < unstableVersion.currentVersion and
                          not self._config.ignoreUnstable)

        stableUpdate = (stableVersion is not None and
                        currentVersion < stableVersion.currentVersion)

        result = len(updatedPlugins) != 0 or unstableUpdate or stableUpdate

        return result

    def getUpdatedPlugins(self, verList):
        """
        Возвращает список плагинов, которые обновились
        """
        updatedPlugins = []

        for plugin in self._application.plugins:
            appInfo = verList.getPluginInfo(plugin.name)
            if appInfo is None:
                continue

            pluginVersion = appInfo.currentVersion

            try:
                currentPluginVersion = Version.parse(plugin.version)
            except ValueError:
                continue

            try:
                pluginInfo = verList.getPluginInfo(plugin.name)
                pluginInfo.currentVersion
            except KeyError:
                continue

            if (pluginVersion is not None and
                    pluginVersion > currentPluginVersion):
                updatedPlugins.append(plugin)

        return updatedPlugins

    def _onSilenceVersionUpdate(self, event):
        setStatusText(u"")

        self._touchLastUpdateDate()

        if self.hasUpdates(event.verList):
            self._showUpdates(event.verList)

        self._silenceThread = None

    def _touchLastUpdateDate(self):
        self._config.lastUpdate = datetime.datetime.today()

    def _silenceThreadFunc(self, verList):
        """
        Функция потока для молчаливой проверки обновлений
        """
        verList.updateVersions()
        event = UpdateVersionsEvent(verList=verList)

        if self._application.mainWindow:
            wx.PostEvent(self._application.mainWindow, event)

    def checkForUpdatesSilence(self):
        """
        Молчаливое обновление списка версий
        """
        setStatusText(_(u"Check for new versions..."))
        verList = VersionList(self._application.plugins)

        if (self._silenceThread is None or not self._silenceThread.isAlive()):
            self._silenceThread = threading.Thread(None,
                                                   self._silenceThreadFunc,
                                                   args=(verList,))
            self._silenceThread.start()

    def checkForUpdates(self):
        """
        Проверить обновления и показать диалог с результатами
        """
        verList = VersionList(self._application.plugins)
        setStatusText(_(u"Check for new versions..."))

        progressRunner = LongProcessRunner(
            verList.updateVersions,
            self._application.mainWindow,
            dialogTitle=u"UpdateNotifier",
            dialogText=_(u"Check for new versions..."))

        progressRunner.run()

        self._touchLastUpdateDate()

        if self.hasUpdates(verList):
            self._showUpdates(verList)
        else:
            MessageBox(_(u"Updates not found"),
                       u"UpdateNotifier")
