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
#     appInfoDict - dictionary. Key - plugin name or special id,
#                               value - AppInfo instance.
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
        pluginPath - path to UpdateNotifier plugin.
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

        if (self._silenceThread is None or not self._silenceThread.isAlive()):
            self._silenceThread = threading.Thread(
                None,
                self._threadFunc,
                args=(self._updateUrls.copy(), True)
            )
            self._silenceThread.start()

    def checkForUpdates(self):
        """
        Execute updates checking and show dialog with the results.
        """
        setStatusText(_(u"Check for new versions..."))

        progressRunner = LongProcessRunner(
            self._threadFunc,
            self._application.mainWindow,
            dialogTitle=u"UpdateNotifier",
            dialogText=_(u"Check for new versions..."))

        progressRunner.run(self._updateUrls.copy(),
                           silenceMode=False)

    def createHTMLContent(self, updatedAppInfo):
        currentVersion = getCurrentVersion()
        currentVersionsDict = self._getCurrentVersionsDict()

        template = readTextFile(self._updateTemplatePath)

        templateData = {
            u'outwiker_current_version': currentVersion,
            u'updatedAppInfo': updatedAppInfo,
            u'currentVersionsDict': currentVersionsDict,
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
    def filterUpdatedApps(currentVersionsDict, latestAppInfoDict):
        """
        Return dictionary with the AppInfo for updated apps only.

        currentVersionsDict - dictionary with apps versions.
            Key - plugin name or special id,
            value - version number string.

        latestAppInfoDict - dictionary with AppInfo instances.
            Key - plugin name or special id,
            value - instance of the AppInfo.
        """
        updatedPlugins = {}

        for app_name, version_str in currentVersionsDict.iteritems():
            if app_name not in latestAppInfoDict:
                continue

            latestAppInfo = latestAppInfoDict[app_name]

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

    def _getUpdatedAppInfo(self, latestVersionsDict):
        '''
        Get AppInfo instances for updated apps (plugins and OutWiker) only.
        latestVersionsDict - dictionary. Key - plugin name or special id,
            value - instalnce of the AppInfo class.

        Return dictionary with the AppInfo instances for updated apps.
        '''
        currentVersionsDict = self._getCurrentVersionsDict()
        updatedAppInfo = self.filterUpdatedApps(currentVersionsDict,
                                                latestVersionsDict)
        return updatedAppInfo

    def _getCurrentVersionsDict(self):
        '''
        Return dictionary with apps versions. Key - plugin name or special id,
        value - string with version.
        '''
        currentVersion = getCurrentVersion()

        currentVersionsDict = {plugin.name: plugin.version
                               for plugin
                               in self._application.plugins}

        currentVersionsDict[self._OUTWIKER_STABLE_KEY] = unicode(currentVersion)
        currentVersionsDict[self._OUTWIKER_UNSTABLE_KEY] = unicode(currentVersion)

        return currentVersionsDict

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

        updatedAppInfo = self._getUpdatedAppInfo(event.appInfoDict)
        self._touchLastUpdateDate()

        if updatedAppInfo:
            self._showUpdates(updatedAppInfo)
        elif not event.silenceMode:
            MessageBox(_(u"Updates not found"), u"UpdateNotifier")

    def _touchLastUpdateDate(self):
        '''
        Save latest updates checking time.
        '''
        self._config.lastUpdate = datetime.datetime.today()

    def _threadFunc(self, updateUrls, silenceMode):
        """
        Thread function for silence updates checking
        """
        verList = VersionList(updateUrls)
        appInfoDict = verList.loadAppInfo()
        event = UpdateVersionsEvent(appInfoDict=appInfoDict,
                                    silenceMode=silenceMode)

        if self._application.mainWindow:
            wx.PostEvent(self._application.mainWindow, event)
