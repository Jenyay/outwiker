# -*- coding: UTF-8 -*-

import datetime
import logging
import threading
import os.path
import json
import shutil
import html

import wx

import outwiker.core
from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version
from outwiker.core.system import getPluginsDirList
import outwiker.core.packageversion as pv
from outwiker.utilites.textfile import readTextFile

from .updatedialog import UpdateDialog
from .updatesconfig import UpdatesConfig
from .versionlist import VersionList
from .i18n import get_
from .contentgenerator import ContentGenerator
from .updateplugin import UpdatePlugin

# The event occurs after finish checking latest versions.
# The parameters:
#     appInfoDict - dictionary. Key - plugin name or special id,
#                               value - AppInfo instance.
#     silenceMode - True if the thread was run in the silence mode.
UpdateVersionsEvent, EVT_UPDATE_VERSIONS = wx.lib.newevent.NewEvent()

logger = logging.getLogger('updatenotifier')
vl = VersionList()

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
        join = os.path.join

        self._application = application
        self._config = UpdatesConfig(self._application.config)
        self._dataPath = join(pluginPath, u'data')
        self._updateTemplatePath = join(self._dataPath, u'update.html')

        # Special string id for stable and unstable OutWiker URL
        self._OUTWIKER_STABLE_KEY = u'OUTWIKER_STABLE'
        self._OUTWIKER_UNSTABLE_KEY = u'OUTWIKER_UNSTABLE'

        # Dictionary. Key - plugin name or special string id,
        # Value - URL to XML file with versions information.
        self._updateUrls = {}
        self._updateUrls[self._OUTWIKER_STABLE_KEY] = u'http://jenyay.net/uploads/Soft/Outwiker/versions.xml'
        self._updateUrls[self._OUTWIKER_UNSTABLE_KEY] = u'http://jenyay.net/uploads/Outwiker/Unstable/versions.xml'

        # update dialog instance
        self._dialog = None

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


    def createHTMLContent(self, appInfoDict, updatedAppInfo, installerInfoDict):
        currentVersion = getCurrentVersion()
        currentVersionsDict = self._getCurrentVersionsDict()

        appInfoDict = self.filterUpdatedApps(currentVersionsDict, appInfoDict)
        updateAppInfo = self.filterUpdatedApps(currentVersionsDict, updatedAppInfo)

        installedAppInfo = {x: y for x, y in updatedAppInfo.items() if x not in updateAppInfo}

        template = readTextFile(self._updateTemplatePath)

        templateData = {
            u'outwiker_current_version': currentVersion,
            u'outwikerAppInfo': appInfoDict,
            u'updatedAppInfo': updateAppInfo,
            u'installedAppInfo': installedAppInfo,
            u'otherAppInfo': installerInfoDict,
            u'currentVersionsDict': currentVersionsDict,
            u'str_outwiker_current_version': _(u'Installed OutWiker version'),
            u'str_outwiker_latest_stable_version': _(u'Latest stable OutWiker version'),
            u'str_outwiker_latest_unstable_version': _(u'Latest unstable OutWiker version'),
            u'str_version_history': _(u'Version history'),
            u'str_more_info': _(u'More info'),
            u'str_update': _(u'Update'),
            u'str_install': _(u'Install'),
            u'str_uninstall': _(u'Uninstall'),
            u'data_path': self._dataPath,
            u'escape': html.escape,
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

        for app_name, version_str in currentVersionsDict.items():
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


    def _getPluginsUpdateUrls(self):
        '''
        plugins - instance of the PluginsLoader
        Return dict which key is plugin name, value is updatesUrl
        '''
        getInfo = self._application.plugins.getInfo

        result = {}
        plugin_names = self._getInstalledPlugins()
        for name in plugin_names:

            try:
                appInfo = getInfo(name, [_(u'__updateLang'), u'en'])
            except IOError:
                logger.warning(u"Can't read {} Info".format(name))
                continue
            except ValueError:
                logger.warning(u"Invalid format {}".format(name))
                continue

            result[name] = appInfo.updatesUrl

        return result

    def _getUpdatedAppInfo(self, latestVersionsDict):
        '''
        Get AppInfo instances for updated apps (plugins and OutWiker) only.

        latestVersionsDict - dictionary. Key - plugin name or special id,
            value - instance of the AppInfo class.

        Return dictionary with the AppInfo instances for updated apps.
        '''
        currentVersionsDict = self._getCurrentVersionsDict()
        updatedAppInfo = self.filterUpdatedApps(currentVersionsDict, latestVersionsDict)
        return updatedAppInfo


    def _getCurrentVersionsDict(self):
        '''
        Return dictionary with apps versions. Key - plugin name or special id,
        value - string with version.
        '''
        currentVersion = getCurrentVersion()

        currentVersionsDict = {plugin: self.get_plugin(plugin).version
                               for plugin
                               in self._getInstalledPlugins()}

        currentVersionsDict[self._OUTWIKER_STABLE_KEY] = str(currentVersion)
        currentVersionsDict[self._OUTWIKER_UNSTABLE_KEY] = str(currentVersion)

        return currentVersionsDict


    def _showUpdates(self, appInfoDict, updatedAppInfo, installerInfoDict):
        '''
        Show dialog with update information.
        '''
        setStatusText(u"")

        HTMLContent = self.createHTMLContent(appInfoDict, updatedAppInfo, installerInfoDict)

        with UpdateDialog(self._application.mainWindow) as updateDialog:
            self._dialog = updateDialog
            updateDialog.setContent(HTMLContent, self._dataPath)
            updateDialog.ShowModal()


    def _onVersionUpdate(self, event):
        '''
        Event handler for EVT_UPDATE_VERSIONS.
        '''
        setStatusText(u"")
        self._touchLastUpdateDate()

        updatedAppInfo = self._getUpdatedAppInfo(event.plugInfoDict)

        if event.silenceMode:
            if updatedAppInfo:
                self._showUpdates(event.appInfoDict, event.plugInfoDict, event.installerInfoDict)
        else:
            self._showUpdates(event.appInfoDict, event.plugInfoDict, event.installerInfoDict)


    def _threadFunc(self, updateUrls, silenceMode):
        """
        Thread function for silence updates checking.
        Get info data from the  updates Urls

        :param:
            updateUrls - dict which key is plugin name or other ID,
                value is update url
            silenceMode - True or False

        :raise:
            EVT_UPDATE_VERSIONS event
        """

        # get
        appInfoDict = vl.loadAppInfo(updateUrls)

        # get update URLs from installed plugins
        plugInfoDict = vl.loadAppInfo(self._getPluginsUpdateUrls())

        # get update URLs from plugins.json and remove installed.
        installerInfoDict = {x: y for x, y in self._getUrlsForInstaller().items()
                             if x not in self._getInstalledPlugins()}
        installerInfoDict = vl.loadAppInfo(installerInfoDict)


        event = UpdateVersionsEvent(appInfoDict=appInfoDict,
                                    plugInfoDict=plugInfoDict,
                                    installerInfoDict=installerInfoDict,
                                    silenceMode=silenceMode)

        if self._application.mainWindow:
            wx.PostEvent(self._application.mainWindow, event)

    def _getUrlsForInstaller(self):

        self._pluginsRepoPath = os.path.join(self._dataPath, u'plugins.json')

        # read data/plugins.json
        self._installerPlugins = json.loads(readTextFile(self._pluginsRepoPath))

        updateUrls = {x['name']:x['url'] for x in self._installerPlugins.values()}
        return updateUrls


    def _touchLastUpdateDate(self):
        '''
        Save latest updates checking time.
        '''
        self._config.lastUpdate = datetime.datetime.today()


    def update_plugin(self, name):
        """
        Update plugin to latest version by name.
        :return: True if plugin was installed, otherwise False
        """
        appInfoDict = vl.loadAppInfo(self._getPluginsUpdateUrls())

        # get link to latest version
        appInfo = appInfoDict.get(name)
        if appInfo:
            url = vl.getDownlodUrl(appInfo)
            if not url:
                MessageBox(_(u"The download link was not found in plugin description. Please update plugin manually"),
                           u"UpdateNotifier")
                return False
        else:
            MessageBox(_(u"Plugin was NOT updated. Please update plugin manually"),
                       u"UpdateNotifier")
            return False

        plugin = self.get_plugin(name)

        logger.info('update_plugin: {url} {path}'.format(url=url, path=plugin.pluginPath))

        rez = UpdatePlugin().update(url, plugin.pluginPath)

        if rez:
            self._application.plugins.reload(name)
            self._dialog.EndModal(wx.ID_OK)
            self.checkForUpdates()
        else:
            MessageBox(_(u"Plugin was NOT updated. Please update plugin manually"), u"UpdateNotifier")
        return rez


    def _getInstalledPlugins(self):
        """
        Retrieve list with names of all installed plugins
        """
        #TODO: It seems the method should be moved to PluginsLoader

        enabled_plugins = [p.name for p in self._application.plugins]
        disabled_plugins = list(self._application.plugins.disabledPlugins)

        return enabled_plugins + disabled_plugins


    def _updateDialog(self):
        """
        Update content on the current opened update dialog.
        """
        if self._dialog and self._dialog.IsModal():
            self._dialog.EndModal(wx.ID_OK)
            self.checkForUpdates()


    def install_plugin(self, name):
        """
        Install plugin by name.

        :return: True if plugin was installed, otherwise False
        """
        getAppInfo = vl.getAppInfoFromUrl
        getDownlodUrl = vl.getDownlodUrl

        plugin_info = self._installerPlugins.get(name, None)
        if plugin_info:

            appInfo = getAppInfo( plugin_info["url"])
            if not appInfo or not appInfo.versionsList:
                MessageBox(_(u"The plugin description can't be downloaded. Please install plugin manually"),
                           u"UpdateNotifier")
                return False

            api_required_version = appInfo.requirements.api_version
            if pv.checkVersionAny(outwiker.core.__version__, api_required_version) != 0:
                MessageBox(_(u"The plugin required last version of Outwiker. Please update application"),
                           u"UpdateNotifier")
                return False

            # get link to latest version
            url = getDownlodUrl(appInfo)
            if not url:
                MessageBox(_(u"The download link was not found in plugin description. Please install plugin manually"),
                           u"UpdateNotifier")
                return False

            # 0 - папка рядом с запускаемым файлом, затем идут другие папки, если они есть
            pluginPath = os.path.join(getPluginsDirList()[-1], name.lower())

            logger.info('install_plugin: {url} {path}'.format(url=url, path=pluginPath))

            rez = UpdatePlugin().update(url, pluginPath)

            if rez:
                self._application.plugins.load(getPluginsDirList())
                self._updateDialog()
            else:
                MessageBox(_(u"Plugin was NOT Installed. Please update plugin manually"), u"UpdateNotifier")
            return rez


    def get_plugin(self, name):
        """
        Retrieve Plugin object from app.plugins

        :param name:
            plugin name
        :return:
            The object with Plugin interface
        """

        # TODO: Seems the method should be add to PluginsLoader class

        for p in self._application.plugins:
            if p.name == name:
                return p

        if name in self._application.plugins.disabledPlugins:
            return self._application.plugins.disabledPlugins[name]

        return None


    def uninstall_plugin(self, name):
        """
        remove plugin from application._plugins and delete plugin folder from disk
        :param name:
        :return:
            True if plugin was uninstalled successful, otherwise False
        """
        rez = True

        plugin_path = self.get_plugin(name).pluginPath

        logger.info('uninstall_plugin: {name} {path}'.format(name=name, path=plugin_path))

        # remove plugin from applications._plugins
        rez = rez and self._application.plugins.remove(name)

        logger.info('uninstall_plugin: remove plugin {}'.format(rez))

        # remove plugin folder or remove symbolic link to it.
        if rez and os.path.exists(plugin_path):
            logger.info('uninstall_plugin: remove folder {}'.format(plugin_path))
            if os.path.islink(plugin_path):
                os.unlink(plugin_path)
            else:
                shutil.rmtree(plugin_path)

        self._updateDialog()
        return rez