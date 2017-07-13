# -*- coding: UTF-8 -*-

import os
import shutil

from fabric.api import local, lcd

from ..base import BuilderBase
from ..linuxbinary import BuilderLinuxBinary
from buildtools.defines import DEB_BINARY_BUILD_DIR
from buildtools.versions import getOutwikerVersion


class BuilderLinuxDebBinary(BuilderBase):
    def __init__(self, subdir_name=DEB_BINARY_BUILD_DIR):
        super(BuilderLinuxDebBinary, self).__init__(subdir_name)
        version = getOutwikerVersion()
        self._architecture = self._getDebArchitecture()
        self._debName = "outwiker-{}+{}_{}".format(version[0],
                                                   version[1],
                                                   self._architecture)

    def clear(self):
        super(BuilderLinuxDebBinary, self).clear()
        deb_result_filename = self._getDebFileName()
        self._remove(os.path.join(self._root_build_dir, deb_result_filename))

    def _build(self):
        self._buildBinaries()
        self._copyDebianFiles()
        self._copy_usr_files(self._getSubpath(self._debName))
        self._move_to_share(self._getSubpath(self._debName))
        self._setPermissions()
        self._buildDeb()

    def _buildBinaries(self):
        dest_subdir = self._getExecutableDir()

        dest_dir = os.path.join(self._root_build_dir, dest_subdir)
        os.makedirs(self._getSubpath(self._debName, u'usr', u'lib'))

        linuxBuilder = BuilderLinuxBinary(dest_subdir, create_archive=False)
        linuxBuilder.build()
        self._remove(os.path.join(dest_dir, u'LICENSE.txt'))

    def _getDEBIANPath(self):
        return self._getSubpath(self._debName, u'DEBIAN')

    def _getExecutableDir(self):
        return os.path.join(self._subdir_name,
                            self._debName,
                            u'usr',
                            u'lib',
                            u'outwiker')

    def _copyDebianFiles(self):
        debian_src_dir = os.path.join(u'need_for_build',
                                      u'debian_debbinary',
                                      u'debian')

        debian_dest_dir = self._getDEBIANPath()
        shutil.copytree(debian_src_dir, debian_dest_dir)

    def _setPermissions(self):
        for par, dirs, files in os.walk(self._getSubpath(self._debName)):
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
        os.chmod(os.path.join(self._root_build_dir,
                              exe_dir,
                              u'outwiker'), 0o755)

        DEBIAN_dir = self._getDEBIANPath()

        os.chmod(os.path.join(DEBIAN_dir, u'postinst'), 0o755)
        os.chmod(os.path.join(DEBIAN_dir, u'postrm'), 0o755)
        os.chmod(os.path.join(self._build_dir,
                              self._debName,
                              u'usr',
                              u'bin',
                              u'outwiker'), 0o755)

    def _buildDeb(self):
        with lcd(self._build_dir):
            local(u'fakeroot dpkg-deb --build {}'.format(self._debName))

        deb_filename = self._getDebFileName()
        shutil.move(self._getSubpath(deb_filename),
                    os.path.join(self._root_build_dir, deb_filename))

        with lcd(self._root_build_dir):
            local(u'lintian {}.deb'.format(self._debName))

    def _move_to_share(self, destdir):
        """Move images, help etc to /usr/share folder."""
        dir_names = [u'help',
                     u'iconset',
                     u'images',
                     u'locale',
                     u'spell',
                     u'styles']

        share_dir = os.path.join(destdir, u'usr', u'share', u'outwiker')
        os.makedirs(share_dir)

        for dir_name in dir_names:
            src_dir = os.path.join(destdir,
                                   u'usr',
                                   u'lib',
                                   u'outwiker',
                                   dir_name)
            dst_dir = os.path.join(share_dir, dir_name)
            shutil.move(src_dir, dst_dir)
            with lcd(destdir):
                local(u'ln -s ../../share/outwiker/{dirname} usr/lib/outwiker'.format(dirname=dir_name))

    def _copy_usr_files(self, destdir):
        """Copy icons files for deb package"""
        dest_usr_dir = os.path.join(destdir, u'usr')
        dest_share_dir = os.path.join(dest_usr_dir, u'share')
        dest_bin_dir = os.path.join(dest_usr_dir, u'bin')

        root_dir = os.path.join(u'need_for_build',
                                u'debian_debbinary',
                                u'root')
        shutil.copytree(os.path.join(root_dir, u'usr', u'share'),
                        dest_share_dir)
        shutil.copytree(os.path.join(root_dir, u'usr', u'bin'),
                        dest_bin_dir)

        dest_doc_dir = os.path.join(dest_share_dir,
                                    u'doc',
                                    u'outwiker')

        shutil.copyfile(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     u'debian',
                                     u'changelog'),
                        os.path.join(dest_doc_dir, u'changelog'))
        with lcd(dest_doc_dir):
            local(u'gzip --best -n -c changelog > changelog.Debian.gz')
            local(u'rm changelog')

    def _getDebArchitecture(self):
        result = local(u'dpkg --print-architecture', capture=True)
        result = u''.join(result)
        return result.strip()

    def _getDebFileName(self):
        '''
        Return file name for deb package(file name only, not path)
        '''
        return u'{}.deb'.format(self._debName)
