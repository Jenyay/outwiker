# -*- coding: UTF-8 -*-

import os
import shutil
import datetime

from fabric.api import local, lcd

from ..base import BuilderBase
from buildtools.versions import getOutwikerVersion, getOutwikerAppInfo
from buildtools.utilites import getCurrentUbuntuDistribName
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
    def __init__(self, subdir_name):
        super(BuilderBaseDebSource, self).__init__(subdir_name)

    def _debuild(self, command, distriblist):
        """
        Run command with debuild.
        The function assembles the deb packages for all releases in distriblist
        """
        date = datetime.datetime.now()
        date_str = date.strftime(u'%a, %d %b %Y %H:%M:%S ' + TIMEZONE)
        current_distrib_name = getCurrentUbuntuDistribName()
        outwiker_appinfo = getOutwikerAppInfo()
        changelog_generator = DebChangelogGenerator(outwiker_appinfo,
                                                    DEB_MAINTAINER,
                                                    DEB_MAINTAINER_EMAIL)

        for distrib_name in distriblist:
            self._orig(distrib_name)
            changelog = changelog_generator.make(distrib_name, date_str)
            current_debian_dirname = os.path.join(self._build_dir,
                                                  self._getDebName(),
                                                  'debian')

            # Change release name in the changelog file
            changelog_path = os.path.join(current_debian_dirname,
                                          u'changelog')
            writeTextFile(changelog_path, changelog)

            with lcd(current_debian_dirname):
                local(command)

    def _orig(self, distname):
        """
        Create an archive for "original" sources for building the deb package
        distname - Ubuntu release name
        """
        self._source()

        origname = self._getOrigName(distname)

        with lcd(self._build_dir):
            local("tar -cvf {} {}".format(origname, self._getDebName()))

        orig_dirname = os.path.join(self._build_dir, origname)
        local("gzip -f {}".format(orig_dirname))

    def _source(self):
        """
        Create a sources folder for building the deb package
        """
        self._debclean()

        dirname = self._getSubpath(self._getDebName())
        os.makedirs(dirname)

        local("rsync -avz * --exclude=.bzr --exclude=distrib --exclude=build --exclude=*.pyc --exclude=*.dll --exclude=*.exe --exclude=src/.ropeproject --exclude=src/test --exclude=src/setup.py --exclude=src/setup_tests.py --exclude=src/profile.py --exclude=src/tests.py --exclude=src/Microsoft.VC90.CRT.manifest --exclude=src/profiles --exclude=src/tools --exclude=doc --exclude=plugins --exclude=profiles --exclude=test --exclude=_update_version_bzr.py --exclude=outwiker_setup.iss --exclude=updateversion --exclude=updateversion.py --exclude=debian_tmp --exclude=Makefile_debbinary  --exclude=need_for_build {dirname}/".format(dirname=dirname))

        shutil.copytree(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     u'debian'),
                        os.path.join(dirname, u'debian'))

        shutil.copyfile(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     u'Makefile'),
                        os.path.join(dirname, u'Makefile'))

        shutil.copyfile(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     u'outwiker.desktop'),
                        os.path.join(dirname, u'outwiker.desktop'))

        shutil.copyfile(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     u'outwiker'),
                        os.path.join(dirname, u'outwiker'))

        shutil.copytree(os.path.join(u'need_for_build',
                                     u'debian_debsource',
                                     u'man'),
                        os.path.join(dirname, u'man'))

    def _debclean(self):
        """
        Clean build/<distversion> folder
        """
        dirname = os.path.join(self._build_dir, self._getDebName())
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
    def __init__(self, subdir_name, release_names):
        super(BuilderBaseDebSource, self).__init__(subdir_name)
        self._release_names = release_names

    def _build(self):
        self._debuild("debuild --source-option=--include-binaries --source-option=--auto-commit",
                      self._release_names)


class BuilderDebSourcesIncluded(BuilderBaseDebSource):
    def __init__(self, subdir_name, release_names):
        super(BuilderDebSourcesIncluded, self).__init__(subdir_name)
        self._release_names = release_names

    def _build(self):
        self._debuild("debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit",
                      self._release_names)
