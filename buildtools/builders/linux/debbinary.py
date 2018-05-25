# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import shutil

from fabric.api import local, lcd, settings

from ..base import BuilderBase
from ..binarybuilders import PyInstallerBuilderLinuxBase
from buildtools.defines import (DEB_BINARY_BUILD_DIR,
                                NEED_FOR_BUILD_DIR,
                                )
from buildtools.versions import getOutwikerVersion
from ...utilites import get_linux_distrib_info


class PyInstallerBuilderLinuxForDeb(PyInstallerBuilderLinuxBase):
    pass
    # def get_additional_files(self):
    #     files = []
    #     self._append_pixbuf_files(files)
    #     self._append_immodules_files(files)
    #     return files
    #
    # def _append_immodules_files(self, files):
    #     dir_dest = u'lib/immodules'
    #     modules_dir = u'/usr/lib/x86_64-linux-gnu/gtk-3.0/3.0.0/immodules/'
    #
    #     files.append(('need_for_build/debian_debbinary/immodules.cache', dir_dest))
    #     self.append_so_files(files, modules_dir, dir_dest)
    #
    # def _append_pixbuf_files(self, files):
    #     dir_dest = u'lib/gdk-pixbuf'
    #     modules_dir = u'/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders'
    #
    #     files.append(('need_for_build/debian_debbinary/loaders.cache', dir_dest))
    #     self.append_so_files(files, modules_dir, dir_dest)
    #
    # def get_params(self):
    #     params = super().get_params()
    #     params.append(u'--runtime-hook=linux_runtime_hook.py')
    #     return params


class BuilderDebBinaryFactory(object):
    '''
    Class to get necessary builder for deb binary.
    '''
    @staticmethod
    def get_default(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinaryFactory.get_opt(dir_name, is_stable)

    # @staticmethod
    # def get_usr(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
    #     return BuilderDebBinary(dir_name, is_stable)

    @staticmethod
    def get_opt(dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        return BuilderDebBinaryOpt(dir_name, is_stable)


class BuilderDebBinaryBase(BuilderBase, metaclass=ABCMeta):
    def __init__(self, dir_name=DEB_BINARY_BUILD_DIR, is_stable=False):
        super(BuilderDebBinaryBase, self).__init__(dir_name, is_stable)
        distrib_info = get_linux_distrib_info()
        version = getOutwikerVersion()
        architecture = self._getDebArchitecture()
        self.debName = "outwiker-{version}+{build}_{architecture}".format(
            version=version[0],
            build=version[1],
            distrib=distrib_info['DISTRIB_ID'],
            codename=distrib_info['DISTRIB_CODENAME'],
            architecture=architecture)

        # tmp/outwiker-x.x.x+xxx_.../
        self.debPath = self.facts.getTempSubpath(self.debName)
        self.debFileName = u'{}.deb'.format(self.debName)

        self._files_to_remove = [
            u'LICENSE.txt',
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

    def _checkLintian(self):
        with settings(warn_only=True):
            with lcd(self.build_dir):
                local(u'lintian --no-tag-display-limit {}.deb'.format(self.debName))

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
        with lcd(doc_dir):
            local(u'gzip --best -n -c changelog > changelog.gz')
            local(u'rm changelog')

    def _build(self):
        self._create_plugins_dir()
        self._buildBinaries()
        self._copyDebianFiles()
        self._copy_share_files()
        self._createFoldersTree()
        self._create_bin_file()
        self._create_changelog()
        self._setPermissions()
        self._buildDeb()
        self._checkLintian()


# class BuilderDebBinary(BuilderDebBinaryBase):
#     '''
#     Class to create deb package from which will be installed to /usr/ folder
#     '''
#     def _getExecutableDirShort(self):
#         return u'usr/lib/outwiker'
#
#     def _createFoldersTree(self):
#         '''
#         Create folders tree inside tmp/outwiker-x.x.x+xxx_.../
#         and copy files to it.
#         '''
#         dir_names = [u'help',
#                      u'iconset',
#                      u'images',
#                      u'locale',
#                      u'spell',
#                      u'styles']
#
#         share_dir = os.path.join(self.debPath, u'usr', u'share', u'outwiker')
#         os.makedirs(share_dir)
#
#         exec_dir = self._getExecutableDir()
#
#         for dir_name in dir_names:
#             src_dir = os.path.join(exec_dir, dir_name)
#             dst_dir = os.path.join(share_dir, dir_name)
#             shutil.move(src_dir, dst_dir)
#             with lcd(self.debPath):
#                 local(u'ln -s ../../share/outwiker/{dirname} usr/lib/outwiker'.format(dirname=dir_name))
#

class BuilderDebBinaryOpt(BuilderDebBinaryBase):
    '''
    Class to create deb package from which will be installed to /opt/ folder
    '''
    def _getExecutableDirShort(self):
        return u'opt/outwiker'
