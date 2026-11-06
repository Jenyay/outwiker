# -*- coding: utf-8 -*-

import os
import shutil

from invoke import Context

from .base import BuilderBase
from .binarybuilders import CxFreezeBuilder
from outwiker.build.defines import (
    LINUX_BUILD_DIR,
    LINUX_EXECUTABLE_DIR,
)
from outwiker.build.utilites import print_info


class BuilderLinuxBinary(BuilderBase):
    """
    Build the binary distribution for Linux with cx_Freeze
    """

    def __init__(
        self,
        c: Context,
        is_stable: bool = False,
        create_archives: bool = True,
    ):
        super().__init__(c, LINUX_BUILD_DIR, is_stable)
        self._create_archives = create_archives

        self._resultBaseName = (
            "outwiker_{version}_linux".format(version=self.facts.version_items[0])
            if self.is_stable
            else "outwiker_linux_unstable"
        )

        self._resultWithPluginsBaseName = self._resultBaseName + "_all_plugins"

        self._executable_dir = os.path.join(self.facts.temp_dir, LINUX_EXECUTABLE_DIR)

        # Path to copy plugins
        self._dest_plugins_dir = os.path.join(self._executable_dir, "plugins")

    def clear(self):
        to_remove = [
            os.path.join(self.build_dir, LINUX_EXECUTABLE_DIR),
            os.path.join(self.build_dir, self._resultBaseName + ".7z"),
            os.path.join(self.build_dir, self._resultBaseName + ".zip"),
            os.path.join(self.build_dir, self._resultWithPluginsBaseName + ".7z"),
            os.path.join(self.build_dir, self._resultWithPluginsBaseName + ".zip"),
        ]
        for fname in to_remove:
            self._remove(fname)

    def _build(self):
        print_info("Is stable: {}".format(self.is_stable))
        print_info("Create archives: {}".format(self._create_archives))

        self._create_plugins_dir()
        self._create_binary()
        self._strip_shared_libraries()
        self._clear_dest_plugins_dir()
        self._create_archives_without_plugins()
        self._copy_plugins(self._dest_plugins_dir)
        self._create_archives_with_plugins()
        self._move_executable_dir()

    def _create_binary(self):
        """
        Build with cx_Freeze
        """
        print_info("Create binary files...")
        src_dir = self.temp_sources_dir
        dest_dir = self._executable_dir
        temp_dir = self.facts.temp_dir

        builder = CxFreezeBuilder(self.context, src_dir, dest_dir, temp_dir)
        builder.build()

    def _strip_shared_libraries(self):
        """
        Remove debug information from shared libraries (.so files)
        """
        print_info("Strip debug information from shared libraries...")
        with self.context.cd(self._executable_dir):
            self.context.run(
                r"find . -type f \( -name '*.so' -o -name '*.so.[0-9]*' \) "
                r"-exec strip --strip-unneeded {} +"
            )

    def _clear_dest_plugins_dir(self):
        self._remove(self._dest_plugins_dir)
        os.mkdir(self._dest_plugins_dir)

    def _create_archives_without_plugins(self):
        if not self._create_archives:
            return

        print_info("Create archives without plugins...")
        with self.context.cd(self._executable_dir):
            path_zip = os.path.abspath(
                os.path.join(self.build_dir, self._resultBaseName + ".zip")
            )

            path_7z = os.path.abspath(
                os.path.join(self.build_dir, self._resultBaseName + ".7z")
            )

            self.context.run(r'7z a -r -aoa "{}" ./*'.format(path_zip))
            self.context.run(r'7z a -r -aoa "{}" ./*'.format(path_7z))

    def _create_archives_with_plugins(self):
        if not self._create_archives:
            return

        print_info("Create archives with plugins...")
        with self.context.cd(self._executable_dir):
            path_zip = os.path.abspath(
                os.path.join(self.build_dir, self._resultWithPluginsBaseName + ".zip")
            )

            path_7z = os.path.abspath(
                os.path.join(self.build_dir, self._resultWithPluginsBaseName + ".7z")
            )

            self.context.run(
                r'7z a -r -aoa -xr!__pycache__ -xr!.ruff_cache -xr!.ropeproject "{}" ./*'.format(
                    path_zip
                )
            )
            self.context.run(
                r'7z a -r -aoa -xr!__pycache__ -xr!.ruff_cache -xr!.ropeproject "{}" ./*'.format(
                    path_7z
                )
            )

    def _move_executable_dir(self):
        print_info("Move result directory to {}...".format(self.build_dir))
        shutil.move(self._executable_dir, self.build_dir)
