#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cx_Freeze import setup, Executable
import os
from abc import ABCMeta, abstractmethod

from outwiker.core.defines import WX_VERSION
import wxversion
wxversion.select(WX_VERSION)


class BaseBuilder (object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def _getExecutable (self):
        pass


    def _getExtraIncludeFiles (self):
        return []


    def _getPathIncludes (self):
        return []


    def _getExtraBuildExeOptions (self):
        return {}


    def _getExcludes (self):
        return ['numpy',
                'scipy',
                'tkinter',
                'PyQt4',
                ]


    def _getPackages (self):
        # Добавляем 'outwiker.pages.wiki.wikipanel',
        # т.к. этот модуль используется только в старых версиях плагинов
        return ['urllib',
                'urllib2',
                'outwiker.pages.wiki.wikipanel',
                'outwiker.gui.htmlrenderfactory',
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
                ]


    def _getCurrentVersion (self):
        """
        Get current version from file
        """
        from outwiker.core.system import getCurrentDir

        fname = "version.txt"
        path = os.path.join (getCurrentDir(), fname)

        with open (path) as fp:
            lines = fp.readlines()

        version_str = "%s.%s" % (lines[0].strip(), lines[1].strip())
        return version_str


    def build (self):
        includeFiles = [
            'images',
            'help',
            'locale',
            'version.txt',
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
        }
        build_exe_options.update (self._getExtraBuildExeOptions())

        executable = self._getExecutable()

        setup (
            name = "OutWiker",
            version = self._getCurrentVersion(),
            description = "Wiki + Outliner",
            options = {'build_exe': build_exe_options},
            executables = [executable]
            )



class WindowsBuilder (BaseBuilder):
    def _getExtraIncludeFiles (self):
        return [
            ('../libs/lib', 'lib'),
            ('../libs/libenchant-1.dll', 'libenchant-1.dll'),
            ('../libs/libglib-2.0-0.dll', 'libglib-2.0-0.dll'),
            ('../libs/libgmodule-2.0-0.dll', 'libgmodule-2.0-0.dll'),
        ]


    def _getExtraBuildExeOptions (self):
        return {
            'include_msvcr': True,
            }


    def _getExecutable (self):
        return Executable("runoutwiker.py",
                          base = 'Win32GUI',
                          icon = "images/outwiker.ico",
                          targetName="outwiker.exe")



class LinuxBuilder (BaseBuilder):
    def _getExecutable (self):
        return Executable("runoutwiker.py",
                          icon = "images/outwiker.ico",
                          targetName="outwiker")


    def _getPathIncludes (self):
        return ["/usr/lib"]



if __name__ == '__main__':
    if os.name == "nt":
        WindowsBuilder().build()
    else:
        LinuxBuilder().build()
