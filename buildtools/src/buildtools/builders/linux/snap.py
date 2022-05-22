# -*- coding: utf-8 -*-

import glob
import os
import shutil

from invoke import Context

from ..base import BuilderBase
from buildtools.defines import SNAP_BUILD_DIR, PLUGINS_DIR
from buildtools.template import substitute_in_file
from buildtools.utilites import print_info


class BuilderSnap(BuilderBase):
    """
    A class to build snap package
    """

    def __init__(self, c: Context, snap_params):
        super().__init__(c, SNAP_BUILD_DIR)
        self._snap_params = snap_params

    def _build(self):
        self._clear_sources()
        self._copy_info_files()
        self._create_dirs_tree()
        self._build_snap()
        self._copy_snap_to_dest_dir()

    def _getBuildReturnValue(self):
        return self.get_snap_files()

    def get_snap_files(self):
        snap_files = []

        for fname in glob.glob(os.path.join(self.facts.build_dir_linux,
                                            '*.snap')):
            snap_files.append(fname)

        return snap_files

    def _copy_snap_to_dest_dir(self):
        for fname in glob.glob(os.path.join(self.facts.temp_dir, '*.snap')):
            shutil.copy(fname, self.facts.build_dir_linux)

    def _build_snap(self):
        print_info('Build snap')
        with self.context.cd(self.facts.temp_dir):
            snap_params = ' '.join(self._snap_params)
            self.context.run('snapcraft snap {params}'.format(params=snap_params))
            # self.context.run('sudo snapcraft snap {params}'.format(params=snap_params))

        # self.context.run('docker run --rm -v "$PWD":/build -w /build snapcore/snapcraft bash -c "apt update && snapcraft"')

    def _build_man(self, usr_share):
        '''
        Copy man files and archive them
        '''
        man_path = os.path.join(usr_share, 'man')
        shutil.copytree(os.path.join(self.facts.nfb_linux, 'man'), man_path)

        with self.context.cd(os.path.join(man_path, 'man1')):
            self.context.run('gzip outwiker.1')

        with self.context.cd(os.path.join(man_path, 'ru', 'man1')):
            self.context.run('gzip outwiker.1')

    def _create_dirs_tree(self):
        root = self.facts.temp_dir
        usr = os.path.join(root, 'usr')
        snap = os.path.join(root, 'snap')

        # Create tmp/usr/share
        usr_share = os.path.join(usr, 'share')

        # Copy usr folder
        shutil.copytree(os.path.join(self.facts.nfb_snap, 'usr'),
                        os.path.join(root, 'usr'))

        self._build_man(usr_share)

        # Create tmp/usr/share/outwiker
        usr_share_outwiker = os.path.join(usr_share, 'outwiker')
        shutil.move(self.temp_sources_dir, usr_share_outwiker)

        # Create tmp/snap
        shutil.copytree(os.path.join(self.facts.nfb_snap, 'snap'), snap)
        self._prepare_snapcraft_file(os.path.join(snap, 'snapcraft.yaml'))

        # Copy plug-ins
        dest_plugins_dir = os.path.join(usr_share_outwiker, PLUGINS_DIR)
        self._copy_plugins(dest_plugins_dir)

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
