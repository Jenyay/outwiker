# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import shutil

from fabric.api import lcd, local

from buildtools.utilites import remove, print_info


class BaseBinaryBuilder(object):
    """Base class for any binary builders"""
    __metaclass__ = ABCMeta

    def __init__(self, src_dir, dest_dir, temp_dir):
        self._src_dir = src_dir
        self._dest_dir = dest_dir
        self._temp_dir = temp_dir

    @abstractmethod
    def build(self):
        pass

    def get_excludes(self):
        """Return modules list to exclude from build. """
        return [
            'Tkinter',
            'PyQt4',
            'PyQt5',
            'unittest',
            'distutils',
            'setuptools',
            'pycparser',
            'sqlite3',
            'numpy',
            'pydoc',
            'xmlrpclib',
            'test',
            'bz2',
            'cffi',
            'PIL.SunImagePlugin',
            'PIL.IptcImagePlugin',
            'PIL.McIdasImagePlugin',
            'PIL.DdsImagePlugin',
            'PIL.FpxImagePlugin',
            'PIL.PixarImagePlugin',
            'bsddb',
        ]

    def get_includes(self):
        """Return modules list to include to build. """
        return [
            'importlib',
            'urllib',
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


class BasePyInstallerBuilder(BaseBinaryBuilder):
    """Class for binary assimbling creation with PyParsing. """
    __metaclass__ = ABCMeta

    def __init__(self, src_dir, dest_dir, temp_dir):
        super(BasePyInstallerBuilder, self).__init__(
            src_dir, dest_dir, temp_dir)

        # The path where the folder with the assembly will be created
        # (before copying to self.dest_dir)
        # build/tmp/build
        self._dist_dir = os.path.join(temp_dir, u'build')

        # The path with the intermediate files (build info)
        # build/tmp/build_tmp
        self._workpath = os.path.join(temp_dir, u'build_tmp')

    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        return []

    def get_params(self):
        params = [u'--log-level WARN',
                  u'--clean',
                  u'--noconfirm',
                  u'--icon images/outwiker.ico',
                  u'--name outwiker',
                  u'--windowed',
                  u'--distpath "{}"'.format(self._dist_dir),
                  u'--workpath "{}"'.format(self._workpath),
                  u'--add-data versions.xml' + os.pathsep + u'.',
                  u'--add-binary help' + os.pathsep + u'help',
                  u'--add-binary iconset' + os.pathsep + u'iconset',
                  u'--add-binary images' + os.pathsep + u'images',
                  u'--add-binary locale' + os.pathsep + u'locale',
                  u'--add-binary spell' + os.pathsep + u'spell',
                  u'--add-binary styles' + os.pathsep + u'styles',
                  u'--add-binary plugins' + os.pathsep + u'plugins',
                  ]

        params += [u' --hiddenimport {}'.format(package)
                   for package
                   in self.get_includes()]

        params += [u' --exclude-module {}'.format(package)
                   for package
                   in self.get_excludes()]

        return params

    def build(self):
        params = self.get_params()
        command = u'pyinstaller runoutwiker.py ' + u' '.join(params)
        with lcd(self._src_dir):
            local(command)

        self._remove_files()

        print_info(u'Copy files to dest path.')
        shutil.copytree(
            os.path.join(self._dist_dir, u'outwiker'),
            self._dest_dir
        )

    def _remove_files(self):
        toRemove = [os.path.join(self._dist_dir, u'outwiker', fname)
                    for fname in self.get_remove_list()]

        for fname in toRemove:
            print_info(u'Remove: {}'.format(fname))
            remove(fname)


class PyInstallerBuilderWindows(BasePyInstallerBuilder):
    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        return [
            u'mfc90.dll',
            u'mfc90u.dll',
            u'mfcm90.dll',
            u'mfcm90u.dll',
            u'Include',
            u'Microsoft.VC90.MFC.manifest',
            u'iconv.dll',
            u'_win32sysloader.pyd',
            u'_winxptheme.pyd',
            u'win32com.shell.shell.pyd',
            u'win32pipe.pyd',
            u'win32trace.pyd',
            u'win32wnet.pyd',
            u'enchant/iconv.dll',
            u'enchant/share',
            u'enchant/lib/enchant/README.txt',
        ]


class PyInstallerBuilderLinux(BasePyInstallerBuilder):
    def get_remove_list(self):
        return [
            u'lib',
            u'include',
            u'_codecs_cn.so',
            u'_codecs_hk.so',
            u'_codecs_iso2022.so',
            u'_codecs_jp.so',
            u'_codecs_kr.so',
            u'_codecs_tw.so',
        ]
