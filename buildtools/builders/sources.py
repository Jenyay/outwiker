# -*- coding: UTF-8 -*-

import os

from fabric.api import local, lcd

from .base import BuilderBase
from buildtools.defines import SOURCES_DIR


class BuilderSources(BuilderBase):
    """
    Create archives with sources
    """
    def __init__(self, build_dir=SOURCES_DIR):
        super(BuilderSources, self).__init__(build_dir)

        self._full_archive_name = u"outwiker-src-full-{}".format(
            self.facts.version
        )

        self._min_archive_name = u"outwiker-src-min-{}".format(
            self.facts.version
        )

        self._full_archive_path = os.path.join(
            self.build_dir,
            self._full_archive_name) + u'.zip'

        self._min_archive_path = os.path.join(
            self.build_dir,
            self._min_archive_name) + u'.zip'

    def clear(self):
        super(BuilderSources, self).clear()
        self._remove(self._full_archive_path)
        self._remove(self._min_archive_path)

    def _build(self):
        local('git archive --prefix={}/ -o "{}" HEAD'.format(
            self._full_archive_name,
            self._full_archive_path))

        with lcd("src"):
            local("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -xr!tests.py -xr!profile.py -xr!setup_tests.py -xr!tests_*.py -xr!setup.py -xr!test -xr!profiles {} ./*".format(self._min_archive_path))
