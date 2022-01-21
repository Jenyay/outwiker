# -*- coding: utf-8 -*-

import os
import shutil
from string import Template

from invoke import Context

from .base import BuilderBase
from .binarybuilders import CxFreezeBuilderWindows
from buildtools.defines import (WINDOWS_BUILD_DIR,
                                PLUGINS_LIST,
                                NEED_FOR_BUILD_DIR,
                                WINDOWS_EXECUTABLE_DIR)
from buildtools.utilites import print_info

from outwiker.utilites.textfile import readTextFile, writeTextFile


class BuilderWindows(BuilderBase):
    """
    Build for Windows
    """

    def __init__(self,
                 c: Context,
                 is_stable: bool = False,
                 create_archives: bool = True,
                 create_installer: bool = True):
        super().__init__(c, WINDOWS_BUILD_DIR, is_stable)
        self._create_installer = create_installer
        self._create_archives = create_archives

        self._resultBaseName = (
            'outwiker_{version}_win'.format(
                version=self.facts.version_items[0])
            if self.is_stable
            else 'outwiker_win_unstable'
        )

        self._resultWithPluginsBaseName = self._resultBaseName + '_all_plugins'
        self._plugins_list = PLUGINS_LIST

        self._executable_dir = os.path.join(self.facts.temp_dir,
                                            WINDOWS_EXECUTABLE_DIR)

        # Path to copy plugins
        self._dest_plugins_dir = os.path.join(self._executable_dir, 'plugins')

    def clear(self):
        toRemove = [
            os.path.join(self.build_dir, WINDOWS_EXECUTABLE_DIR),
            os.path.join(self.build_dir,
                         self._resultBaseName + '.7z'),
            os.path.join(self.build_dir,
                         self._resultBaseName + '.exe'),
            os.path.join(self.build_dir,
                         self._resultBaseName + '.zip'),
            os.path.join(self.build_dir,
                         self._resultWithPluginsBaseName + '.7z'),
            os.path.join(self.build_dir,
                         self._resultWithPluginsBaseName + '.zip'),
        ]
        for fname in toRemove:
            self._remove(fname)

    def _build(self):
        print_info('Is stable: {}'.format(self.is_stable))
        print_info('Create installer: {}'.format(self._create_installer))
        print_info('Create archives: {}'.format(self._create_archives))

        self._copy_necessary_files()
        self._create_plugins_dir()
        self._create_binary()
        self._clear_dest_plugins_dir()
        self._create_archives_without_plugins()
        self._copy_plugins()
        self._build_installer()
        self._create_archives_with_plugins()
        self._move_executable_dir()

    def _create_binary(self):
        """
        Build with PyInstaller
        """
        print_info('Create binary files...')
        src_dir = self.temp_sources_dir
        dest_dir = self._executable_dir
        temp_dir = self.facts.temp_dir

        builder = CxFreezeBuilderWindows(self.context, src_dir, dest_dir, temp_dir)
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

        print_info('Create installer...')
        if self.is_stable:
            installerName = 'outwiker_{}_win'.format(
                self.facts.version_items[0])
        else:
            installerName = 'outwiker_win_unstable'

        installer_path = os.path.join(self.facts.temp_dir, installerName)

        installer_template = readTextFile(os.path.join(
            NEED_FOR_BUILD_DIR, 'windows', 'outwiker_setup.iss.tpl'))

        installer_text = Template(installer_template).safe_substitute(
            version=self.facts.version,
            resultname=installerName
        )

        installer_script_path = os.path.join(self.facts.temp_dir,
                                             'outwiker_setup.iss')

        writeTextFile(installer_script_path, installer_text)

        with self.context.cd(self.facts.temp_dir):
            self.context.run("iscc outwiker_setup.iss")

        shutil.move(installer_path + '.exe', self.build_dir)

    def _copy_plugins(self):
        """
        Copy plugins to build folder
        """
        print_info('Copy plugins...')
        src_pluginsdir = 'plugins'
        for plugin in self._plugins_list:
            shutil.copytree(
                os.path.join(src_pluginsdir, plugin, plugin),
                os.path.join(self._dest_plugins_dir, plugin),
            )

    def _copy_necessary_files(self):
        print_info('Copy necessary files...')
        shutil.copy('copyright.txt', self.facts.temp_dir)
        shutil.copy('LICENSE.txt', self.facts.temp_dir)

    def _create_archives_without_plugins(self):
        if not self._create_archives:
            return

        print_info('Create archives without plugins...')
        with self.context.cd(self._executable_dir):
            path_zip = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultBaseName + '.zip')
            )

            path_7z = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultBaseName + '.7z')
            )

            self.context.run(r'7z a "{}" .\* .\plugins -r -aoa'.format(path_zip))
            self.context.run(r'7z a "{}" .\* .\plugins -r -aoa'.format(path_7z))

    def _create_archives_with_plugins(self):
        if not self._create_archives:
            return

        print_info('Create archives with plugins...')
        with self.context.cd(self._executable_dir):
            path_zip = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultWithPluginsBaseName + '.zip')
            )

            path_7z = os.path.abspath(
                os.path.join(
                    self.build_dir,
                    self._resultWithPluginsBaseName + '.7z')
            )

            self.context.run(
                r'7z a "{}" .\* .\plugins -r -aoa -xr!__pycache__ -xr!.ropeproject'.format(path_zip))
            self.context.run(
                r'7z a "{}" .\* .\plugins -r -aoa -xr!__pycache__ -xr!.ropeproject'.format(path_7z))

    def _move_executable_dir(self):
        print_info('Move result directory to {}...'.format(self.build_dir))
        shutil.move(self._executable_dir, self.build_dir)
