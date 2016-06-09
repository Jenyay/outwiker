# -*- coding: UTF-8 -*-

import abc
import os
import shutil

from buildtools.defines import BUILD_DIR


class BuilderBase(object):
    """
    Base class for all builders.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, subdir_name):
        self._root_build_dir = BUILD_DIR
        self._subdir_name = subdir_name
        self._build_dir = os.path.join(self._root_build_dir,
                                       self._subdir_name)

    @abc.abstractmethod
    def _build(self):
        pass

    def clear(self):
        self._remove(self._build_dir)

    def build(self):
        self._createRootDir()
        self.clear()
        os.mkdir(self._build_dir)

        self._build()

    def _createRootDir(self):
        if not os.path.exists(self._root_build_dir):
            os.mkdir(self._root_build_dir)

    def _getSubpath(self, *args):
        """
        Return subpath inside current build path(inside 'build' subpath)
        """
        return os.path.join(self._build_dir, *args)

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
