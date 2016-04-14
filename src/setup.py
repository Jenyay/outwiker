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
    def _getIncludeFiles (self):
        pass


    @abstractmethod
    def _getTargetName (self):
        pass


    def _getAdvancedBuildExeOptions (self):
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
        Получить текущую версию для файла
        """
        from outwiker.core.system import getCurrentDir

        fname = "version.txt"
        path = os.path.join (getCurrentDir(), fname)

        with open (path) as fp:
            lines = fp.readlines()

        version_str = "%s.%s" % (lines[0].strip(), lines[1].strip())
        return version_str


    def build (self):
        build_exe_options = {
            'excludes': self._getExcludes(),
            'packages': self._getPackages(),
            'include_files': self._getIncludeFiles(),
            }
        build_exe_options.update (self._getAdvancedBuildExeOptions())

        setup (
            name = "OutWiker",
            version = self._getCurrentVersion(),
            description = "Wiki + Outliner",
            options = {'build_exe': build_exe_options},
            executables = [Executable(
                                "runoutwiker.py",
                                icon = "images/outwiker.ico",
                                targetName=self._getTargetName()
                                )
                           ]
            )


class WindowsBuilder (BaseBuilder):
    def _getIncludeFiles (self):
        return [
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
            ('../libs/lib', 'lib'),
            ('../libs/libenchant-1.dll', 'libenchant-1.dll'),
            ('../libs/libglib-2.0-0.dll', 'libglib-2.0-0.dll'),
            ('../libs/libgmodule-2.0-0.dll', 'libgmodule-2.0-0.dll'),
        ]


    def _getTargetName (self):
        return u'outwiker.exe'


    def _getAdvancedBuildExeOptions (self):
        return {
            'include_msvcr': True,
            }


class LinuxBuilder (BaseBuilder):
    def _getIncludeFiles (self):
        return [
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
        ]


    def _getTargetName (self):
        return u'outwiker'



if __name__ == '__main__':
    if os.name == "nt":
        WindowsBuilder().build()
    else:
        LinuxBuilder().build()
