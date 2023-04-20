# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
from pathlib import Path
import shutil

from invoke import Context
from buildtools.utilites import remove, print_info


class BaseBinaryBuilder(metaclass=ABCMeta):
    """Base class for any binary builders"""

    def __init__(self, c: Context, src_dir: str, dest_dir: str, temp_dir: str):
        self.context = c
        self._src_dir = src_dir
        self._dest_dir = dest_dir
        self._temp_dir = temp_dir

    @abstractmethod
    def build(self):
        pass

    def get_excludes(self):
        """Return modules list to exclude from build. """
        return [
            'tkinter',
            'PyQt4',
            'PyQt5',
            'unittest',
            'sqlite3',
            'numpy',
            'pydoc',
            'test',
            'pycparser',
            'xmlrpclib',
            'bz2',
            'cffi',
            'bsddb',
            'pytest',
            'Sphynx',
            'PIL.SunImagePlugin',
            'PIL.IptcImagePlugin',
            'PIL.McIdasImagePlugin',
            'PIL.DdsImagePlugin',
            'PIL.FpxImagePlugin',
            'PIL.PixarImagePlugin',
        ]

    def get_includes(self):
        """Return modules list to include to build. """
        return [
            'importlib',
            'urllib',
            'outwiker.api',
            'outwiker.api.core',
            'outwiker.api.core.attachment',
            'outwiker.api.core.config',
            'outwiker.api.core.defines',
            'outwiker.api.core.events',
            'outwiker.api.core.exceptions',
            'outwiker.api.core.hashcalculator',
            'outwiker.api.core.html',
            'outwiker.api.core.images',
            'outwiker.api.core.pagecontentcache',
            'outwiker.api.core.text',
            'outwiker.api.core.tree',
            'outwiker.api.core.plugins',
            'outwiker.api.core.pagestyle',
            'outwiker.api.core.tags',
            'outwiker.api.gui',
            'outwiker.api.gui.actions',
            'outwiker.api.gui.basetextstylingcontroller',
            'outwiker.api.gui.configelements',
            'outwiker.api.gui.controls',
            'outwiker.api.gui.defines',
            'outwiker.api.gui.dialogs',
            'outwiker.api.gui.hotkeys',
            'outwiker.api.gui.longprocessrunner',
            'outwiker.api.gui.mainwindow',
            'outwiker.api.gui.preferences',
            'outwiker.api.gui.texteditorhelper',
            'outwiker.api.app',
            'outwiker.api.app.application',
            'outwiker.api.app.config',
            'outwiker.api.app.attachment',
            'outwiker.api.app.bookmarks',
            'outwiker.api.app.clipboard',
            'outwiker.api.app.messages',
            'outwiker.api.app.system',
            'outwiker.api.app.texteditor',
            'outwiker.api.app.tree',
            'outwiker.api.pages',
            'outwiker.api.pages.wiki',
            'outwiker.api.pages.wiki.config',
            'outwiker.api.pages.wiki.defines',
            'outwiker.api.pages.wiki.editor',
            'outwiker.api.pages.wiki.wikiparser',
            'outwiker.api.pages.wiki.wikipage',
            'outwiker.actions.close',
            'outwiker.actions.showhideattaches',
            'outwiker.actions.showhidetags',
            'outwiker.actions.showhidetree',
            'outwiker.gui.controls.popupbutton',
            'outwiker.gui.controls.filestreectrl',
            'outwiker.core.attachfilters',
            'outwiker.core.commands',
            'outwiker.utilites.actionsguicontroller',
            'outwiker.utilites.text',
            'PIL.Image',
            'PIL.ImageFile',
            'PIL.ImageDraw',
            'PIL.ImageDraw2',
            'PIL.ImageFont',
            'PIL.ImageFilter',
            'PIL.IcoImagePlugin',
            'PIL.PngImagePlugin',
            'PIL.BmpImagePlugin',
            'PIL.TiffImagePlugin',
            'PIL.JpegImagePlugin',
            'xml',
            'json',
            'asyncio',
            'html.parser',
            'pkg_resources',
            'hunspell',
            'hunspell.platform',
            'cacheman',
            'cacheman.cachewrap',
        ]

    def get_includes_dirs(self):
        return ['help', 'iconset', 'images', 'locale', 'spell',
                'styles', 'textstyles', 'plugins']

    def get_additional_files(self):
        return []

    def _copy_additional_files(self):
        root_dir = os.path.join(self._dist_dir, u'outwiker')

        for fname, subpath in self.get_additional_files():
            dest_dir = os.path.join(root_dir, subpath)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            print_info('Copy: {} -> {}'.format(fname, dest_dir))
            shutil.copy(fname, dest_dir)


class BasePyInstallerBuilder(BaseBinaryBuilder, metaclass=ABCMeta):
    """Class for binary assembling creation with PyInstaller. """

    def __init__(self, src_dir, dest_dir, temp_dir):
        super().__init__(src_dir, dest_dir, temp_dir)

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
                  u'--add-binary help' + os.pathsep + u'help',
                  u'--add-binary iconset' + os.pathsep + u'iconset',
                  u'--add-binary images' + os.pathsep + u'images',
                  u'--add-binary locale' + os.pathsep + u'locale',
                  u'--add-binary spell' + os.pathsep + u'spell',
                  u'--add-binary styles' + os.pathsep + u'styles',
                  u'--add-binary textstyles' + os.pathsep + u'textstyles',
                  u'--add-binary plugins' + os.pathsep + u'plugins',
                  ]

        params += [u'--hiddenimport {}'.format(package)
                   for package
                   in self.get_includes()]

        params += [u'--exclude-module {}'.format(package)
                   for package
                   in self.get_excludes()]

        return params

    def build(self):
        params = self.get_params()
        command = u'pyinstaller runoutwiker.py ' + u' '.join(params)
        with self.context.cd(self._src_dir):
            self.context.run(command)

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


class BaseCxFreezeBuilder(BaseBinaryBuilder, metaclass=ABCMeta):
    """Class for binary assembling creation with cx_freeze. """

    def __init__(self, c: Context, src_dir, dest_dir, temp_dir):
        super().__init__(c, src_dir, dest_dir, temp_dir)

        # The path where the folder with the assembly will be created
        # (before copying to self.dest_dir)
        # build/tmp/build
        self._dist_dir = os.path.join(temp_dir, u'build')

    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        return []

    def get_params(self):
        params = ['-OO',
                  '-c',
                  '-s',
                  '--base-name Win32GUI',
                  '--target-dir "{}"'.format(self._dist_dir),
                  '--target-name outwiker',
                  '--includes {}'.format(','.join(self.get_includes())),
                  '--excludes {}'.format(','.join(self.get_excludes())),
                  '--include-files {}'.format(
                      ','.join(self.get_includes_dirs())),
                  '--icon images/outwiker.ico',
                  ]

        return params

    def build(self):
        params = self.get_params()
        command = u'cxfreeze runoutwiker.py ' + u' '.join(params)
        with self.context.cd(self._src_dir):
            self.context.run(command)

        self._remove_files()
        self._copy_additional_files()

        print_info(
            u'Copy files to dest path: {} -> {}'.format(self._dist_dir,
                                                        self._dest_dir))

        shutil.copytree(self._dist_dir, self._dest_dir)

    def _remove_files(self):
        toRemove = [os.path.join(self._dist_dir, u'outwiker', fname)
                    for fname in self.get_remove_list()]

        for fname in toRemove:
            print_info(u'Remove: {}'.format(fname))
            remove(fname)

    def get_files_by_mask(self, directory, mask):
        return [str(fname.resolve()) for fname in Path(directory).glob(mask)]


class CxFreezeBuilderWindows(BaseCxFreezeBuilder):
    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        to_remove = [
            u'_win32sysloader.pyd',
            u'win32com.shell.shell.pyd',
            u'win32trace.pyd',
            u'win32wnet.pyd',
            u'iconv.dll',
            u'_winxptheme.pyd',
            u'mfc140u.dll',
            u'include',
        ]

        to_remove += [fname.name for fname
                      in Path(self._dist_dir, 'outwiker').glob('api-ms-win*.dll')]

        return to_remove


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
            u'mfc140u.dll',
            u'include',
        ]

        to_remove += [fname.name for fname
                      in Path(self._dist_dir, 'outwiker').glob('api-ms-win*.dll')]

        return to_remove


class PyInstallerBuilderLinuxBase(BasePyInstallerBuilder):
    def get_remove_list(self):
        return [
            'lib',
            'include',
            '_codecs_cn.so',
            '_codecs_hk.so',
            '_codecs_iso2022.so',
            '_codecs_jp.so',
            '_codecs_kr.so',
            '_codecs_tw.so',

            # libstdc++.so.6, libgio-2.0.so.0 etc must be excluded
            # else application will be fall
            'libstdc++.so.6',
            'libgio-2.0.so.0',
            'libc.so.6',
            'libgdk_pixbuf-2.0.so.0',
            'libz.so.1',
            'libglib-2.0.so.0',

            # List of excludes from AppImage recomendations
            # https://github.com/AppImage/AppImages/blob/master/excludelist

            'libgobject-2.0.so.0',
            'libGL.so.1',
            'libEGL.so.1',
            'libdrm.so.2',
            'libX11.so.6',
            'libasound.so.2',
            'libfontconfig.so.1',
            'libexpat.so.1',
            'libgcc_s.so.1',
            'libgpg-error.so.0',
            'libICE.so.6',
            'libSM.so.6',
            'libuuid.so.1',
            'libgpg-error.so.0',
            'libX11-xcb.so.1',
            'libfreetype.so.6',
            'libfreetype-550560cb.so',
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
                self.context.run('strip -s -o "{fname}" "{fname}"'.format(fname=fname))

    def get_includes(self):
        result = super().get_includes()
        result.append('hunspell')
        return result

    def append_so_files(self, files, modules_dir, dir_dest):
        so_files = self.get_files_by_mask(modules_dir, '*.so')
        files += [(fname, dir_dest) for fname in so_files]


class PyInstallerBuilderLinuxSimple(PyInstallerBuilderLinuxBase):
    pass
