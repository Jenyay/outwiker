# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
from pathlib import Path
import shutil

from fabric.api import lcd, local

from buildtools.utilites import remove, print_info


class BaseBinaryBuilder(object, metaclass=ABCMeta):
    """Base class for any binary builders"""

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
            'outwiker.gui.htmlrenderfactory',
            'outwiker.gui.controls.popupbutton',
            'outwiker.utilites.actionsguicontroller',
            'PIL.Image',
            'PIL.ImageDraw',
            'PIL.ImageFont',
            'PIL.ImageFilter',
            'PIL.IcoImagePlugin',
            'PIL.BmpImagePlugin',
            'PIL.TiffImagePlugin',
            'enchant',
            'xml',
            'json',
            'asyncio',
        ]

    def get_additional_files(self):
        return []

    def _copy_additional_files(self):
        root_dir = os.path.join(self._dist_dir, u'outwiker')

        for fname, subpath in self.get_additional_files():
            dest_dir = os.path.join(root_dir, subpath)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            print_info(u'Copy: {} -> {}'.format(fname, dest_dir))
            shutil.copy(fname, dest_dir)


class BasePyInstallerBuilder(BaseBinaryBuilder, metaclass=ABCMeta):
    """Class for binary assimbling creation with PyParsing. """

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
        self._copy_additional_files()

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

    def get_files_by_mask(self, directory, mask):
        return [str(fname.resolve()) for fname in Path(directory).glob(mask)]


class PyInstallerBuilderWindows(BasePyInstallerBuilder):
    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        to_remove = [
            u'_win32sysloader.pyd',
            u'win32com.shell.shell.pyd',
            u'win32trace.pyd',
            u'win32wnet.pyd',
            u'iconv.dll',
            u'_winxptheme.pyd',
            u'enchant/iconv.dll',
            u'enchant/share',
            u'enchant/lib/enchant/README.txt',
            u'mfc140u.dll',
            u'include',
        ]

        to_remove += [fname.name for fname
                      in Path(self._dist_dir, 'outwiker').glob('api-ms-win*.dll')]

        return to_remove


class PyInstallerBuilderLinuxBase(BasePyInstallerBuilder):
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

    def build(self):
        super(PyInstallerBuilderLinuxBase, self).build()
        self._strip_binary()

    def _strip_binary(self):
        strip_path = Path(self._dest_dir)
        files_for_strip = (list(strip_path.glob('libwx*.so.*')) +
                           list(strip_path.glob('wx.*so')))

        for fname in files_for_strip:
            print_info(u'Strip {}'.format(fname))
            if os.path.exists(str(fname)):
                local(u'strip -s -o "{fname}" "{fname}"'.format(fname=fname))

    def get_includes(self):
        result = super(PyInstallerBuilderLinuxBase, self).get_includes()
        # result.append('gi')
        # result.append('gi.repository.Gtk')
        # result.append('gi.repository.GdkPixbuf')
        return result

    def append_so_files(self, files, modules_dir, dir_dest):
        so_files = self.get_files_by_mask(modules_dir, '*.so')
        files += [(fname, dir_dest) for fname in so_files]


class PyInstallerBuilderLinuxSimple(PyInstallerBuilderLinuxBase):
    def get_additional_files(self):
        files = []
        self._append_pixbuf_files(files)
        self._append_immodules_files(files)
        return files

    def _append_immodules_files(self, files):
        dir_dest = u'lib/immodules'
        modules_dir = u'/usr/lib/x86_64-linux-gnu/gtk-3.0/3.0.0/immodules/'

        files.append(('need_for_build/linux/immodules.cache', dir_dest))
        self.append_so_files(files, modules_dir, dir_dest)

    def _append_pixbuf_files(self, files):
        dir_dest = u'lib/gdk-pixbuf'
        modules_dir = u'/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders'

        files.append(('need_for_build/linux/loaders.cache', dir_dest))
        self.append_so_files(files, modules_dir, dir_dest)

    def get_params(self):
        params = super(PyInstallerBuilderLinuxSimple, self).get_params()
        params.append(u'--runtime-hook=linux_runtime_hook.py')
        return params
