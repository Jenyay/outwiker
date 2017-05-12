# -*- coding: UTF-8 -*-

import os
import shutil

from fabric.api import local, lcd

from .base import BuilderBase
from buildtools.utilites import getPython
from buildtools.defines import (WINDOWS_BUILD_DIR,
                                PLUGINS_LIST,
                                OUTWIKER_VERSIONS_FILENAME,
                                WINDOWS_INSTALLER_FILENAME,
                                NEED_FOR_BUILD_DIR)


class BuilderWindows(BuilderBase):
    """
    Build for Windows
    """
    def __init__(self,
                 build_dir=WINDOWS_BUILD_DIR,
                 create_installer=True,
                 create_archives=True):
        super(BuilderWindows, self).__init__(build_dir)
        self._create_installer = create_installer
        self._create_archives = create_archives

        self._resultBaseName = u'outwiker_win_unstable'
        self._resultWithPluginsBaseName = u'outwiker_win_unstable_all_plugins'
        self._plugins_list = PLUGINS_LIST

        # Path to copy plugins
        self._dest_plugins_dir = os.path.join(self.build_dir, u'plugins')

    def clear(self):
        super(BuilderWindows, self).clear()
        toRemove = [
            os.path.join(self.facts.version_dir,
                         OUTWIKER_VERSIONS_FILENAME),
            os.path.join(self.facts.version_dir,
                         self._resultBaseName + u'.7z'),
            os.path.join(self.facts.version_dir,
                         self._resultBaseName + u'.exe'),
            os.path.join(self.facts.version_dir,
                         self._resultBaseName + u'.zip'),
            os.path.join(self.facts.version_dir,
                         self._resultWithPluginsBaseName + u'.7z'),
            os.path.join(self.facts.version_dir,
                         self._resultWithPluginsBaseName + u'.zip'),
            os.path.join(self.facts.version_dir,
                         WINDOWS_INSTALLER_FILENAME),
        ]
        map(self._remove, toRemove)

    def _build(self):
        shutil.copy(os.path.join(u'src', OUTWIKER_VERSIONS_FILENAME),
                    self.facts.version_dir)

        self._create_plugins_dir()
        self._build_binary()
        self._clear_dest_plugins_dir()

        # Create archives without plugins
        if self._create_archives:
            with lcd(self.build_dir):
                path_zip = os.path.abspath(
                    os.path.join(
                        self.facts.version_dir,
                        u'outwiker_win_unstable.zip')
                )

                path_7z = os.path.abspath(
                    os.path.join(
                        self.facts.version_dir,
                        u'outwiker_win_unstable.7z')
                )

                local(u'7z a "{}" .\* .\plugins -r -aoa'.format(path_zip))
                local(u'7z a "{}" .\* .\plugins -r -aoa'.format(path_7z))

        # Compile installer
        if self._create_installer:
            self._build_installer()

        # Copy plugins to build folder
        self._copy_plugins()

        # Archive versions with plugins
        if self._create_archives:
            with lcd(self.build_dir):
                path_zip = os.path.abspath(
                    os.path.join(
                        self.facts.version_dir,
                        u'outwiker_win_unstable_all_plugins.zip')
                )

                path_7z = os.path.abspath(
                    os.path.join(
                        self.facts.version_dir,
                        u'outwiker_win_unstable_all_plugins.7z')
                )

                local(u'7z a "{}" .\* .\plugins -r -aoa -xr!*.pyc -xr!.ropeproject'.format(path_zip))
                local(u'7z a "{}" .\* .\plugins -r -aoa -xr!*.pyc -xr!.ropeproject'.format(path_7z))

    def _build_binary(self):
        """
        Build with cx_Freeze
        """
        with lcd("src"):
            local(u'{python} setup.py build --build-exe "{builddir}"'.format(
                python=getPython(),
                builddir=self.build_dir)
            )

    def _create_plugins_dir(self):
        """
        Create the plugins folder(it is not appened to the git repository)
        """
        pluginsdir = os.path.join("src", "plugins")
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)

    def _clear_dest_plugins_dir(self):
        self._remove(self._dest_plugins_dir)
        os.mkdir(self._dest_plugins_dir)

    def _build_installer(self):
        fnames = [
            os.path.join(NEED_FOR_BUILD_DIR, u'windows', u'outwiker_setup.iss'),
            u'LICENSE.txt',
        ]

        map(lambda fname: shutil.copy(fname, self.facts.version_dir), fnames)

        with lcd(self.facts.version_dir):
            local("iscc outwiker_setup.iss")

        for fname in fnames:
            os.remove(os.path.join(self.facts.version_dir,
                                   os.path.basename(fname)))

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
