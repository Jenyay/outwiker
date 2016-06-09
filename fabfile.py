#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import shutil
import glob

from fabric.api import local, lcd, settings, task

from buildtools.utilites import (getPython,
                                 execute,
                                 getCurrentUbuntuDistribName,
                                 )
from buildtools.defines import(
    UBUNTU_RELEASE_NAMES,
    BUILD_DIR,
    DEB_SOURCE_BUILD_DIR,
)
from buildtools.versions import getOutwikerVersion
from buildtools.builders import (BuilderBase,
                                 BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins,
                                 BuilderLinuxBinary,
                                 BuilderLinuxDebBinary,
                                 BuilderDebSource,
                                 BuilderDebSourcesIncluded,
                                 )


@task
def deb_sources_included():
    """
    Create files for uploading in PPA(including sources)
    """
    builder = BuilderDebSourcesIncluded(DEB_SOURCE_BUILD_DIR,
                                        UBUNTU_RELEASE_NAMES)
    builder.build()


@task
def deb():
    """
    Assemble the deb packages
    """
    builder = BuilderDebSource(DEB_SOURCE_BUILD_DIR, UBUNTU_RELEASE_NAMES)
    builder.build()


@task
def deb_clear():
    """
    Remove the deb packages
    """
    builder = BuilderDebSource(DEB_SOURCE_BUILD_DIR, UBUNTU_RELEASE_NAMES)
    builder.clear()


@task
def debsingle():
    """
    Assemble the deb package for the current Ubuntu release
    """
    builder = BuilderDebSource(DEB_SOURCE_BUILD_DIR,
                               [getCurrentUbuntuDistribName()])
    builder.build()


@task
def ppaunstable():
    """
    Upload the current OutWiker version in PPA(unstable)
    """
    version = getOutwikerVersion()

    for distname in UBUNTU_RELEASE_NAMES:
        with lcd(os.path.join(BUILD_DIR, DEB_SOURCE_BUILD_DIR)):
            local("dput ppa:outwiker-team/unstable outwiker_{}+{}~{}_source.changes".format(version[0], version[1], distname))


# @task
# def ppastable():
#     """
#     Upload the current OutWiker version in PPA(unstable)
#     """
#     version = getOutwikerVersion()
#
#     for distname in UBUNTU_RELEASE_NAMES:
#         with lcd(os.path.join(BUILD_DIR, DEB_SOURCE_BUILD_DIR)):
#             local("dput ppa:outwiker-team/ppa outwiker_{}+{}~{}_source.changes".format(version[0], version[1], distname))


@task
def plugins():
    """
    Create an archive with plugins(7z required)
    """
    builder = BuilderPlugins()
    builder.build()


@task
def plugins_clear():
    """
    Remove an archive with plugins(7z required)
    """
    builder = BuilderPlugins()
    builder.clear()


@task
def sources():
    """
    Create the sources archives.
    """
    builder = BuilderSources()
    builder.build()


@task
def sources_clear():
    """
    Remove the sources archives.
    """
    builder = BuilderSources()
    builder.clear()


@task
def win(skipinstaller=False, skiparchives=False):
    """
    Build assemblies under Windows
    """
    builder = BuilderWindows(create_installer=not skipinstaller,
                             create_archives=not skiparchives)
    builder.build()


@task
def win_clear():
    """
    Remove assemblies under Windows
    """
    builder = BuilderWindows()
    builder.clear()


@task
def linux(create_archive=True):
    """
    Assemble binary builds for Linux
    """
    builder = BuilderLinuxBinary(create_archive=create_archive)
    builder.build()


@task
def linux_clear():
    """
    Remove binary builds for Linux
    """
    builder = BuilderLinuxBinary()
    builder.clear()


@task
def nextversion():
    """
    Increment a version number(execute under Linux only,
    incremented the deb package version also)
    """
    (version_major, version_build) = getOutwikerVersion()
    version_build = unicode(int(version_build) + 1)

    with lcd(os.path.join(u'need_for_build', u'debian_debsource')):
        local('dch -v "{major}+{build}~{distrib}" -D {distrib}'.format(
            major=version_major,
            build=version_build,
            distrib=getCurrentUbuntuDistribName())
        )


@task
def debinstall():
    """
    Assemble deb package for current Ubuntu release
    """
    debsingle()

    version = getOutwikerVersion()

    with lcd(os.path.join(BUILD_DIR, DEB_SOURCE_BUILD_DIR)):
        local("sudo dpkg -i outwiker_{}+{}~{}_all.deb".format(
            version[0],
            version[1],
            getCurrentUbuntuDistribName()))


@task
def locale():
    """
    Update the localization file(outwiker.pot)
    """
    with lcd("src"):
        local(r'find . -iname "*.py" | xargs xgettext -o locale/outwiker.pot')


@task
def localeplugin(pluginname):
    """
    Create or update the localization file for pluginname plug-in
    """
    with lcd(os.path.join("plugins", pluginname, pluginname)):
        local(r'find . -iname "*.py" | xargs xgettext -o locale/{}.pot'.format(pluginname))


@task
def run():
    """
    Run OutWiker from sources
    """
    with lcd("src"):
        execute(u'{} runoutwiker.py'.format(getPython()))


@task
def test(section=u'', *args):
    """
    Run the unit tests
    """
    testdir = u'src'
    files = [fname[len(testdir) + 1:]
             for fname
             in glob.glob(u'{}/tests_*.py'.format(testdir))]
    files.sort()

    with lcd("src"):
        if section:
            execute("{} tests_{}.py {}".format(getPython(),
                                               section,
                                               u' '.join(args)))
        else:
            with settings(warn_only=True):
                for fname in files:
                    execute("{} {}".format(getPython(),
                                           fname,
                                           u' '.join(args)))


@task
def deb_binary():
    builder = BuilderLinuxDebBinary()
    builder.build()


@task
def deb_binary_clear():
    builder = BuilderLinuxDebBinary()
    builder.clear()


@task
def clear():
    plugins_clear()
    sources_clear()

    if os.name == 'posix':
        linux_clear()
        deb_clear()
        deb_binary_clear()
    elif os.name == 'nt':
        win_clear()
