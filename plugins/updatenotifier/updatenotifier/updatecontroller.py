# -*- coding: UTF-8 -*-

import datetime
import logging
import threading
import os.path

import wx

from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version
from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.core.xmlversionparser import XmlVersionParser
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

logger = logging.getLogger('UpdateNotifierPlugin')


class UpdateController(object):
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

        self._updateUrls = self._getPluginsUpdateUrls(self._application.plugins)
        self._updateUrls[u'OUTWIKER_STABLE'] = u'http://jenyay.net/uploads/Soft/Outwiker/versions.xml'
        self._updateUrls[u'OUTWIKER_UNSTABLE'] = u'http://jenyay.net/uploads/Outwiker/Unstable/versions.xml'

        # Экземпляр потока, который будет проверять новые версии
        self._silenceThread = None
        if self._application.mainWindow is not None:
            self._application.mainWindow.Bind(
                EVT_UPDATE_VERSIONS,
                handler=self._onSilenceVersionUpdate)

    def _getPluginsUpdateUrls(self, plugins):
        '''
        plugins - instance of the PluginsLoader
        Return dict which key is plugin name, value is updatesUrl
        '''
        result = {}

        for plugin in plugins:
            xmlPath = os.path.join(plugin._pluginPath,
                                   PLUGIN_VERSION_FILE_NAME)
            try:
                xmlText = readTextFile(xmlPath)
            except IOError:
                logger.warning(u"Can't read {}".format(xmlPath))
                continue

            versionParser = XmlVersionParser([_(u'__updateLang'), u'en'])
            try:
                result[plugin.name] = versionParser.parse(xmlText).updatesUrl
            except ValueError:
                logger.warning(u"Invalid format {}".format(xmlPath))
                continue

        return result

    def _showUpdates(self, verList):
        """
        Сверяем полученные номера версий с теми,
        что установлены сейчас и заполняем диалог изменениями (updateDialog)
        Возвращает True, если есть какие-нибудь обновления
        """
        setStatusText(u"")

        currentVersion = getCurrentVersion()
        stableAppInfo = verList[u'OUTWIKER_STABLE']
        unstableAppInfo = verList[u'OUTWIKER_UNSTABLE']

        updatedPluginsInfo = self.getUpdatedPlugins(verList)
        currentPluginsVersions = {plugin.name: plugin.version
                                  for plugin
                                  in self._application.plugins}
        template = readTextFile(self._updateTemplatePath)

        templateData = {
            u'outwiker_current_version': currentVersion,
            u'stableAppInfo': stableAppInfo,
            u'unstableAppInfo': unstableAppInfo,
            u'updatedPluginsInfo': updatedPluginsInfo,
            u'currentPluginsVersions': currentPluginsVersions,
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
        stableVersion = verList[u'OUTWIKER_STABLE']
        unstableVersion = verList[u'OUTWIKER_UNSTABLE']

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
            plugin_name = plugin.name
            appInfo = verList[plugin_name]

            if appInfo is None:
                continue

            pluginVersion = appInfo.currentVersion

            try:
                currentPluginVersion = Version.parse(plugin.version)
            except ValueError:
                continue

            try:
                pluginInfo = verList[plugin_name]
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
        verList = VersionList(self._updateUrls)

        if (self._silenceThread is None or not self._silenceThread.isAlive()):
            self._silenceThread = threading.Thread(None,
                                                   self._silenceThreadFunc,
                                                   args=(verList,))
            self._silenceThread.start()

    def checkForUpdates(self):
        """
        Проверить обновления и показать диалог с результатами
        """
        verList = VersionList(self._updateUrls)
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
