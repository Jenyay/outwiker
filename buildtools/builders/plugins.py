# -*- coding: UTF-8 -*-

import os
import shutil

from fabric.api import local, lcd

from .base import BuilderBase
from buildtools.defines import (PLUGINS_DIR,
                                PLUGINS_LIST,
                                PLUGIN_VERSIONS_FILENAME)
from buildtools.versions import readAppInfo


class BuilderPlugins(BuilderBase):
    """
    Create archives with plug-ins
    """
    def __init__(self, build_dir=PLUGINS_DIR, plugins_list=PLUGINS_LIST):
        super(BuilderPlugins, self).__init__(build_dir)
        self._all_plugins_fname = u'outwiker-plugins-all.zip'
        self._plugins_list = plugins_list


    def clear(self):
        super(BuilderPlugins, self).clear()
        self._remove(self._getSubpath(self._all_plugins_fname))


    def _build(self):
        for plugin in self._plugins_list:
            # Path to plugin.xml for current plugin
            xmlplugin_path = u'plugins/{plugin}/{plugin}/{pluginxml}'.format(
                plugin=plugin,
                pluginxml=PLUGIN_VERSIONS_FILENAME)
            try:
                appInfo = readAppInfo(xmlplugin_path)
            except EnvironmentError:
                appInfo = None

            # Future plug-in archive name
            if appInfo is None or appInfo.currentVersion is None:
                archive_name = plugin + u'.zip'
            else:
                version = unicode(appInfo.currentVersion)
                archive_name = u'{}-{}.zip'.format(plugin, version)

            # Subpath to current plug-in archive
            plugin_dir_path = self._getSubpath(plugin)

            # Path to future archive
            archive_path = self._getSubpath(plugin, archive_name)

            # Path to archive with all plug-ins
            full_archive_path = self._getSubpath(self._all_plugins_fname)
            self._remove(plugin_dir_path)
            self._remove(archive_path)

            os.mkdir(plugin_dir_path)
            if appInfo is not None:
                shutil.copy(xmlplugin_path, plugin_dir_path)

            with lcd("plugins/{}".format(plugin)):
                local("7z a -r -aoa -xr!*.pyc -xr!.ropeproject ../../{} ./*".format(archive_path))
                local("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -w../ ../../{} ./*".format(full_archive_path))
