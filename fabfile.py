#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import shutil
import glob

from fabric.api import local, lcd, settings, task

# from buildtools.utilites import addToSysPath
from buildtools.defines import(
    UBUNTU_RELEASE_NAMES,
    BUILD_DIR,
    LINUX_BUILD_DIR,
    DEB_BINARY_BUILD_DIR,
    DEB_SOURCE_BUILD_DIR,
)
from buildtools.versions import getOutwikerVersion
from buildtools.builders import (BuilderBase,
                                 BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins)


class BuilderLinuxBinaryBase(BuilderBase):
    """
    Base class for all Linux binary builders.
    """
    def __init__(self, build_dir, create_archive):
        super(BuilderLinuxBinaryBase, self).__init__(build_dir)

        self._create_archive = create_archive
        self._toRemove = [
            self._getSubpath(u'tcl'),
            self._getSubpath(u'tk'),
            self._getSubpath(u'PyQt4.QtCore.so'),
            self._getSubpath(u'PyQt4.QtGui.so'),
            self._getSubpath(u'_tkinter.so'),
        ]


    def _build_binary(self):
        """
        Build with cx_Freeze
        """
        with lcd("src"):
            local("python setup.py build --build-exe ../{}".format(self._build_dir))

        map(self._remove, self._toRemove)


    def _create_plugins_dir(self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join("src", "plugins")

        # Create the plugins folder(it is not appened to the git repository)
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)


class BuilderLinuxBinary(BuilderLinuxBinaryBase):
    """
    Class for making simple Linux binary build
    """
    def __init__(self, build_dir=LINUX_BUILD_DIR, create_archive=True):
        super(BuilderLinuxBinary, self).__init__(build_dir, create_archive)
        self._archiveFullName = os.path.join(self._root_build_dir,
                                             'outwiker_linux_unstable_x64.7z')


    def _build(self):
        self._create_plugins_dir()
        self._build_binary()

        if self._create_archive:
            self._build_archive()


    def clear(self):
        super(BuilderLinuxBinary, self).clear()
        self._remove(self._archiveFullName)


    def _build_archive(self):
        # Create archive without plugins
        with lcd(self._build_dir):
            local("7z a ../outwiker_linux_unstable_x64.7z ./* ./plugins -r -aoa")



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
        current_distrib_name = _getCurrentUbuntuDistribName()
        for distrib_name in distriblist:
            self._orig(distrib_name)
            current_debian_dirname = os.path.join(self._build_dir,
                                                  self._getDebName(),
                                                  'debian')

            # Change release name in the changelog file
            changelog_path = os.path.join(current_debian_dirname,
                                          u'changelog')
            self._makechangelog(changelog_path,
                                current_distrib_name,
                                distrib_name)

            with lcd(current_debian_dirname):
                local(command)

            # Return the source release name
            self._makechangelog(changelog_path,
                                distrib_name,
                                current_distrib_name)


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


    def _makechangelog(self, changelog_path, distrib_src, distrib_new):
        """
        Update the changelog file for current Ubuntu release.
        """
        with open(changelog_path) as fp:
            lines = fp.readlines()

        lines[0] = lines[0].replace(distrib_src, distrib_new)

        with open(changelog_path, "w") as fp:
            fp.write(u"".join(lines))



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


def _getCurrentUbuntuDistribName():
    with open('/etc/lsb-release') as fp:
        for line in fp:
            line = line.strip()
            if line.startswith(u'DISTRIB_CODENAME'):
                codename = line.split(u'=')[1].strip()
                return codename


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
                               [_getCurrentUbuntuDistribName()])
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
            distrib=_getCurrentUbuntuDistribName())
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
            _getCurrentUbuntuDistribName()))


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
        _run(u'{} runoutwiker.py'.format(_getPython()))


def _getPython():
    if os.name == 'posix':
        return u'python2.7'
    else:
        return u'python'


def _run(command):
    if os.name == 'posix':
        local(u'LD_PRELOAD=libwx_gtk2u_webview-3.0.so.0 ' + command)
    else:
        local(command)


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
            _run("{} tests_{}.py {}".format(_getPython(),
                                            section,
                                            u' '.join(args)))
        else:
            with settings(warn_only=True):
                for fname in files:
                    _run("{} {}".format(_getPython(),
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
    deb_clear()
    linux_clear()
    plugins_clear()
    sources_clear()
    win_clear()
