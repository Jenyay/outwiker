# -*- coding: utf-8 -*-

import abc
import os
import shutil

from buildtools.defines import OUTWIKER_VERSIONS_FILENAME
from buildtools.buildfacts import BuildFacts
from buildtools.utilites import print_info


class BuilderBase(object, metaclass=abc.ABCMeta):
    """
    Base class for all builders.
    """

    def __init__(self, subdir_name, is_stable=False):
        self.is_stable = is_stable

        self.facts = BuildFacts()
        self.build_dir = os.path.join(self.facts.version_dir, subdir_name)
        self.temp_sources_dir = os.path.join(self.facts.temp_dir, u'src')

    @abc.abstractmethod
    def _build(self):
        pass

    def _postBuild(self):
        pass

    def _getBuildReturnValue(self):
        return None

    def clear(self):
        self._remove(self.build_dir)

    def build(self):
        self._createRootDir()
        print_info(u'Clearing...')
        self.clear()

        self._remove(self.facts.temp_dir)
        os.mkdir(self.facts.temp_dir)

        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

        self._copy_sources_to_temp()
        self._copy_versions_file()

        print_info(u'Build to {}'.format(self.build_dir))
        self._build()
        self._postBuild()
        return self._getBuildReturnValue()

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

    def _copy_sources_to_temp(self):
        print_info(u'Copy sources to {}...'.format(self.temp_sources_dir))
        shutil.copytree(u'src',
                        self.temp_sources_dir,
                        ignore=shutil.ignore_patterns('__pycache__',
                                                      '.pytest_cache'))

    def _clear_sources(self):
        '''
        Remove tests and dev scripts from sources
        '''
        root = self.temp_sources_dir
        shutil.rmtree(os.path.join(root, 'test'))
        shutil.rmtree(os.path.join(root, 'profiles'))

        try:
            os.remove(os.path.join(root, '.coverage'))
        except IOError:
            pass

        os.remove(os.path.join(root, 'profile.py'))
        os.remove(os.path.join(root, 'runtests.py'))
        os.remove(os.path.join(root, '__init__.py'))

    def _copy_versions_file(self):
        src_versions_name = (u'versions_stable.xml'
                             if self.is_stable
                             else OUTWIKER_VERSIONS_FILENAME)

        shutil.copy(
            os.path.join(u'src', src_versions_name),
            self.facts.versions_file)

        shutil.copy(
            os.path.join(u'src', src_versions_name),
            os.path.join(self.temp_sources_dir, OUTWIKER_VERSIONS_FILENAME))

        os.remove(os.path.join(self.temp_sources_dir, u'versions_stable.xml'))

    def _create_plugins_dir(self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join(self.temp_sources_dir, u"plugins")

        # Create the plugins folder(it is not appened to the git repository)
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)
