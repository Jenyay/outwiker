# -*- coding: utf-8 -*-

import glob
import os
import shutil

from fabric.api import local, lcd

from ..base import BuilderBase
from buildtools.defines import SNAP_BUILD_DIR, PLUGINS_DIR, PLUGINS_LIST
from buildtools.template import substitute_in_file
from buildtools.utilites import print_info


class BuilderSnap(BuilderBase):
    """
    A class to build snap package
    """
    def __init__(self, is_stable):
        super().__init__(SNAP_BUILD_DIR, is_stable)

    def _build(self):
        self._clear_sources()
        os.remove(os.path.join(self.temp_sources_dir, 'linux_runtime_hook.py'))
        self._copy_info_files()
        self._create_dirs_tree()
        self._build_snap()
        self._copy_snap_to_dest_dir()

    def _getBuildReturnValue(self):
        return self.get_snap_files()

    def get_snap_files(self):
        snap_files = []

        for fname in glob.glob(os.path.join(self.facts.temp_dir, '*.snap')):
            snap_files.append(os.path.join(self.facts.build_dir_linux, fname))

        return snap_files

    def _copy_snap_to_dest_dir(self):
        for fname in glob.glob(os.path.join(self.facts.temp_dir, '*.snap')):
            shutil.copy(fname, self.facts.build_dir_linux)

    def _build_snap(self):
        print_info('Build snap')
        with lcd(self.facts.temp_dir):
            local('snapcraft cleanbuild')

    def _create_dirs_tree(self):
        root = self.facts.temp_dir
        usr = os.path.join(root, 'usr')
        share = os.path.join(root, 'share')
        snap = os.path.join(root, 'snap')

        # Create tmp/usr/share
        usr_share = os.path.join(usr, 'share')
        os.makedirs(usr_share, exist_ok=True)

        # Create tmp/usr/share/outwiker
        usr_share_outwiker = os.path.join(usr_share, 'outwiker')
        shutil.move(self.temp_sources_dir, usr_share_outwiker)

        # Create tmp/usr/share/bin
        shutil.copytree(os.path.join(self.facts.nfb_snap, 'usr', 'bin'),
                        os.path.join(usr, 'bin'))

        # Create tmp/share
        shutil.copytree(os.path.join(self.facts.nfb_snap, 'share'), share)

        # Create tmp/snap
        shutil.copytree(os.path.join(self.facts.nfb_snap, 'snap'), snap)
        self._prepare_snapcraft_file(os.path.join(snap, 'snapcraft.yaml'))

        # Copy plug-ins
        self._copy_plugins(usr_share_outwiker)

    def _copy_plugins(self, usr_share_outwiker):
        print_info('Copy plugins:')
        dest_plugins_dir = os.path.join(usr_share_outwiker, PLUGINS_DIR)
        if not os.path.exists(dest_plugins_dir):
            os.mkdir(dest_plugins_dir)

        for plugin_name in PLUGINS_LIST:
            print_info('    {}'.format(plugin_name))

            src_dir = os.path.join(self.facts.src_plugins_dir,
                                   plugin_name,
                                   plugin_name)
            shutil.copytree(src_dir,
                            os.path.join(dest_plugins_dir, plugin_name),
                            ignore=shutil.ignore_patterns('__pycache__'))

    def _prepare_snapcraft_file(self, snapcraft_file):
        substitute_in_file(snapcraft_file,
                           version=self.facts.version)

    def _copy_info_files(self):
        files = ['README', 'copyright.txt', 'LICENSE.txt']
        for fname in files:
            shutil.copy(fname, self.temp_sources_dir)

    def clear(self):
        super().clear()
        self._remove(self.getResultPath())

    def getResultPath(self):
        return self.build_dir
