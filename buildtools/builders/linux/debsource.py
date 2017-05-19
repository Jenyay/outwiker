# -*- coding: UTF-8 -*-

import os
import shutil
import datetime

from fabric.api import local, lcd

from ..base import BuilderBase
from buildtools.versions import getOutwikerVersion, getOutwikerAppInfo
from buildtools.contentgenerators import DebChangelogGenerator
from buildtools.defines import (TIMEZONE,
                                DEB_MAINTAINER,
                                DEB_MAINTAINER_EMAIL,
                                )
from outwiker.utilites.textfile import writeTextFile


class BuilderBaseDebSource(BuilderBase):
    """
    The base class for source deb packages assebbling.
    """
    def __init__(self, subdir_name, is_stable):
        super(BuilderBaseDebSource, self).__init__(subdir_name, is_stable)

    def clear(self):
        super(BuilderBaseDebSource, self).clear()
        self._remove(self.getResultPath())

    def _debuild(self, command, distriblist):
        """
        Run command with debuild.
        The function assembles the deb packages for all releases in distriblist
        """
        date = datetime.datetime.now()
        date_str = date.strftime(u'%a, %d %b %Y %H:%M:%S ' + TIMEZONE)
        outwiker_appinfo = getOutwikerAppInfo()
        changelog_generator = DebChangelogGenerator(outwiker_appinfo,
                                                    DEB_MAINTAINER,
                                                    DEB_MAINTAINER_EMAIL)

        for distrib_name in distriblist:
            self._orig(distrib_name)
            changelog = changelog_generator.make(distrib_name, date_str)
            current_debian_dirname = os.path.join(self.build_dir,
                                                  self._getDebName(),
                                                  'debian')

            # Change release name in the changelog file
            changelog_path = os.path.join(current_debian_dirname,
                                          u'changelog')
            writeTextFile(changelog_path, changelog)

            with lcd(current_debian_dirname):
                local(command)

    def _postBuild(self):
        src_dir = self.build_dir
        dest_dir = self.getResultPath()
        shutil.move(src_dir, dest_dir)

        # Remove temp files
        self._remove(os.path.join(dest_dir, self._getDebName()))

    def getResultPath(self):
        return self.build_dir

    def _orig(self, distname):
        """
        Create an archive for "original" sources for building the deb package
        distname - Ubuntu release name
        """
        self._source(distname)

        origname = self._getOrigName(distname)

        with lcd(self.build_dir):
            local("tar -cvf {} {}".format(origname, self._getDebName()))

        orig_dirname = os.path.join(self.build_dir, origname)
        local("gzip -f {}".format(orig_dirname))

    def _source(self, distname):
        """
        Create a sources folder for building the deb package
        """
        self._debclean()

        dirname = os.path.join(self.build_dir, self._getDebName())
        os.makedirs(dirname)

        temp_images_dir = os.path.join(self.facts.temp_dir, u'images')
        if os.path.exists(temp_images_dir):
            shutil.rmtree(temp_images_dir)

        shutil.copy(u'copyright.txt', dirname)
        shutil.copy(u'README', dirname)
        shutil.copytree(u'images', temp_images_dir)

        shutil.copytree(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     distname,
                                     u'debian'),
                        os.path.join(dirname, u'debian'))

        shutil.copy(os.path.join(u'need_for_build',
                                 u'debian_debsource',
                                 distname,
                                 u'Makefile'),
                    dirname)

        shutil.copy(os.path.join(u'need_for_build',
                                 u'debian_debsource',
                                 distname,
                                 u'outwiker.desktop'),
                    dirname)

        shutil.copy(os.path.join(u'need_for_build',
                                 u'debian_debsource',
                                 distname,
                                 u'outwiker'),
                    dirname)

        shutil.copytree(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     distname,
                                     u'man'),
                        os.path.join(dirname, u'man'))

        excludes = [
            u'build',
            u'*.pyc',
            u'*.dll',
            u'*.exe',
            u'src/.ropeproject',
            u'src/test',
            u'src/setup.py',
            u'src/setup_tests.py',
            u'src/tests_*',
            u'src/profile.py',
            u'src/profiles',
            u'doc',
            u'plugins',
            u'profiles',
            u'test',
            u'outwiker_setup.iss',
            u'need_for_build',
            u'buildtools',
            u'test_*',
            u'images/datagraph',
            u'images/old',
            u'images/outwiker_new_year_*',
        ]
        excludes_param = reduce(lambda x, y: x + u' --exclude={}'.format(y),
                                excludes,
                                u'')

        command = "rsync -avz * {excludes} {dirname}/".format(
            dirname=dirname,
            excludes=excludes_param)

        with lcd(self.facts.temp_dir):
            local(command)

    def _debclean(self):
        """
        Clean build/<distversion> folder
        """
        dirname = os.path.join(self.build_dir, self._getDebName())
        if os.path.exists(dirname):
            shutil.rmtree(dirname)

    def _getDebName(self):
        """
        Return a folder name for sources for building the deb package
        """
        version = getOutwikerVersion()
        return "outwiker-{}+{}".format(version[0], version[1])

    def _getOrigName(self, distname):
        version = getOutwikerVersion()
        return "outwiker_{}+{}~{}.orig.tar".format(version[0],
                                                   version[1],
                                                   distname)


class BuilderDebSource(BuilderBaseDebSource):
    def __init__(self, subdir_name, release_names, is_stable):
        super(BuilderBaseDebSource, self).__init__(subdir_name, is_stable)
        self._release_names = release_names

    def _build(self):
        self._debuild("debuild --source-option=--include-binaries --source-option=--auto-commit",
                      self._release_names)


class BuilderDebSourcesIncluded(BuilderBaseDebSource):
    def __init__(self, subdir_name, release_names, is_stable):
        super(BuilderDebSourcesIncluded, self).__init__(subdir_name, is_stable)
        self._release_names = release_names

    def _build(self):
        self._debuild("debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit",
                      self._release_names)
