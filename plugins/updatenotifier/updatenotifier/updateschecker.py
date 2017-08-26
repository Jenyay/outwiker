# -*- coding: UTF-8 -*-

import datetime
import threading
import os.path

import wx

from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version
from outwiker.utilites.textfile import readTextFile

from .longprocessrunner import LongProcessRunner
from .updatedialog import UpdateDialog
from .updatesconfig import UpdatesConfig
from .versionlist import VersionList
from .i18n import get_
from .contentgenerator import ContentGenerator

# Событие срабатывает, когда завершается "молчаливое" обновление списка версий
# Параметр verList - экземпляр класса VersionList
UpdateVersionsEvent, EVT_UPDATE_VERSIONS = wx.lib.newevent.NewEvent()


class UpdatesChecker(object):
    """
    Контроллер для управления UpdateDialog.
    Сюда вынесена вся логика.
    """
    def __init__(self, application, pluginPath):
        global _
        _ = get_()

        self._application = application
        self._config = UpdatesConfig(self._application.config)
        self._dataPath = os.path.join(pluginPath, u'data')
        self._updateTemplatePath = os.path.join(self._dataPath, u'update.html')

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
        stableAppInfo = verList.stableVersionInfo
        unstableAppInfo = verList.unstableVersionInfo

        updatedPluginsInfo = self.getUpdatedPlugins(verList)
        currentPluginsInfo = verList.currentPluginsInfo
        template = readTextFile(self._updateTemplatePath)

        templateData = {
            u'outwiker_current_version': currentVersion,
            u'stableAppInfo': stableAppInfo,
            u'unstableAppInfo': unstableAppInfo,
            u'updatedPluginsInfo': updatedPluginsInfo,
            u'currentPluginsInfo': currentPluginsInfo,
            u'str_outwiker_current_version': _(u'Installed OutWiker version'),
            u'str_outwiker_latest_stable_version': _(u'Latest stable OutWiker version'),
            u'str_outwiker_latest_unstable_version': _(u'Latest unstable OutWiker version'),
            u'str_version_history': _(u'Version history'),
            u'str_more_info': _(u'More info'),
            u'str_download': _(u'Download'),
        }

        contentGenerator = ContentGenerator(template)
        HTMLContent = contentGenerator.render(templateData)

        with UpdateDialog(self._application.mainWindow) as updateDialog:
            basepath = self._dataPath
            updateDialog.setContent(HTMLContent, basepath)
            updateDialog.ShowModal()

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
        updatedPlugins = {}

        for plugin in self._application.plugins:
            appInfo = verList.latestPluginsInfo[plugin.name]
            if appInfo is None:
                continue

            pluginVersion = appInfo.currentVersion

            try:
                currentPluginVersion = Version.parse(plugin.version)
            except ValueError:
                continue

            try:
                pluginInfo = verList.latestPluginsInfo[plugin.name]
                pluginInfo.currentVersion
            except KeyError:
                continue

            if (pluginVersion is not None and
                    pluginVersion > currentPluginVersion):
                updatedPlugins[plugin.name] = appInfo

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
