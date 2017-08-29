# -*- coding: UTF-8 -*-

import datetime
import logging
import threading
import os.path

import wx

from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version
from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile

from .updatedialog import UpdateDialog
from .updatesconfig import UpdatesConfig
from .versionlist import VersionList
from .i18n import get_
from .contentgenerator import ContentGenerator

# The event occures after finish cheching latest versions.
# The parameters:
#     verList - instance of the VersionList class
#     silenceMode - True if the theread was runned in the silence mode.
UpdateVersionsEvent, EVT_UPDATE_VERSIONS = wx.lib.newevent.NewEvent()

logger = logging.getLogger('UpdateNotifierPlugin')


class UpdateController(object):
    """
    Controller for updates checking and show information.
    """
    def __init__(self, application, pluginPath):
        '''
        application - instance of the ApplicationParams class.
        pluginPath - path to UpdatesNotifier plugin.
        '''
        global _
        _ = get_()

        self._application = application
        self._config = UpdatesConfig(self._application.config)
        self._dataPath = os.path.join(pluginPath, u'data')
        self._updateTemplatePath = os.path.join(self._dataPath, u'update.html')

        # Special string id for stable and unstable OutWiker URL
        self._OUTWIKER_STABLE_KEY = u'OUTWIKER_STABLE'
        self._OUTWIKER_UNSTABLE_KEY = u'OUTWIKER_UNSTABLE'

        # Dictionary. Key - plugin name or special string id,
        # Value - URL to XML file with versions information.
        self._updateUrls = self._getPluginsUpdateUrls(self._application.plugins)
        self._updateUrls[self._OUTWIKER_STABLE_KEY] = u'http://jenyay.net/uploads/Soft/Outwiker/versions.xml'
        self._updateUrls[self._OUTWIKER_UNSTABLE_KEY] = u'http://jenyay.net/uploads/Outwiker/Unstable/versions.xml'

        # The thread to check updates in the silence mode (after program start)
        self._silenceThread = None
        if self._application.mainWindow is not None:
            self._application.mainWindow.Bind(
                EVT_UPDATE_VERSIONS,
                handler=self._onVersionUpdate)

    def checkForUpdatesSilence(self):
        """
        Execute the silence update checking.
        """
        setStatusText(_(u"Check for new versions..."))
        verList = VersionList(self._updateUrls)

        if (self._silenceThread is None or not self._silenceThread.isAlive()):
            self._silenceThread = threading.Thread(None,
                                                   self._threadFunc,
                                                   args=(verList, True))
            self._silenceThread.start()

    def checkForUpdates(self):
        """
        Execute updates checking and show dialog with the results.
        """
        verList = VersionList(self._updateUrls)
        setStatusText(_(u"Check for new versions..."))

        progressRunner = LongProcessRunner(
            self._threadFunc,
            self._application.mainWindow,
            dialogTitle=u"UpdateNotifier",
            dialogText=_(u"Check for new versions..."))

        progressRunner.run(verList, silenceMode=False)

    def createHTMLContent(self, updatedAppInfo):
        currentVersion = getCurrentVersion()
        currentVersionsList = self._getCurrentVersionsList()

        template = readTextFile(self._updateTemplatePath)

        templateData = {
            u'outwiker_current_version': currentVersion,
            u'updatedAppInfo': updatedAppInfo,
            u'currentVersionsList': currentVersionsList,
            u'str_outwiker_current_version': _(u'Installed OutWiker version'),
            u'str_outwiker_latest_stable_version': _(u'Latest stable OutWiker version'),
            u'str_outwiker_latest_unstable_version': _(u'Latest unstable OutWiker version'),
            u'str_version_history': _(u'Version history'),
            u'str_more_info': _(u'More info'),
            u'str_download': _(u'Download'),
        }

        contentGenerator = ContentGenerator(template)
        HTMLContent = contentGenerator.render(templateData)
        return HTMLContent

    @staticmethod
    def filterUpdatedApps(currentVersionsList, latestAppInfoList):
        """
        Return dictionary with the AppInfo fot updated apps only.
        """
        updatedPlugins = {}

        for app_name, version_str in currentVersionsList.iteritems():
            latestAppInfo = latestAppInfoList[app_name]

            if latestAppInfo is None:
                continue

            try:
                currentPluginVersion = Version.parse(version_str)
            except ValueError:
                continue

            latestVersion = latestAppInfo.currentVersion
            if (latestVersion is not None and
                    latestVersion > currentPluginVersion):
                updatedPlugins[app_name] = latestAppInfo

        return updatedPlugins

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

    def _getUpdatedAppInfo(self, latestVersionsList):
        '''
        Get AppInfo instances for updated apps (plugins and OutWiker) only.
        '''
        currentVersionsList = self._getCurrentVersionsList()
        updatedAppInfo = self.filterUpdatedApps(currentVersionsList,
                                                latestVersionsList)
        return updatedAppInfo

    def _getCurrentVersionsList(self):
        '''
        Return dictionary with apps versions. Key - plugin name or special id,
        Value - string with version.
        '''
        currentVersion = getCurrentVersion()

        currentVersionsList = {plugin.name: plugin.version
                               for plugin
                               in self._application.plugins}

        currentVersionsList[self._OUTWIKER_STABLE_KEY] = unicode(currentVersion)
        currentVersionsList[self._OUTWIKER_UNSTABLE_KEY] = unicode(currentVersion)

        return currentVersionsList

    def _showUpdates(self, updatedAppInfo):
        '''
        Show dialog with update information.
        '''
        setStatusText(u"")

        HTMLContent = self.createHTMLContent(updatedAppInfo)

        with UpdateDialog(self._application.mainWindow) as updateDialog:
            basepath = self._dataPath
            updateDialog.setContent(HTMLContent, basepath)
            updateDialog.ShowModal()

    def _onVersionUpdate(self, event):
        '''
        Event handler for EVT_UPDATE_VERSIONS.
        '''
        setStatusText(u"")

        self._touchLastUpdateDate()
        updatedAppInfo = self._getUpdatedAppInfo(event.verList)

        if updatedAppInfo:
            self._showUpdates(updatedAppInfo)
        elif not event.silenceMode:
            MessageBox(_(u"Updates not found"), u"UpdateNotifier")

    def _touchLastUpdateDate(self):
        '''
        Save latest updates checking time.
        '''
        self._config.lastUpdate = datetime.datetime.today()

    def _threadFunc(self, verList, silenceMode):
        """
        Thread function for silence updates checking
        """
        verList.updateVersions()
        event = UpdateVersionsEvent(verList=verList, silenceMode=silenceMode)

        if self._application.mainWindow:
            wx.PostEvent(self._application.mainWindow, event)
