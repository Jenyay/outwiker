# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import glob
import os
import shutil

from invoke import Context

from ..base import BuilderBase
from ..binarybuilders import PyInstallerBuilderLinuxBase
from buildtools.defines import (DEB_BINARY_BUILD_DIR,
                                NEED_FOR_BUILD_DIR,
                                PLUGINS_DIR,
                                )
from buildtools.versions import getOutwikerVersion
from ...utilites import get_linux_distrib_info


class PyInstallerBuilderLinuxForDeb(PyInstallerBuilderLinuxBase):
    pass


class BuilderDebBinaryFactory(object):
    '''
    Class to get necessary builder for deb binary.
    '''
    @staticmethod
    def get_default(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinaryFactory.get_opt(dir_name, is_stable)

    @staticmethod
    def get_opt(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinaryOpt(dir_name, is_stable)


class BuilderDebBinaryBase(BuilderBase, metaclass=ABCMeta):
    def __init__(self, dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        super().__init__(dir_name, is_stable)
        version = getOutwikerVersion()
        architecture = self._getDebArchitecture()
        self.debName = "outwiker-{version}+{build}_{architecture}".format(
            version=version[0],
            build=version[1],
            architecture=architecture)

        # tmp/outwiker-x.x.x+xxx_.../
        self.debPath = self.facts.getTempSubpath(self.debName)
        self.debFileName = u'{}.deb'.format(self.debName)
        self.pluginsDir = os.path.join(self._getExecutableDir(),
                                       PLUGINS_DIR)

        self._files_to_remove = [
            'LICENSE.txt',
        ]

    def _getExecutableDir(self):
        return os.path.join(self.facts.temp_dir,
                            self.debName,
                            self._getExecutableDirShort())

    @abstractmethod
    def _getExecutableDirShort(self):
        pass

    def _createFoldersTree(self):
        '''
        Create folders tree inside tmp/outwiker-x.x.x+xxx_.../
        and copy files to it.
        '''
        pass

    def clear(self):
        self._remove(os.path.join(self.build_dir, self.debFileName))

    def _getDEBIANPath(self):
        return self.facts.getTempSubpath(self.debName, 'DEBIAN')

    def _copyDebianFiles(self):
        '''
        Copy files to tmp/outwiker-x.x.x+xxx_architecture/DEBIAN
        '''
        debian_src_dir = os.path.join(NEED_FOR_BUILD_DIR,
                                      'debian_debbinary',
                                      'debian')

        debian_dest_dir = self._getDEBIANPath()
        shutil.copytree(debian_src_dir, debian_dest_dir)
        self._create_control_file(debian_dest_dir)

    def _create_control_file(self, debian_dir):
        '''
        Create DEBIAN/control file from template (insert version number)
        '''
        version = getOutwikerVersion()
        template_file = os.path.join(debian_dir, 'control.tpl')

        with open(template_file) as fp:
            template = fp.read()

        control_text = template.replace('{{version}}', version[0])
        control_text = control_text.replace('{{build}}', version[1])

        with open(os.path.join(debian_dir, 'control'), 'w') as fp:
            fp.write(control_text)

        os.remove(template_file)

    def _getDebArchitecture(self):
        result = self.context.run('dpkg --print-architecture', capture=True)
        result = u''.join(result)
        return result.strip()

    def _buildDeb(self):
        with self.context.cd(self.facts.temp_dir):
            self.context.run('fakeroot dpkg-deb --build {}'.format(self.debName))

        shutil.move(self.facts.getTempSubpath(self.debFileName),
                    os.path.join(self.build_dir, self.debFileName))

    def _checkLintian(self):
        # with settings(warn_only=True):
        with self.context.cd(self.build_dir):
            self.context.run('lintian --no-tag-display-limit {}.deb'.format(self.debName))

    def _setPermissions(self):
        for par, dirs, files in os.walk(self.debPath):
            for d in dirs:
                try:
                    os.chmod(os.path.join(par, d), 0o755)
                except OSError:
                    continue
            for f in files:
                try:
                    os.chmod(os.path.join(par, f), 0o644)
                except OSError:
                    continue

        exe_dir = self._getExecutableDir()
        os.chmod(os.path.join(self.build_dir,
                              exe_dir,
                              u'outwiker'), 0o755)

        os.chmod(os.path.join(self.debPath, u'usr', u'bin', u'outwiker'),
                 0o755)

    def _buildBinaries(self):
        dest_dir = self._getExecutableDir()

        src_dir = self.temp_sources_dir
        temp_dir = self.facts.temp_dir

        linuxBuilder = PyInstallerBuilderLinuxForDeb(src_dir,
                                                     dest_dir,
                                                     temp_dir)
        linuxBuilder.build()

        for fname in self._files_to_remove:
            self._remove(os.path.join(dest_dir, fname))

    def _create_bin_file(self):
        '''
        Create executable file in usr/bin
        '''
        bin_path = os.path.join(self.debPath, u'usr', u'bin')
        if not os.path.exists(bin_path):
            os.mkdir(bin_path)

        text = u'''#!/bin/sh
/{}/outwiker "$@"'''.format(self._getExecutableDirShort())

        bin_file = os.path.join(bin_path, u'outwiker')
        with open(bin_file, 'w') as fp:
            fp.write(text)

        os.chmod(bin_file, 0o755)

    def _copy_share_files(self):
        """
        Copy files to tmp/outwiker-x.x.x+xxx_architecture/usr/bin and
        tmp/outwiker-x.x.x+xxx_architecture/usr/share
        """
        dest_usr_dir = os.path.join(self.debPath, u'usr')
        dest_share_dir = os.path.join(dest_usr_dir, u'share')

        root_dir = os.path.join(NEED_FOR_BUILD_DIR,
                                u'debian_debbinary',
                                u'root')
        shutil.copytree(os.path.join(root_dir, u'usr', u'share'),
                        dest_share_dir)

    def _create_changelog(self):
        doc_dir = os.path.join(self.debPath,
                               u'usr', u'share', u'doc',
                               u'outwiker')

        # Create empty changelog
        # TODO: Generate changelog with
        # buildtools.contentgenerators.DebChangelogGenerator
        with open(os.path.join(doc_dir, u'changelog'), "w"):
            pass

        # Archive the changelog to usr/share/doc/outwiker
        with self.context.cd(doc_dir):
            self.context.run(u'gzip --best -n -c changelog > changelog.gz')
            self.context.run(u'rm changelog')

    def _build(self):
        self._create_plugins_dir()
        self._buildBinaries()
        self._copy_plugins(self.pluginsDir)
        self._copyDebianFiles()
        self._copy_share_files()
        self._createFoldersTree()
        self._create_bin_file()
        self._create_changelog()
        self._setPermissions()
        self._buildDeb()
        self._checkLintian()

    def get_deb_files(self):
        result_files = []

        for fname in glob.glob(os.path.join(self.facts.build_dir_linux,
                                            '*.deb')):
            result_files.append(fname)

        return result_files


class BuilderDebBinaryOpt(BuilderDebBinaryBase):
    '''
    Class to create deb package from which will be installed to /opt/ folder
    '''
    def _getExecutableDirShort(self):
        return 'opt/outwiker'
