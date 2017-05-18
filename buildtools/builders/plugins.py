# -*- coding: UTF-8 -*-

import os
import shutil
import urllib2

from fabric.api import local, lcd

from .base import BuilderBase
from buildtools.defines import (PLUGINS_DIR,
                                PLUGINS_LIST)
from buildtools.versions import (readAppInfo,
                                 getPluginVersionsPath,
                                 downloadAppInfo)


class BuilderPlugins(BuilderBase):
    """
    Create archives with plug-ins
    """
    def __init__(self,
                 updatedOnly=False,
                 build_dir=PLUGINS_DIR,
                 plugins_list=PLUGINS_LIST):
        super(BuilderPlugins, self).__init__(build_dir)
        self._all_plugins_fname = u'outwiker-plugins-all.zip'
        self._plugins_list = plugins_list
        self._updatedOnly = updatedOnly

    def get_plugins_pack_path(self):
        return self._getSubpath(self._all_plugins_fname)

    def clear(self):
        super(BuilderPlugins, self).clear()
        self._remove(self.get_plugins_pack_path())

    def _build(self):
        # Path to archive with all plug-ins
        full_archive_path = self.get_plugins_pack_path()

        for plugin in self._plugins_list:
            # Path to plugin.xml for current plugin
            xmlplugin_path = getPluginVersionsPath(plugin)

            localAppInfo = readAppInfo(xmlplugin_path)
            assert localAppInfo is not None
            assert localAppInfo.currentVersion is not None

            skip_plugin = False

            # Check for update
            if self._updatedOnly:
                url = localAppInfo.updatesUrl
                try:
                    siteappinfo = downloadAppInfo(url)
                    if localAppInfo.currentVersion == siteappinfo.currentVersion:
                        skip_plugin = True
                except (urllib2.URLError, urllib2.HTTPError):
                    pass

            # Archive a single plug-in
            if not skip_plugin:
                version = unicode(localAppInfo.currentVersion)
                archive_name = u'{}-{}.zip'.format(plugin, version)

                # Subpath to current plug-in archive
                plugin_dir_path = self._getSubpath(plugin)

                # Path to future archive
                archive_path = self._getSubpath(plugin, archive_name)
                os.mkdir(plugin_dir_path)
                shutil.copy(xmlplugin_path, plugin_dir_path)

                # Archive a single plug-in
                with lcd("plugins/{}".format(plugin)):
                    local('7z a -r -aoa -xr!*.pyc -xr!.ropeproject "{}" ./*'.format(archive_path))

            # Add a plug-in to full archive
            with lcd("plugins/{}".format(plugin)):
                local('7z a -r -aoa -xr!*.pyc -xr!.ropeproject -w../ "{}" ./*'.format(full_archive_path))

    def _getSubpath(self, *args):
        """
        Return subpath inside current build path (inside 'build' subpath)
        """
        return os.path.join(self.build_dir, *args)
