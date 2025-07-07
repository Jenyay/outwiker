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
        """Return modules list to exclude from build."""
        return [
            "tkinter",
            "PyQt4",
            "PyQt5",
            "unittest",
            "sqlite3",
            "numpy",
            "pydoc",
            "test",
            "pycparser",
            "xmlrpclib",
            "bz2",
            "cffi",
            "bsddb",
            "pytest",
            "Sphynx",
            "PIL.SunImagePlugin",
            "PIL.IptcImagePlugin",
            "PIL.McIdasImagePlugin",
            "PIL.DdsImagePlugin",
            "PIL.FpxImagePlugin",
            "PIL.PixarImagePlugin",
        ]

    def get_includes(self):
        """Return modules list to include to build."""
        return [
            "importlib",
            "urllib",
            "outwiker.api",
            "outwiker.api.core",
            "outwiker.api.core.attachment",
            "outwiker.api.core.config",
            "outwiker.api.core.defines",
            "outwiker.api.core.events",
            "outwiker.api.core.exceptions",
            "outwiker.api.core.hashcalculator",
            "outwiker.api.core.html",
            "outwiker.api.core.images",
            "outwiker.api.core.pagecontentcache",
            "outwiker.api.core.text",
            "outwiker.api.core.tree",
            "outwiker.api.core.plugins",
            "outwiker.api.core.pagestyle",
            "outwiker.api.core.spellchecker",
            "outwiker.api.core.tags",
            "outwiker.api.gui",
            "outwiker.api.gui.actions",
            "outwiker.api.gui.basetextstylingcontroller",
            "outwiker.api.gui.configelements",
            "outwiker.api.gui.controls",
            "outwiker.api.gui.defines",
            "outwiker.api.gui.dialogs",
            "outwiker.api.gui.hotkeys",
            "outwiker.api.gui.images",
            "outwiker.api.gui.longprocessrunner",
            "outwiker.api.gui.mainwindow",
            "outwiker.api.gui.preferences",
            "outwiker.api.gui.texteditorhelper",
            "outwiker.api.app",
            "outwiker.api.app.application",
            "outwiker.api.app.config",
            "outwiker.api.app.attachment",
            "outwiker.api.app.bookmarks",
            "outwiker.api.app.clipboard",
            "outwiker.api.app.messages",
            "outwiker.api.app.system",
            "outwiker.api.app.texteditor",
            "outwiker.api.app.tree",
            "outwiker.api.pages",
            "outwiker.api.pages.html",
            "outwiker.api.pages.html.gui",
            "outwiker.api.pages.html.guitools",
            "outwiker.api.pages.html.actions",
            "outwiker.api.pages.wiki",
            "outwiker.api.pages.wiki.config",
            "outwiker.api.pages.wiki.defines",
            "outwiker.api.pages.wiki.editor",
            "outwiker.api.pages.wiki.gui",
            "outwiker.api.pages.wiki.wikiparser",
            "outwiker.api.pages.wiki.wikipage",
            "outwiker.gui.controls.popupbutton",
            "outwiker.gui.controls.filestreectrl",
            "outwiker.gui.images",
            "outwiker.core.attachfilters",
            "outwiker.utilites.actionsguicontroller",
            "outwiker.utilites.text",
            "PIL.Image",
            "PIL.ImageFile",
            "PIL.ImageDraw",
            "PIL.ImageDraw2",
            "PIL.ImageFont",
            "PIL.ImageFilter",
            "PIL.IcoImagePlugin",
            "PIL.PngImagePlugin",
            "PIL.BmpImagePlugin",
            "PIL.TiffImagePlugin",
            "PIL.JpegImagePlugin",
            "xml",
            "json",
            "asyncio",
            "html.parser",
            "pkg_resources",
            "hunspell",
            "hunspell.platform",
            "cacheman",
            "cacheman.cachewrap",
        ]

    def get_includes_dirs(self):
        return [
            "plugins",
        ]

    def get_additional_files(self):
        return []

    def _copy_additional_files(self):
        root_dir = os.path.join(self._dist_dir, "outwiker")

        for fname, subpath in self.get_additional_files():
            dest_dir = os.path.join(root_dir, subpath)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            print_info("Copy: {} -> {}".format(fname, dest_dir))
            shutil.copy(fname, dest_dir)


class BaseCxFreezeBuilder(BaseBinaryBuilder, metaclass=ABCMeta):
    """Class for binary assembling creation with cx_freeze."""

    def __init__(self, c: Context, src_dir, dest_dir, temp_dir):
        super().__init__(c, src_dir, dest_dir, temp_dir)

        # The path where the folder with the assembly will be created
        # (before copying to self.dest_dir)
        # build/tmp/build
        self._dist_dir = os.path.join(temp_dir, "build")

    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        return []

    def get_params(self):
        params = [
            "--optimize=2",
            "--silent",
            "--base-name Win32GUI",
            '--target-dir "{}"'.format(self._dist_dir),
            "--target-name outwiker",
            "--includes {}".format(",".join(self.get_includes())),
            "--excludes {}".format(",".join(self.get_excludes())),
            "--include-files {}".format(",".join(self.get_includes_dirs())),
            "--icon outwiker/data/images/outwiker.ico",
        ]

        return params

    def build(self):
        params = self.get_params()
        command = "cxfreeze outwiker/__main__.py " + " ".join(params)
        with self.context.cd(self._src_dir):
            print_info(command)
            self.context.run(command)

        self._remove_files()
        self._copy_additional_files()

        print_info(
            "Copy files to dest path: {} -> {}".format(self._dist_dir, self._dest_dir)
        )

        shutil.copytree(self._dist_dir, self._dest_dir)

    def _remove_files(self):
        toRemove = [
            os.path.join(self._dist_dir, "outwiker", fname)
            for fname in self.get_remove_list()
        ]

        for fname in toRemove:
            print_info("Remove: {}".format(fname))
            remove(fname)

    def get_files_by_mask(self, directory, mask):
        return [str(fname.resolve()) for fname in Path(directory).glob(mask)]


class CxFreezeBuilderWindows(BaseCxFreezeBuilder):
    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        to_remove = [
            "_win32sysloader.pyd",
            "win32com.shell.shell.pyd",
            "win32trace.pyd",
            "win32wnet.pyd",
            "iconv.dll",
            "_winxptheme.pyd",
            "mfc140u.dll",
            "include",
        ]

        to_remove += [
            fname.name
            for fname in Path(self._dist_dir, "outwiker").glob("api-ms-win*.dll")
        ]

        return to_remove
