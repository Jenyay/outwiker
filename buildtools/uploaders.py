# -*- coding: utf-8 -*-

import os.path
import urllib2
import sys

from fabric.api import cd, put

from .versions import (getOutwikerVersion,
                       getOutwikerVersionStr,
                       readAppInfo,
                       downloadAppInfo)
from .serverinfo import (PATH_TO_WINDOWS_DISTRIBS)
from .defines import WINDOWS_BUILD_DIR
from .libs.colorama import Fore
from .buildfacts import BuildFacts


class BinaryUploader(object):
    '''
    Class to upload binary files to server.
    '''
    def __init__(self,
                 win_tpl_files, linux_tpl_files, versions_file,
                 deploy_path):
        self.facts = BuildFacts()

        self.deploy_path = deploy_path
        self.versions_file = versions_file

        version = getOutwikerVersion()
        version_dir = getOutwikerVersionStr()

        files_for_upload_win = [fname.format(version=version[0])
                                for fname in win_tpl_files]
        files_for_upload_linux = [fname.format(version=version[0])
                                  for fname in linux_tpl_files]

        src_path_win = os.path.join(PATH_TO_WINDOWS_DISTRIBS,
                                    version_dir,
                                    WINDOWS_BUILD_DIR)

        upload_files_win = map(
            lambda item: os.path.join(src_path_win, item),
            files_for_upload_win)

        upload_files_linux = map(
            lambda item: os.path.join(self.facts.build_dir_linux, item),
            files_for_upload_linux)

        self.upload_files = (upload_files_win +
                             upload_files_linux +
                             [self.versions_file]
                             )

    def deploy(self):
        if self._checkVersion():
            self._uploadFiles()

    def _checkVersion(self):
        print('Checking versions')
        newOutWikerAppInfo = readAppInfo(self.versions_file)
        print('Download {}'.format(newOutWikerAppInfo.updatesUrl))
        try:
            prevOutWikerAppInfo = downloadAppInfo(newOutWikerAppInfo.updatesUrl)

            if newOutWikerAppInfo.currentVersion < prevOutWikerAppInfo.currentVersion:
                print(Fore.RED + 'Error. New version < Prev version')
                return False
            elif newOutWikerAppInfo.currentVersion == prevOutWikerAppInfo.currentVersion:
                print(Fore.RED + 'Warning: Uploaded the same version')
        except urllib2.HTTPError:
            pass

        return True

    def _uploadFiles(self):
        # Check files for existence
        for fname in self.upload_files:
            if not os.path.exists(fname):
                print(Fore.RED + u'Error. File not found: {}'.format(fname))
                sys.exit(1)

        for fname in self.upload_files:
            with cd(self.deploy_path):
                basename = os.path.basename(fname)
                put(fname, basename)
