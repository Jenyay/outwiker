# -*- coding: UTF-8 -*-

import datetime
import logging
import threading
import os.path
import json
import shutil

import wx

from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version
from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile
from outwiker.core.system import getOS, getPluginsDirList

from .updatedialog import UpdateDialog
from .updatesconfig import UpdatesConfig
from .versionlist import VersionList
from .i18n import get_
from .contentgenerator import ContentGenerator
from .updateplugin import UpdatePlugin

logger = logging.getLogger('updatenotifier')

class InstallController(object):
    """
    provide interfaces to install/remove plugins
    responsible for plugin's installer dialog
    """

    def __init__(self, application):
        '''
        application - instance of the ApplicationParams class.
        '''
        global _
        _ = get_()
        join = os.path.join

        self._application = application
        self._config = UpdatesConfig(self._application.config)
        self._dataPath = join(os.path.dirname(__file__), u'data')
        self._installTemplatePath = join(self._dataPath, u'install.html')
        self._pluginsRepoPath = join(self._dataPath, u'plugins.json')
        self._installerPlugins = {}
        self._dialog = None

        ##logger.info('install_plugin: {}'.format(self._dataPath.replace(r'\\', r"/")))

    def run(self):
        """
        Open plugins installer dialog
        """
        # read data/plugins.json
        self._installerPlugins = json.loads(readTextFile(self._pluginsRepoPath))

        # get installed plugins
        # fixme: add to PluginLoader method loaded plugins
        enabled_plugins = [p.name for p in self._application.plugins]
        installed_plugins = enabled_plugins + list(self._application.plugins.disabledPlugins)

        # show dialog
        self._showPluginsInstaller(self._installerPlugins, installed_plugins)

    def createInstallerHTMLContent(self, all_plugins, installed_plugins):
        """
        Prepare plugins view based on install.html template
        :param all_plugins:
            Serialised dict from plugins.json
        :return
            string for html render
        """
        template = readTextFile(self._installTemplatePath)

        templateData = {
            u'plugins': all_plugins,
            u'installed_plugins': installed_plugins,
            u'str_more_info': _(u'More info'),
            u'str_install': _(u'Install'),
            u'str_uninstall': _(u'Uninstall'),
            u'str_wait': _(u'Please wait'),
            u'data_path': self._dataPath,
        }

        contentGenerator = ContentGenerator(template)
        HTMLContent = contentGenerator.render(templateData)
        return HTMLContent

    def _showPluginsInstaller(self, all_plugins, installed_plugins):
        '''
        Show dialog with installed plugins information.
        '''
        setStatusText(u"")

        HTMLContent = self.createInstallerHTMLContent(all_plugins, installed_plugins)

        with UpdateDialog(self._application.mainWindow) as updateDialog:
            self._dialog = updateDialog
            updateDialog.setContent(HTMLContent, self._dataPath)
            updateDialog.ShowModal()

    def install_plugin(self, name):
        """
        Install plugin by name.

        :return: True if plugin was installed, otherwise False
        """
        getAppInfo = VersionList().getAppInfoFromUrl
        getDownlodUrl = VersionList().getDownlodUrl

        plugin_info = self._installerPlugins.get(name, None)
        if plugin_info:

            appInfo = getAppInfo( plugin_info["url"])
            if not appInfo or not appInfo.versionsList:
                MessageBox(_(u"The plugin description can't be downloaded. Please install plugin manually"),
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
                self._application.plugins.load([getPluginsDirList()[-1]])
                self._updateDialog()
            else:
                MessageBox(_(u"Plugin was NOT Installed. Please update plugin manually"), u"UpdateNotifier")
            return rez

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

        # remove plugin folder
        if rez and os.path.exists(plugin_path):
            logger.info('uninstall_plugin: remove folder {}'.format(plugin_path))
            shutil.rmtree(plugin_path)

        self._updateDialog()
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

    def _updateDialog(self):
        """
        Update content on the current opened installer dialog.
        """
        if self._dialog and self._dialog.IsModal():
            # get installed plugins
            # fixme: add to PluginLoader method loaded plugins
            enabled_plugins = [p.name for p in self._application.plugins]
            installed_plugins = enabled_plugins + list(self._application.plugins.disabledPlugins)

            HTMLContent = self.createInstallerHTMLContent(self._installerPlugins, installed_plugins)

            # Setup updated data to dialog render
            self._dialog.setContent(HTMLContent, self._dataPath)