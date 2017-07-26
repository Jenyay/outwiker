# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import shutil

from fabric.api import local, lcd

from ..base import BuilderBase
from ..binarybuilders import PyInstallerBuilderLinux
from buildtools.defines import (DEB_BINARY_BUILD_DIR,
                                NEED_FOR_BUILD_DIR,
                                # TIMEZONE,
                                # DEB_MAINTAINER,
                                # DEB_MAINTAINER_EMAIL
                                )
# from buildtools.contentgenerators import DebChangelogGenerator
from buildtools.versions import getOutwikerVersion


class BuilderDebBinaryFactory(object):
    '''
    Class to get necessary builder for deb binary.
    '''
    @staticmethod
    def get_default(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinaryFactory.get_usr(dir_name, is_stable)

    @staticmethod
    def get_usr(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinary(dir_name, is_stable)

    @staticmethod
    def get_opt(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinaryOpt(dir_name, is_stable)


class BuilderDebBinaryBase(BuilderBase):
    __metaclass__ = ABCMeta

    def __init__(self, dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        super(BuilderDebBinaryBase, self).__init__(dir_name, is_stable)
        version = getOutwikerVersion()
        architecture = self._getDebArchitecture()
        self.debName = "outwiker-{}+{}_{}".format(version[0],
                                                  version[1],
                                                  architecture)

        # tmp/outwiker-x.x.x+xxx_.../
        self.debPath = self.facts.getTempSubpath(self.debName)
        self.debFileName = u'{}.deb'.format(self.debName)

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
        return self.facts.getTempSubpath(self.debName, u'DEBIAN')

    def _copyDebianFiles(self):
        '''
        Copy files to tmp/outwiker-x.x.x+xxx_architecture/DEBIAN
        '''
        debian_src_dir = os.path.join(NEED_FOR_BUILD_DIR,
                                      u'debian_debbinary',
                                      u'debian')

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
        result = local(u'dpkg --print-architecture', capture=True)
        result = u''.join(result)
        return result.strip()

    def _buildDeb(self):
        with lcd(self.facts.temp_dir):
            local(u'fakeroot dpkg-deb --build {}'.format(self.debName))

        shutil.move(self.facts.getTempSubpath(self.debFileName),
                    os.path.join(self.build_dir, self.debFileName))

        with lcd(self.build_dir):
            local(u'lintian {}.deb'.format(self.debName))

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

        DEBIAN_dir = self._getDEBIANPath()

        os.chmod(os.path.join(DEBIAN_dir, u'postinst'), 0o755)
        os.chmod(os.path.join(DEBIAN_dir, u'postrm'), 0o755)
        os.chmod(os.path.join(self.debPath, u'usr', u'bin', u'outwiker'),
                 0o755)

    def _buildBinaries(self):
        dest_dir = self._getExecutableDir()

        src_dir = self.temp_sources_dir
        temp_dir = self.facts.temp_dir

        linuxBuilder = PyInstallerBuilderLinux(src_dir,
                                               dest_dir,
                                               temp_dir)
        linuxBuilder.build()
        self._remove(os.path.join(dest_dir, u'LICENSE.txt'))

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

        # Archive the changelog to usr/share/doc
        with lcd(doc_dir):
            local(u'gzip --best -n -c changelog > changelog.Debian.gz')
            local(u'rm changelog')

    def _build(self):
        self._buildBinaries()
        self._copyDebianFiles()
        self._copy_share_files()
        self._createFoldersTree()
        self._create_bin_file()
        self._create_changelog()
        self._setPermissions()
        self._buildDeb()


class BuilderDebBinary(BuilderDebBinaryBase):
    '''
    Class to create deb package from which will be installed to /usr/ folder
    '''
    def _getExecutableDirShort(self):
        return u'usr/lib/outwiker'

    def _createFoldersTree(self):
        '''
        Create folders tree inside tmp/outwiker-x.x.x+xxx_.../
        and copy files to it.
        '''
        dir_names = [u'help',
                     u'iconset',
                     u'images',
                     u'locale',
                     u'spell',
                     u'styles']

        share_dir = os.path.join(self.debPath, u'usr', u'share', u'outwiker')
        os.makedirs(share_dir)

        exec_dir = self._getExecutableDir()

        for dir_name in dir_names:
            src_dir = os.path.join(exec_dir, dir_name)
            dst_dir = os.path.join(share_dir, dir_name)
            shutil.move(src_dir, dst_dir)
            with lcd(self.debPath):
                local(u'ln -s ../../share/outwiker/{dirname} usr/lib/outwiker'.format(dirname=dir_name))


class BuilderDebBinaryOpt(BuilderDebBinaryBase):
    '''
    Class to create deb package from which will be installed to /opt/ folder
    '''
    def _getExecutableDirShort(self):
        return u'opt/outwiker'
