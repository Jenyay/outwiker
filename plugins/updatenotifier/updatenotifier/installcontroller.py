# -*- coding: UTF-8 -*-

import datetime
import logging
import threading
import os.path
import json

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
    Controller for updates checking and show information.
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

    def run(self):
        """
        Open plugins installer dialog
        """
        # read data/plugins.json
        all_plugins = json.loads(readTextFile(self._pluginsRepoPath))

        # get installed plugins
        installed_plugins = self._application.plugins + self._application.plugins.disabledPlugins

        # show dialog
        self._showPluginsInstaller(all_plugins, installed_plugins)

    def createInstallerHTMLContent(self, all_plugins, installed_plugins):
        """
        Prepare plugins view based on install.html template
        :param plugins:
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
            updateDialog.setContent(HTMLContent, None)
            updateDialog.ShowModal()

    def install_plugin(self, id):
        """
        Install plugin by id.

        :return: True if plugin was updated, otherwise False
        """

        plugin_info = self._installerPlugins.get(id, None)
        if plugin_info:
            xml_url = plugin_info["url"]

            appInfoDict = VersionList().getAppInfoFromUrl(xml_url)
            # get link to latest version
            plugin_downloads = appInfoDict[id].versionsList[0].downloads
            if 'all' in plugin_downloads:
                url = plugin_downloads.get('all')
            elif getOS().name in plugin_downloads:
                url = plugin_downloads.get(getOS().name)
            else:
                MessageBox(_(u"The download link was not found in plugin description. Please update plugin manually"),
                           u"UpdateNotifier")
                return False

            # 0 - папка рядом с запускаемым файлом, затем идут другие папки, если они есть
            pluginPath = os.path.join(getPluginsDirList()[-1], id)

            logger.info('update_plugin: {url} {path}'.format(url=url, path=pluginPath))

            #rez = UpdatePlugin().update(url, pluginPath)

            if rez:
                # TODO: надо как то убрать плагин из диалога, но непонятно как получить к нему доступ при обработке евента
                self._application.plugins.load(getPluginsDirList()[-1])
                MessageBox(_(u"Plugin was successfully updated."), u"UpdateNotifier")
            else:
                MessageBox(_(u"Plugin was NOT updated. Please update plugin manually"), u"UpdateNotifier")
            return rez
