# -*- coding: UTF-8 -*-

import os
import shutil

from fabric.api import local, lcd

from ..base import BuilderBase
from buildtools.defines import LINUX_BUILD_DIR
from buildtools.utilites import getPython


class BuilderLinuxBinaryBase(BuilderBase):
    """
    Base class for all Linux binary builders.
    """
    def __init__(self, build_dir, create_archive):
        super(BuilderLinuxBinaryBase, self).__init__(build_dir)

        self._create_archive = create_archive
        # self._toRemove = [
        #     os.path.join(self.build_dir, u'tcl'),
        #     os.path.join(self.build_dir, u'tk'),
        #     os.path.join(self.build_dir, u'PyQt4.QtCore.so'),
        #     os.path.join(self.build_dir, u'PyQt4.QtGui.so'),
        #     os.path.join(self.build_dir, u'_tkinter.so'),
        # ]

    def _build_binary(self):
        """
        Build with cx_Freeze
        """
        with lcd(self.temp_sources_dir):
            local(u'{python} setup.py build --build-exe "{build_dir}"'.format(
                build_dir=self.build_dir,
                python=getPython()
            ))

        # map(self._remove, self._toRemove)

    def _create_plugins_dir(self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join(self.temp_sources_dir, u"plugins")

        # Create the plugins folder(it is not appened to the git repository)
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)


class BuilderLinuxBinary(BuilderLinuxBinaryBase):
    """
    Class for making simple Linux binary build
    """
    def __init__(self, build_dir=LINUX_BUILD_DIR, create_archive=True):
        super(BuilderLinuxBinary, self).__init__(build_dir, create_archive)
        self._archiveFullName = os.path.join(self.build_dir,
                                             'outwiker_linux_unstable_x64.7z')

    def _build(self):
        self._copy_necessary_files()
        self._create_plugins_dir()
        self._build_binary()

        if self._create_archive:
            self._build_archive()

    def clear(self):
        super(BuilderLinuxBinary, self).clear()
        self._remove(self._archiveFullName)

    def _build_archive(self):
        # Create archive without plugins
        with lcd(self.build_dir):
            local("7z a ../outwiker_linux_unstable_x64.7z ./* ./plugins -r -aoa")

    def _copy_necessary_files(self):
        shutil.copy(u'copyright.txt', self.facts.temp_dir)
        shutil.copy(u'LICENSE.txt', self.facts.temp_dir)
