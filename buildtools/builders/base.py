# -*- coding: UTF-8 -*-

import abc
import os
import shutil

from buildtools.defines import BUILD_DIR
from buildtools.buildfacts import BuildFacts


class BuilderBase(object):
    """
    Base class for all builders.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, subdir_name, is_stable=False):
        self.facts = BuildFacts(BUILD_DIR)

        self.build_dir = os.path.join(self.facts.version_dir, subdir_name)
        self.is_stable = is_stable
        # self._root_build_dir = BUILD_DIR
        # self._subdir_name = subdir_name
        # self._build_dir = os.path.join(self._root_build_dir,
        #                                self._subdir_name)

        # version = getOutwikerVersion()
        # self._distrib_dir_name = version[0] + u'.' + version[1]
        #
        # self._distrib_dir = os.path.join(self._root_build_dir,
        #                                  self._distrib_dir_name)

    @abc.abstractmethod
    def _build(self):
        pass

    def _postBuild(self):
        pass

    def clear(self):
        self._remove(self.build_dir)

    def build(self):
        self._createRootDir()
        self.clear()

        self._remove(self.facts.temp_dir)
        os.mkdir(self.facts.temp_dir)

        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

        self._build()
        self._postBuild()

    def _createRootDir(self):
        if not os.path.exists(self.facts.root_dir):
            os.mkdir(self.facts.root_dir)

    def _remove(self, path):
        """
        Remove the fname file if it exists.
        The function not catch any exceptions.
        """
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
