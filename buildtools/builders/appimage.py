# -*- coding: utf-8 -*-

import os
import shutil

from fabric.api import local, lcd

from .base import BuilderBase
from .binarybuilders import PyInstallerBuilderLinuxSimple

from buildtools.defines import APPIMAGE_BUILD_DIR, NEED_FOR_BUILD_DIR


class BuilderAppImage(BuilderBase):
    '''
    Class to create AppImage package for Linux.
    '''
    def __init__(self, is_stable=False):
        super(BuilderAppImage, self).__init__(APPIMAGE_BUILD_DIR, is_stable)
        self._appdir_name = u'Outwiker.AppDir'
        self._appimage_result_name = u'Outwiker-x86_64.AppImage'

        self._temp_dir = os.path.join(self.facts.temp_dir, u'AppImage')
        self._app_dir = os.path.join(self._temp_dir, self._appdir_name)
        self._opt_dir = os.path.join(self._app_dir, u'opt')
        self._binary_dir = os.path.join(self._opt_dir, u'outwiker')
        self._result_full_path = os.path.join(self.build_dir,
                                              self._appimage_result_name)

    def clear(self):
        self._remove(self._result_full_path)

    def _build(self):
        self._create_plugins_dir()
        self._copy_appimage_files()
        self._createdir_tree()
        self._create_binaries()
        self._download_appimagetool()
        self._build_appimage()
        self._copy_result()

    def _copy_appimage_files(self):
        src = os.path.join(NEED_FOR_BUILD_DIR, u'AppImage', u'Outwiker.AppDir')
        dest = self._app_dir
        shutil.copytree(src, dest)

    def _createdir_tree(self):
        os.makedirs(self._opt_dir)

    def _create_binaries(self):
        dest_dir = self._binary_dir
        src_dir = self.temp_sources_dir
        temp_dir = self.facts.temp_dir

        linuxBuilder = PyInstallerBuilderLinuxSimple(src_dir, dest_dir, temp_dir)
        linuxBuilder.build()

    def _download_appimagetool(self):
        with lcd(self._temp_dir):
            local(u'wget "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"')
            local(u'chmod a+x appimagetool-x86_64.AppImage')

    def _build_appimage(self):
        with lcd(self._temp_dir):
            local(u'export ARCH=x86_64 && ./appimagetool-x86_64.AppImage {}'.format(self._appdir_name))

    def _copy_result(self):
        src = os.path.join(self._temp_dir, self._appimage_result_name)
        dest = self.build_dir
        shutil.copy(src, dest)
