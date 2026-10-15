# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
from pathlib import Path
import shutil

from cx_Freeze import Executable, Freezer
from invoke.context import Context
from buildtools.utilites import remove, print_info


class BaseBinaryBuilder(metaclass=ABCMeta):
    """Base class for any binary builders"""

    def __init__(self, c: Context, src_dir: str, dest_dir: str, temp_dir: str):
        self.context = c
        self._src_dir = src_dir
        self._dest_dir = dest_dir
        self._temp_dir = temp_dir

        print_info(f"Temporary directory: {self._temp_dir}")
        print_info(f"Src directory: {self._src_dir}")
        print_info(f"Dest directory: {self._dest_dir}")

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
            "outwiker.api.core.utils",
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
            "hunspell",
            "urllib.request",
        ]

    def get_includes_dirs(self):
        return [
            "plugins",
        ]

    def get_additional_files(self):
        return [
            ("LICENSE.txt", "."),
            ("copyright.txt", "."),
        ]

    def _copy_additional_files(self):
        for fname, subpath in self.get_additional_files():
            dest_dir = os.path.join(self._dest_dir, subpath)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            print_info("Copy: {} -> {}".format(fname, dest_dir))
            shutil.copy(fname, dest_dir)


class BaseCxFreezeBuilder(BaseBinaryBuilder, metaclass=ABCMeta):
    """Class for binary assembling creation with cx_freeze."""

    def __init__(self, c: Context, src_dir, dest_dir, temp_dir):
        super().__init__(c, src_dir, dest_dir, temp_dir)

    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        return []

    def _get_executable(self) -> Executable:
        """
        Return the description of the executable file to create.

        The paths in the description are relative to the source directory
        (self._src_dir).
        """
        return Executable(
            script=os.path.join(self._src_dir, "outwiker/__main__.py"),
            base="gui",
            target_name="outwiker",
            icon=os.path.join(self._src_dir, "outwiker/data/images/outwiker.ico"),
        )

    def _get_freezer_params(self):
        """
        Return the parameters for the cx_Freeze Freezer class.

        The paths in the parameters are relative to the source directory
        (self._src_dir).
        """
        return {
            "includes": self.get_includes(),
            "excludes": self.get_excludes(),
            "include_files": self.get_includes_dirs(),
            "optimize": 2,
            "silent": 1,
        }

    def build(self):
        self._create_application()
        self._remove_files()
        self._copy_additional_files()

    def _create_application(self):
        """
        Create the application files with cx_Freeze.
        """
        dest_dir = os.path.abspath(self._dest_dir)

        params = self._get_freezer_params()

        print_info("Run cx_Freeze with the parameters:")
        for key, value in params.items():
            print_info(f"    {key} = {value}")

        freezer = Freezer([self._get_executable()], target_dir=dest_dir, **params)
        freezer.freeze()

    def _remove_files(self):
        for fname in self.get_remove_list():
            print_info("Remove: {}".format(fname))
            remove(fname)


class CxFreezeBuilderWindows(BaseCxFreezeBuilder):
    pass
