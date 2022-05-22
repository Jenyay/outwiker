# -*- coding: utf-8 -*-

import os

from invoke import Context

from .base import BuilderBase
from buildtools.defines import SOURCES_DIR
from buildtools.utilites import print_info


class BuilderSources(BuilderBase):
    """
    Create archives with sources
    """
    def __init__(self, c: Context, build_dir: str = SOURCES_DIR, is_stable: bool = False):
        super().__init__(c, build_dir, is_stable)

        self._full_archive_name = u"outwiker-src-full-{}".format(
            self.facts.version
        )

        self._min_archive_name = u"outwiker-src-min-{}".format(
            self.facts.version
        )

        if not self.is_stable:
            self._min_archive_name += u'-unstable'

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
        print_info(u'Create full sources archive...')
        self.context.run('git archive --prefix={}/ -o "{}" HEAD'.format(
            self._full_archive_name,
            self._full_archive_path))

        print_info(u'Create minimal sources archive...')
        with self.context.cd(self.temp_sources_dir):
            self.context.run(u'7z a -r -aoa -xr!__pycache__ -xr!*.pyc -xr!.ropeproject -xr!tests.py -xr!profile.py -xr!setup_tests.py -xr!tests_*.py -xr!setup.py -xr!test -xr!profiles "{}" ./*'.format(self._min_archive_path))
