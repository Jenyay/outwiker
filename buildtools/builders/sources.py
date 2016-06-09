# -*- coding: UTF-8 -*-

import os

from fabric.api import local, lcd

from .base import BuilderBase
from buildtools.defines import SOURCES_DIR
from buildtools.versions import getOutwikerVersion


class BuilderSources(BuilderBase):
    """
    Create archives with sources
    """
    def __init__(self, build_dir=SOURCES_DIR):
        super(BuilderSources, self).__init__(build_dir)
        self._fullfname = os.path.join(self._root_build_dir,
                                       u"outwiker-src-full.zip")
        self._minfname = os.path.join(self._root_build_dir,
                                      u"outwiker-src-min.zip")

    def clear(self):
        super(BuilderSources, self).clear()
        self._remove(self._fullfname)
        self._remove(self._minfname)

    def _build(self):
        version = getOutwikerVersion()

        local('git archive --prefix=outwiker-{}.{}/ -o "{}" HEAD'.format(
            version[0],
            version[1],
            self._fullfname))

        with lcd("src"):
            local("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -xr!tests.py -xr!profile.py -xr!setup_tests.py -xr!tests_*.py -xr!setup.py -xr!test -xr!profiles ../{} ./*".format(self._minfname))

        self._remove(self._build_dir)
