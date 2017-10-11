# -*- coding: utf-8 -*-

import os.path

from buildtools.versions import getOutwikerVersionStr, getOutwikerVersion
import defines


class BuildFacts(object):
    def __init__(self):
        # x.x.x.xxx
        self.version = getOutwikerVersionStr()

        # Version tuple ('x.x.x', 'xxx')
        self.version_items = getOutwikerVersion()

        # build/
        self.root_dir = os.path.abspath(defines.BUILD_DIR)

        # build/x.x.x.xxx/
        self.version_dir = os.path.join(self.root_dir, self.version)

        # build/x.x.x.xxx/windows/
        self.build_dir_windows = os.path.join(self.version_dir,
                                              defines.WINDOWS_BUILD_DIR)

        # build/x.x.x.xxx/linux/
        self.build_dir_linux = os.path.join(self.version_dir,
                                            defines.LINUX_BUILD_DIR)

        # build/x.x.x.xxx/versions.xml
        self.versions_file = os.path.join(self.version_dir,
                                          defines.OUTWIKER_VERSIONS_FILENAME)

        # build/tmp/
        self.temp_dir = os.path.join(self.root_dir, u'tmp')

        # need_for_build/
        self.need_for_build = os.path.abspath(defines.NEED_FOR_BUILD_DIR)

        # need_for_build/windows
        self.nfb_win = os.path.join(self.need_for_build, u'windows')

        # need_for_build/linux
        self.nfb_linux = os.path.join(self.need_for_build, u'linux')

        # need_for_build/virtual
        self.nfb_virtual = os.path.join(self.need_for_build, u'virtual')

    def getTempSubpath(self, *args):
        '''
        Return path inside tmp folder
        '''
        return os.path.join(self.temp_dir, *args)
