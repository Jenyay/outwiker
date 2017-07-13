# -*- coding: UTF-8 -*-

import os
import shutil
from string import Template

from fabric.api import local, lcd

from .base import BuilderBase
from .binarybuilders import PyInstallerBuilderWindows
from buildtools.defines import (WINDOWS_BUILD_DIR,
                                PLUGINS_LIST,
                                OUTWIKER_VERSIONS_FILENAME,
                                WINDOWS_INSTALLER_FILENAME,
                                NEED_FOR_BUILD_DIR,
                                WINDOWS_EXECUTABLE_DIR)

from outwiker.utilites.textfile import readTextFile, writeTextFile


class BuilderWindows(BuilderBase):
    """
    Build for Windows
    """
    def __init__(self,
                 is_stable=False,
                 create_archives=True,
                 create_installer=True):
        super(BuilderWindows, self).__init__(WINDOWS_BUILD_DIR, is_stable)
        self._create_installer = create_installer
        self._create_archives = create_archives

        self._resultBaseName = (
            u'outwiker_{version}_win'.format(
                version=self.facts.version_items[0])
            if self.is_stable
            else u'outwiker_win_unstable'
        )

        self._resultWithPluginsBaseName = self._resultBaseName + u'_all_plugins'
        self._plugins_list = PLUGINS_LIST

        self._executable_dir = os.path.join(self.facts.temp_dir,
                                            WINDOWS_EXECUTABLE_DIR)

        # Path to copy plugins
        self._dest_plugins_dir = os.path.join(self._executable_dir, u'plugins')

    def clear(self):
        super(BuilderWindows, self).clear()
        toRemove = [
            os.path.join(self.facts.version_dir,
                         OUTWIKER_VERSIONS_FILENAME),
            os.path.join(self.build_dir,
                         self._resultBaseName + u'.7z'),
            os.path.join(self.build_dir,
                         self._resultBaseName + u'.exe'),
            os.path.join(self.build_dir,
                         self._resultBaseName + u'.zip'),
            os.path.join(self.build_dir,
                         self._resultWithPluginsBaseName + u'.7z'),
            os.path.join(self.build_dir,
                         self._resultWithPluginsBaseName + u'.zip'),
            os.path.join(self.build_dir,
                         WINDOWS_INSTALLER_FILENAME),
        ]
        map(self._remove, toRemove)

    def _build(self):
        self._copy_necessary_files()
        self._create_plugins_dir()
        self._create_binary()
        self._clear_dest_plugins_dir()
        self._create_archives_without_plugins()
        self._build_installer()
        self._copy_plugins()
        self._create_archives_with_plugins()
        self._move_executable_dir()

    def _create_binary(self):
        """
        Build with PyInstaller
        """
        src_dir = self.temp_sources_dir
        dest_dir = self._executable_dir
        temp_dir = self.facts.temp_dir

        builder = PyInstallerBuilderWindows(src_dir, dest_dir, temp_dir)
        builder.build()

    def _create_plugins_dir(self):
        """
        Create the plugins folder(it is not appened to the git repository)
        """
        pluginsdir = os.path.join(self.temp_sources_dir, u"plugins")
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)

    def _clear_dest_plugins_dir(self):
        self._remove(self._dest_plugins_dir)
        os.mkdir(self._dest_plugins_dir)

    def _build_installer(self):
        if not self._create_installer:
            return

        if self.is_stable:
            installerName = u'outwiker_{}_win'.format(self.facts.version_items[0])
        else:
            installerName = u'outwiker_win_unstable'.format(self.facts.version)

        installer_path = os.path.join(self.facts.temp_dir, installerName)

        installer_template = readTextFile(os.path.join(NEED_FOR_BUILD_DIR, u'windows', u'outwiker_setup.iss.tpl'))

        installer_text = Template(installer_template).safe_substitute(
            version=self.facts.version,
            resultname=installerName
        )

        installer_script_path = os.path.join(self.facts.temp_dir,
                                             u'outwiker_setup.iss')

        writeTextFile(installer_script_path, installer_text)

        with lcd(self.facts.temp_dir):
            local("iscc outwiker_setup.iss")

        shutil.move(installer_path + u'.exe', self.build_dir)

    def _copy_plugins(self):
        """
        Copy plugins to build folder
        """
        src_pluginsdir = u"plugins"
        for plugin in self._plugins_list:
            shutil.copytree(
                os.path.join(src_pluginsdir, plugin, plugin),
                os.path.join(self._dest_plugins_dir, plugin),
            )

    def _copy_necessary_files(self):
        shutil.copy(u'copyright.txt', self.facts.temp_dir)
        shutil.copy(u'LICENSE.txt', self.facts.temp_dir)

    def _create_archives_without_plugins(self):
        if not self._create_archives:
            return

        with lcd(self._executable_dir):
            path_zip = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultBaseName + u'.zip')
            )

            path_7z = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultBaseName + u'.7z')
            )

            local(u'7z a "{}" .\* .\plugins -r -aoa'.format(path_zip))
            local(u'7z a "{}" .\* .\plugins -r -aoa'.format(path_7z))

    def _create_archives_with_plugins(self):
        if not self._create_archives:
            return

        with lcd(self._executable_dir):
            path_zip = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultWithPluginsBaseName + u'.zip')
            )

            path_7z = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultWithPluginsBaseName + u'.7z')
            )

            local(u'7z a "{}" .\* .\plugins -r -aoa -xr!*.pyc -xr!.ropeproject'.format(path_zip))
            local(u'7z a "{}" .\* .\plugins -r -aoa -xr!*.pyc -xr!.ropeproject'.format(path_7z))

    def _move_executable_dir(self):
        shutil.move(self._executable_dir, self.build_dir)
