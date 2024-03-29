# -*- coding: utf-8 -*-

import abc
import os
import shutil

from invoke import Context

from buildtools.defines import PLUGINS_LIST
from buildtools.buildfacts import BuildFacts
from buildtools.utilites import print_info


class BuilderBase(metaclass=abc.ABCMeta):
    """
    Base class for all builders.
    """

    def __init__(self, c: Context, subdir_name, is_stable=False):
        self.context = c
        self.is_stable = is_stable

        self.facts = BuildFacts()
        self.build_dir = os.path.join(self.facts.version_dir, subdir_name)
        self.temp_sources_dir = os.path.join(self.facts.temp_dir, 'src')

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
        print_info('Clearing...')
        self.clear()

        self._remove(self.facts.temp_dir)
        os.mkdir(self.facts.temp_dir)

        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

        self._copy_sources_to_temp()

        print_info('Build to {}'.format(self.build_dir))
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
        print_info('Copy sources to {}...'.format(self.temp_sources_dir))
        shutil.copytree('src',
                        self.temp_sources_dir,
                        ignore=shutil.ignore_patterns('__pycache__',
                                                      '.pytest_cache',
                                                      '.mypy_cache',
                                                      'OutWiker.egg-info',
                                                      'outwiker.egg-info',
                                                      'tests'))

    def _clear_sources(self):
        '''
        Remove tests and dev scripts from sources
        '''

    def _create_plugins_dir(self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join(self.temp_sources_dir, 'plugins')

        # Create the plugins folder(it is not appened to the git repository)
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)

        return pluginsdir

    def _copy_plugins(self, plugins_dir):
        print_info('Copy plugins:')
        if not os.path.exists(plugins_dir):
            os.mkdir(plugins_dir)

        for plugin_name in PLUGINS_LIST:
            print_info('    {}'.format(plugin_name))

            src_dir = os.path.join(self.facts.src_plugins_dir,
                                   plugin_name,
                                   plugin_name)
            shutil.copytree(src_dir,
                            os.path.join(plugins_dir, plugin_name),
                            ignore=shutil.ignore_patterns('__pycache__',
                                                          '.mypy_cache'))
