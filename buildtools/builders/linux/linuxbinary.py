# -*- coding: UTF-8 -*-

import os
import shutil

from fabric.api import local, lcd

from ..base import BuilderBase
from buildtools.defines import LINUX_BUILD_DIR


class BuilderLinuxBinaryBase(BuilderBase):
    """
    Base class for all Linux binary builders.
    """
    def __init__(self, build_dir, create_archive):
        super(BuilderLinuxBinaryBase, self).__init__(build_dir)

        self._create_archive = create_archive
        self._toRemove = [
            self._getSubpath(u'tcl'),
            self._getSubpath(u'tk'),
            self._getSubpath(u'PyQt4.QtCore.so'),
            self._getSubpath(u'PyQt4.QtGui.so'),
            self._getSubpath(u'_tkinter.so'),
        ]

    def _build_binary(self):
        """
        Build with cx_Freeze
        """
        with lcd("src"):
            local("python setup.py build --build-exe ../{}".format(self._build_dir))

        map(self._remove, self._toRemove)

    def _create_plugins_dir(self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join("src", "plugins")

        # Create the plugins folder(it is not appened to the git repository)
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)


class BuilderLinuxBinary(BuilderLinuxBinaryBase):
    """
    Class for making simple Linux binary build
    """
    def __init__(self, build_dir=LINUX_BUILD_DIR, create_archive=True):
        super(BuilderLinuxBinary, self).__init__(build_dir, create_archive)
        self._archiveFullName = os.path.join(self._root_build_dir,
                                             'outwiker_linux_unstable_x64.7z')

    def _build(self):
        self._create_plugins_dir()
        self._build_binary()

        if self._create_archive:
            self._build_archive()

    def clear(self):
        super(BuilderLinuxBinary, self).clear()
        self._remove(self._archiveFullName)

    def _build_archive(self):
        # Create archive without plugins
        with lcd(self._build_dir):
            local("7z a ../outwiker_linux_unstable_x64.7z ./* ./plugins -r -aoa")
