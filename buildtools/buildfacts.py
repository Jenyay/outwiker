# -*- coding: utf-8 -*-

import os.path

from buildtools.versions import getOutwikerVersion


class BuildFacts(object):
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)

        self.version_items = getOutwikerVersion()
        self.version = self.version_items[0] + u'.' + self.version_items[1]

        self.version_dir = os.path.join(self.root_dir, self.version)

        self.temp_dir = os.path.join(self.root_dir, u'tmp')
