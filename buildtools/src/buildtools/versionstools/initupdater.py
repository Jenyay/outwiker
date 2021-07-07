# -*- coding: utf-8 -*-

from typing import List

from buildtools.buildfacts import BuildFacts


class InitUpdater:
    """Add / edit __init__.py file to version update"""

    def __init__(self):
        self._facts = BuildFacts()

    def set_version(self, version: List[int], status: str = ''):
        pass
