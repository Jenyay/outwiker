# -*- coding: utf-8 -*-

import os
import shutil

from invoke import Context

from .base import BuilderBase
from .binarybuilders import PyInstallerBuilderLinuxSimple

from buildtools.defines import LINUX_BUILD_DIR


class BuilderLinuxBinary(BuilderBase):
    """
    Base class for all Linux binary builders.
    """
    def __init__(self, c: Context, create_archive=True, is_stable=False):
        super().__init__(c, LINUX_BUILD_DIR, is_stable)

        self._archiveFullName_7z = os.path.join(self.build_dir,
                                                'outwiker_linux_bin.7z')
        self._archiveFullName_zip = os.path.join(self.build_dir,
                                                 'outwiker_linux_bin.zip')

        self._create_archive = create_archive
        self._exe_path = os.path.join(self.build_dir, u'outwiker_exe')

    def _build_binary(self):
        """
        Build with PyInstaller
        """
        src_dir = self.temp_sources_dir
        dest_dir = self._exe_path
        temp_dir = self.facts.temp_dir

        builder = PyInstallerBuilderLinuxSimple(src_dir, dest_dir, temp_dir)
        builder.build()

    def _build(self):
        self._copy_necessary_files()
        self._create_plugins_dir()
        self._build_binary()

        if self._create_archive:
            self._build_archive()

    def clear(self):
        self._remove(self._exe_path)
        self._remove(self._archiveFullName_7z)
        self._remove(self._archiveFullName_zip)

    def _build_archive(self):
        # Create archive without plugins
        with self.context.cd(self._exe_path):
            self.context.run('7z a "{}" ./* ./plugins -r -aoa'.format(self._archiveFullName_7z))
            self.context.run('7z a "{}" ./* ./plugins -r -aoa'.format(self._archiveFullName_zip))

    def _copy_necessary_files(self):
        shutil.copy(u'copyright.txt', self.facts.temp_dir)
        shutil.copy(u'LICENSE.txt', self.facts.temp_dir)
