#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cx_Freeze import setup, Executable
import os
from abc import ABCMeta, abstractmethod

from outwiker.core.defines import WX_VERSION
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile

import wxversion
wxversion.select(WX_VERSION)


class BaseBuilder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _getExecutable(self):
        pass

    def _getExtraIncludeFiles(self):
        return []

    def _getPathIncludes(self):
        return []

    def _getExtraBuildExeOptions(self):
        return {}

    def _getExcludes(self):
        return ['numpy',
                'scipy',
                'tkinter',
                'PyQt4',
                'tcl',
                'tk',
                'unittest',
                'setuptools',
                'distutils',
                'email',
                ]

    def _getPackages(self):
        # Добавляем 'outwiker.pages.wiki.wikipanel',
        # т.к. этот модуль используется только в старых версиях плагинов
        return ['urllib',
                'urllib2',
                'outwiker.pages.wiki.wikipanel',
                'outwiker.gui.htmlrenderfactory',
                'outwiker.gui.controls.popupbutton',
                'PIL.Image',
                'PIL.ImageDraw',
                'PIL.ImageFont',
                'PIL.ImageFilter',
                'PIL.IcoImagePlugin',
                'PIL.BmpImagePlugin',
                'PIL.TiffImagePlugin',
                'enchant',
                'htmlentitydefs',
                'HTMLParser',
                'xml',
                ]

    def _getCurrentVersion(self):
        """
        Get current version from file
        """
        from outwiker.core.system import getCurrentDir

        fname = "versions.xml"
        path = os.path.join(getCurrentDir(), fname)

        text = readTextFile(fname)
        appinfo = XmlVersionParser([u'en']).parse(text)

        version_str = u'.'.join([unicode(item) for item in appinfo.currentVersion])
        return version_str

    def build(self):
        includeFiles = [
            'images',
            'help',
            'locale',
            'versions.xml',
            'styles',
            'iconset',
            'plugins',
            'spell',
            ('../LICENSE.txt', 'LICENSE.txt'),
            ('../copyright.txt', 'copyright.txt'),
        ] + self._getExtraIncludeFiles()

        build_exe_options = {
            'excludes': self._getExcludes(),
            'packages': self._getPackages(),
            'include_files': includeFiles,
            "bin_path_includes": self._getPathIncludes(),
            # For cx_Freeze 5.0.x
            # 'zip_include_packages': ['outwiker', 'wx', 'wx.html', 'PIL', 'comtypes',
            #                          'ctypes', 'importlib', 'logging', 'xml',
            #                          'enchant', 'encodings', 'pkg_resources', 'packaging',
            #                          'bz2'],
        }
        build_exe_options.update(self._getExtraBuildExeOptions())

        executable = self._getExecutable()

        setup(
            name="OutWiker",
            version=self._getCurrentVersion(),
            description="OutWiker",
            options={'build_exe': build_exe_options},
            executables=[executable]
            )


class WindowsBuilder(BaseBuilder):
    def _getExtraIncludeFiles(self):
        return [
           ('../../../need_for_build/windows/libs/lib', 'lib'),

           ('../../../need_for_build/windows/libs/libenchant-1.dll',
            'libenchant-1.dll'),

           ('../../../need_for_build/windows/libs/libglib-2.0-0.dll',
            'libglib-2.0-0.dll'),

           ('../../../need_for_build/windows/libs/libgmodule-2.0-0.dll',
            'libgmodule-2.0-0.dll'),
        ]

    def _getExtraBuildExeOptions(self):
        return {
            'include_msvcr': True,
            }

    def _getExecutable(self):
        return Executable("runoutwiker.py",
                          base='Win32GUI',
                          icon="images/outwiker.ico",
                          targetName="outwiker.exe")


class LinuxBuilder(BaseBuilder):
    def _getExecutable(self):
        return Executable("runoutwiker.py",
                          icon="images/outwiker.ico",
                          targetName="outwiker")

    def _getPathIncludes(self):
        return [u'/usr/lib']

    def _getExtraIncludeFiles(self):
        return [
            ('../need_for_build/linux/libs_amd64/libgcrypt.so.20',
             'libgcrypt.so.20'),
            ('../need_for_build/linux/libs_amd64/libglib-2.0.so.0',
             'libglib-2.0.so.0'),
        ]


if __name__ == '__main__':
    if os.name == "nt":
        WindowsBuilder().build()
    else:
        LinuxBuilder().build()
