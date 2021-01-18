# -*- coding: utf-8 -*-

import os.path
import sys

from fabric.api import cd, put

from buildtools.buildfacts import BuildFacts
from buildtools.utilites import print_error
from buildtools.defines import (FILES_FOR_UPLOAD_STABLE_WIN,
                                FILES_FOR_UPLOAD_STABLE_LINUX,
                                FILES_FOR_UPLOAD_UNSTABLE_WIN,
                                FILES_FOR_UPLOAD_UNSTABLE_LINUX)


class DistribsUploader(object):
    '''
    Class to upload binary files to server.
    '''

    def __init__(self,
                 version: str,
                 is_stable: bool,
                 windows_binary_path: str,
                 deploy_path: str):
        self.deploy_path = deploy_path

        self.facts = BuildFacts()

        if is_stable:
            win_tpl_files = FILES_FOR_UPLOAD_STABLE_WIN
            linux_tpl_files = FILES_FOR_UPLOAD_STABLE_LINUX
        else:
            win_tpl_files = FILES_FOR_UPLOAD_UNSTABLE_WIN
            linux_tpl_files = FILES_FOR_UPLOAD_UNSTABLE_LINUX

        files_for_upload_win = [fname.format(version=version[0],
                                             build=version[1])
                                for fname in win_tpl_files]
        files_for_upload_linux = [fname.format(version=version[0],
                                               build=version[1])
                                  for fname in linux_tpl_files]

        upload_files_win = [os.path.join(
            windows_binary_path, item) for item in files_for_upload_win]

        upload_files_linux = [os.path.join(self.facts.build_dir_linux, item)
                              for item in files_for_upload_linux]

        self.upload_files = upload_files_win + upload_files_linux

    def deploy(self):
        # Check files for existence
        for fname in self.upload_files:
            if not os.path.exists(fname):
                print_error('Error. File not found: {}'.format(fname))
                sys.exit(1)

        for fname in self.upload_files:
            with cd(self.deploy_path):
                basename = os.path.basename(fname)
                put(fname, basename)
