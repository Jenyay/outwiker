#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import shutil
import glob

from fabric.api import local, lcd, settings

# Supported Ubuntu releases
distribs = ["wily", "trusty"]

# List of the supported plugins
plugins_list = [
    "autorenamer",
    "changepageuid",
    "counter",
    "diagrammer",
    "datagraph",
    "export2html",
    "externaltools",
    "htmlformatter",
    "htmlheads",
    "lightbox",
    "livejournal",
    "pagetypecolor",
    "readingmode",
    "sessions",
    "source",
    "spoiler",
    "statistics",
    "style",
    "thumbgallery",
    "tableofcontents",
    "texequation",
    "updatenotifier",
    "webpage",
]

BUILD_DIR = u'build'
LINUX_BUILD_DIR = u"outwiker_linux"
DEB_BINARY_BUILD_DIR = u'deb_binary'
DEB_SOURCE_BUILD_DIR = u'deb_source'
SOURCES_DIR = u'sources'
PLUGINS_DIR = u'plugins'


def _getVersion():
    """
    Return a tuple: (version number, build number)
    """
    # The file with version number
    fname = u"src/version.txt"

    with open (fname) as fp_in:
        lines = fp_in.readlines()

    return (lines[0].strip(), lines[1].strip())


class BuilderBase (object):
    """
    Base class for all builders.
    """
    __metaclass__ = ABCMeta

    def __init__ (self, subdir_name):
        self._root_build_dir = BUILD_DIR
        self._subdir_name = subdir_name
        self._build_dir = os.path.join (self._root_build_dir, self._subdir_name)


    @abstractmethod
    def _build (self):
        pass


    def clear (self):
        self._remove (self._build_dir)


    def build (self):
        self._createRootDir()
        self.clear()
        os.makedirs (self._build_dir)

        self._build()


    def _createRootDir (self):
        if not os.path.exists (self._root_build_dir):
            os.mkdir (self._root_build_dir)


    def _getSubpath (self, *args):
        """
        Return subpath inside current build path (inside 'build' subpath)
        """
        return os.path.join (self._build_dir, *args)


    def _remove (self, path):
        """
        Remove the fname file if it exists. The function not catch any exceptions.
        """
        if os.path.exists (path):
            if os.path.isfile (path):
                os.remove (path)
            elif os.path.isdir (path):
                shutil.rmtree (path)


    def _getVersion(self):
        """
        Return a tuple: (version number, build number)
        """
        # The file with version number
        fname = u"src/version.txt"

        with open (fname) as fp_in:
            lines = fp_in.readlines()

        return (lines[0].strip(), lines[1].strip())


class BuilderLinuxBinaryBase (BuilderBase):
    """
    Base class for all Linux binary builders.
    """
    def __init__ (self, build_dir, create_archives):
        super (BuilderLinuxBinaryBase, self).__init__ (build_dir)

        self._create_archives = create_archives
        self._toRemove = [
            self._getSubpath (u'tcl'),
            self._getSubpath (u'tk'),
            self._getSubpath (u'PyQt4.QtCore.so'),
            self._getSubpath (u'PyQt4.QtGui.so'),
            self._getSubpath (u'_tkinter.so'),
        ]


    def _build_binary (self):
        """
        Build with cx_Freeze
        """
        with lcd ("src"):
            local ("python setup.py build --build-exe ../{}".format (self._build_dir))

        map (self._remove, self._toRemove)


    def _create_plugins_dir (self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join ("src", "plugins")

        # Create the plugins folder (it is not appened to the git repository)
        if not os.path.exists (pluginsdir):
            os.mkdir (pluginsdir)


class BuilderLinuxBinary (BuilderLinuxBinaryBase):
    """
    Class for making simple Linux binary build
    """
    def __init__ (self, build_dir, create_archives):
        super (BuilderLinuxBinary, self).__init__ (build_dir, create_archives)
        self._archiveFullName = os.path.join (self._root_build_dir,
                                              'outwiker_linux_unstable_x64.7z')


    def _build (self):
        self._create_plugins_dir()
        self._build_binary()

        if self._create_archives:
            self._build_archives()


    def clear (self):
        super (BuilderLinuxBinary, self).clear()
        self._remove (self._archiveFullName)


    def _build_archives (self):
        # Create archive without plugins
        with lcd (self._build_dir):
            local ("7z a ../outwiker_linux_unstable_x64.7z ./* ./plugins -r -aoa")



class BuilderLinuxDebBinary (BuilderBase):
    def __init__ (self, subdir_name):
        super (BuilderLinuxDebBinary, self).__init__ (subdir_name)
        version = self._getVersion()
        self._architecture = self._getDebArchitecture()
        self._debName = "outwiker-{}+{}_{}".format (version[0], version[1], self._architecture)


    def clear (self):
        super (BuilderLinuxDebBinary, self).clear ()
        deb_result_filename = self._getDebFileName()
        self._remove (os.path.join (self._root_build_dir, deb_result_filename))


    def _build (self):
        self._buildBinaries()
        self._copyDebianFiles()
        self._copy_share (self._getSubpath (self._debName))
        self._move_to_share (self._getSubpath (self._debName))
        self._setPermissions()
        self._buildDeb()


    def _buildBinaries (self):
        dest_subdir = self._getExecutableDir()

        dest_dir = os.path.join (self._root_build_dir, dest_subdir)

        linuxBuilder = BuilderLinuxBinary (dest_subdir, create_archives=False)
        linuxBuilder.build()
        self._remove (os.path.join (dest_dir, u'LICENSE.txt'))


    def _getDEBIANPath (self):
        return self._getSubpath (self._debName, u'DEBIAN')


    def _getExecutableDir (self):
        return os.path.join (self._subdir_name,
                             self._debName,
                             u'usr',
                             u'lib',
                             u'outwiker')


    def _copyDebianFiles (self):
        debian_src_dir = os.path.join (u'need_for_build',
                                       u'debian_debbinary',
                                       u'debian')

        debian_dest_dir = self._getDEBIANPath()

        os.mkdir (debian_dest_dir)
        shutil.copyfile (os.path.join (debian_src_dir, u'control'),
                         os.path.join (debian_dest_dir, u'control'))

        shutil.copyfile (os.path.join (debian_src_dir, u'postinst'),
                         os.path.join (debian_dest_dir, u'postinst'))

        shutil.copyfile (os.path.join (debian_src_dir, u'postrm'),
                         os.path.join (debian_dest_dir, u'postrm'))


    def _setPermissions (self):
        for par, dirs, files in os.walk(self._getSubpath (self._debName)):
            for d in dirs:
                try:
                    os.chmod(os.path.join (par, d), 0o755)
                except OSError:
                    continue
            for f in files:
                try:
                    os.chmod(os.path.join (par, f), 0o644)
                except OSError:
                    continue

        exe_dir = self._getExecutableDir()
        os.chmod(os.path.join (self._root_build_dir,
                               exe_dir,
                               u'outwiker'), 0o755)

        DEBIAN_dir = self._getDEBIANPath()

        os.chmod(os.path.join (DEBIAN_dir, u'postinst'), 0o755)
        os.chmod(os.path.join (DEBIAN_dir, u'postrm'), 0o755)
        os.chmod(os.path.join (self._build_dir,
                               self._debName,
                               u'usr',
                               u'bin',
                               u'outwiker'), 0o755)


    def _buildDeb (self):
        with lcd (self._build_dir):
            local (u'fakeroot dpkg-deb --build {}'.format (self._debName))

        deb_filename = self._getDebFileName()
        shutil.move (self._getSubpath (deb_filename),
                     os.path.join (self._root_build_dir, deb_filename))

        with lcd (self._root_build_dir):
            local (u'lintian {}.deb'.format (self._debName))


    def _move_to_share (self, destdir):
        """Move images, help etc to /usr/share folder."""
        dir_names = [u'help', u'iconset', u'images', u'locale', u'spell', u'styles']

        share_dir = os.path.join (destdir, u'usr', u'share', u'outwiker')
        os.makedirs (share_dir)

        for dir_name in dir_names:
            src_dir = os.path.join (destdir, u'usr', u'lib', u'outwiker', dir_name)
            dst_dir = os.path.join (share_dir, dir_name)
            shutil.move (src_dir, dst_dir)
            with lcd (destdir):
                local (u'ln -s ../../share/outwiker/{dirname} usr/lib/outwiker'.format (dirname = dir_name))


    def _copy_share (self, destdir):
        """Copy icons files for deb package"""
        share_dir = os.path.join (destdir, u'usr', u'share')
        bin_dir = os.path.join (destdir, u'usr', u'bin')

        debian_dir = os.path.join (u'need_for_build', u'debian')
        shutil.copytree (os.path.join (debian_dir, u'usr', u'share'), share_dir)

        # Make link to bin file
        os.makedirs (bin_dir)

        exe_file = os.path.join (bin_dir, u'outwiker')
        src_bin_file = u'/usr/lib/outwiker/outwiker'
        with open (exe_file, 'w') as fp:
            fp.write ('#!/bin/sh\n')
            fp.write (src_bin_file)

        doc_dir = os.path.join (share_dir,
                                u'doc',
                                u'outwiker')

        shutil.copyfile (os.path.join (u'debian_debsource', u'changelog'),
                         os.path.join (doc_dir, u'changelog'))
        with lcd (doc_dir):
            local (u'gzip --best -n -c changelog > changelog.Debian.gz')
            local (u'rm changelog')


    def _getDebArchitecture (self):
        result = local (u'dpkg --print-architecture', capture=True)
        result = u''.join (result)
        return result.strip()


    def _getDebFileName (self):
        '''
        Return file name for deb package (file name only, not path)
        '''
        return u'{}.deb'.format (self._debName)


class BuilderBaseDebSource (BuilderBase):
    """
    The base class for source deb packages assebbling.
    """
    def __init__ (self, subdir_name):
        super (BuilderBaseDebSource, self).__init__ (subdir_name)


    def _debuild (self, command, distriblist):
        """
        Run command with debuild.
        The function assembles the deb packages for all releases in distriblist.
        """
        current_distrib_name = _getCurrentUbuntuDistribName()
        for distrib_name in distriblist:
            self._orig(distrib_name)
            current_debian_dirname = os.path.join (self._build_dir,
                                                   self._getDebName(),
                                                   'debian')

            # Change release name in the changelog file
            changelog_path = os.path.join (current_debian_dirname, u'changelog')
            self._makechangelog (changelog_path, current_distrib_name, distrib_name)

            with lcd (current_debian_dirname):
                local (command)

            # Return the source release name
            self._makechangelog (changelog_path, distrib_name, current_distrib_name)


    def _orig (self, distname):
        """
        Create an archive for "original" sources for building the deb package
        distname - Ubuntu release name
        """
        self._source()

        origname = self._getOrigName(distname)

        with lcd (self._build_dir):
            local ("tar -cvf {} {}".format (origname, self._getDebName()))

        orig_dirname = os.path.join (self._build_dir, origname)
        local ("gzip -f {}".format (orig_dirname))


    def _source(self):
        """
        Create a sources folder for building the deb package
        """
        self._debclean()

        dirname = os.path.join (self._build_dir, self._getDebName())
        os.makedirs (dirname)

        local ("rsync -avz * --exclude=.bzr --exclude=distrib --exclude=build --exclude=*.pyc --exclude=*.dll --exclude=*.exe --exclude=src/.ropeproject --exclude=src/test --exclude=src/setup.py --exclude=src/setup_tests.py --exclude=src/profile.py --exclude=src/tests.py --exclude=src/Microsoft.VC90.CRT.manifest --exclude=src/profiles --exclude=src/tools --exclude=doc --exclude=plugins --exclude=profiles --exclude=test --exclude=_update_version_bzr.py --exclude=outwiker_setup.iss --exclude=updateversion --exclude=updateversion.py --exclude=debian_tmp --exclude=Makefile_debbinary --exclude=need_for_build {dirname}/".format (dirname=dirname))

        os.rename (os.path.join (dirname, u'Makefile_debsource'),
                   os.path.join (dirname, u'Makefile'))

        os.rename (os.path.join (dirname, u'debian_debsource'),
                   os.path.join (dirname, u'debian'))


    def _debclean(self):
        """
        Clean build/<distversion> folder
        """
        dirname = os.path.join (self._build_dir, self._getDebName())
        if os.path.exists (dirname):
            shutil.rmtree (dirname)


    def _getDebName(self):
        """
        Return a folder name for sources for building the deb package
        """
        version = self._getVersion()
        return "outwiker-{}+{}".format (version[0], version[1])


    def _getOrigName (self, distname):
        version = self._getVersion()
        return "outwiker_{}+{}~{}.orig.tar".format (version[0], version[1], distname)


    def _makechangelog (self, changelog_path, distrib_src, distrib_new):
        """
        Update the changelog file for current Ubuntu release.
        """
        with open (changelog_path) as fp:
            lines = fp.readlines()

        lines[0] = lines[0].replace (distrib_src, distrib_new)

        with open (changelog_path, "w") as fp:
            fp.write (u"".join (lines))



class BuilderDebSource (BuilderBaseDebSource):
    def __init__ (self, subdir_name, release_names):
        super (BuilderBaseDebSource, self).__init__ (subdir_name)
        self._release_names = release_names


    def _build (self):
        self._debuild ("debuild --source-option=--include-binaries --source-option=--auto-commit",
                       self._release_names)


class BuilderDebSourcesIncluded (BuilderBaseDebSource):
    def __init__ (self, subdir_name, release_names):
        super (BuilderDebSourcesIncluded, self).__init__ (subdir_name)
        self._release_names = release_names


    def _build (self):
        self._debuild ("debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit",
                       self._release_names)


class BuilderSources (BuilderBase):
    """
    Create archives with sources
    """
    def __init__ (self, build_dir):
        super (BuilderSources, self).__init__ (build_dir)
        self._fullfname = os.path.join (self._root_build_dir,
                                        u"outwiker-src-full.zip")
        self._minfname = os.path.join (self._root_build_dir,
                                       u"outwiker-src-min.zip")


    def clear (self):
        super (BuilderSources, self).clear()
        self._remove (self._fullfname)
        self._remove (self._minfname)


    def _build (self):
        version = self._getVersion()

        local ('git archive --prefix=outwiker-{}.{}/ -o "{}" HEAD'.format (
            version[0],
            version[1],
            self._fullfname))

        with lcd ("src"):
            local ("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -xr!tests.py -xr!profile.py -xr!setup_tests.py -xr!setup.py -xr!test -xr!profiles ../{} ./*".format (self._minfname))

        self._remove (self._build_dir)


class BuilderPlugins (BuilderBase):
    """
    Create archives with plug-ins
    """
    def __init__ (self, build_dir, plugins_list):
        super (BuilderPlugins, self).__init__ (build_dir)
        self._all_plugins_fname = u'outwiker-plugins-all.zip'
        self._plugins_list = plugins_list


    def clear (self):
        super (BuilderPlugins, self).clear()
        self._remove (self._getSubpath (self._all_plugins_fname))


    def _build (self):
        for plugin in self._plugins_list:
            archive_name = plugin + u'.zip'
            archive_path = self._getSubpath (archive_name)
            full_archive_path = self._getSubpath (self._all_plugins_fname)
            self._remove (archive_path)

            with lcd ("plugins/{}".format (plugin)):
                local ("7z a -r -aoa -xr!*.pyc -xr!.ropeproject ../../{} ./*".format (archive_path))
                local ("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -w../ ../../{} ./*".format (full_archive_path))



def _getCurrentUbuntuDistribName ():
    with open ('/etc/lsb-release') as fp:
        for line in fp:
            line = line.strip()
            if line.startswith (u'DISTRIB_CODENAME'):
                codename = line.split(u'=')[1].strip()
                return codename


def deb_sources_included():
    """
    Create files for uploading in PPA (including sources)
    """
    builder = BuilderDebSourcesIncluded (DEB_SOURCE_BUILD_DIR, distribs)
    builder.build()


def deb():
    """
    Assemble the deb package
    """
    builder = BuilderDebSource (DEB_SOURCE_BUILD_DIR, distribs)
    builder.build()


def debsingle():
    """
    Assemble the deb package for the current Ubuntu release
    """
    builder = BuilderDebSource (DEB_SOURCE_BUILD_DIR,
                                [_getCurrentUbuntuDistribName()])
    builder.build()


def ppaunstable ():
    """
    Upload the current OutWiker version in PPA (unstable)
    """
    version = _getVersion()

    for distname in distribs:
        with lcd (os.path.join (BUILD_DIR, DEB_SOURCE_BUILD_DIR)):
            local ("dput ppa:outwiker-team/unstable outwiker_{}+{}~{}_source.changes".format (version[0], version[1], distname))


# def ppastable ():
#     """
#     Upload the current OutWiker version in PPA (unstable)
#     """
#     version = _getVersion()
#
#     for distname in distribs:
#         with lcd (os.path.join (BUILD_DIR, DEB_SOURCE_BUILD_DIR)):
#             local ("dput ppa:outwiker-team/ppa outwiker_{}+{}~{}_source.changes".format (version[0], version[1], distname))


def plugins():
    """
    Create an archive with plugins (7z required)
    """
    builder = BuilderPlugins (PLUGINS_DIR, plugins_list)
    builder.build()


def sources ():
    """
    Create the sources archives.
    """
    builder = BuilderSources (SOURCES_DIR)
    builder.build()


def win (skipinstaller=False):
    """
    Assemble builds under Windows
    """
    build_dir = u'build'
    src_pluginsdir = u"plugins"
    pluginsdir = os.path.join ("src", "plugins")
    win_build_dir = os.path.join (build_dir, u"outwiker_win")
    build_pluginsdir = os.path.join (win_build_dir, u'plugins')

    # Create the plugins folder (it is not appened to the git repository)
    _remove (pluginsdir)
    os.mkdir (pluginsdir)

    # Build by cx_Freeze
    with lcd ("src"):
        local ("python setup.py build --build-exe ../{}".format (win_build_dir))

    _remove (build_pluginsdir)
    os.mkdir (build_pluginsdir)

    # Remove old versions
    _remove ("build/outwiker_win_unstable.zip")
    _remove ("build/outwiker_win_unstable.7z")

    # Create archive without plugins
    with lcd (win_build_dir):
        local ("7z a ..\outwiker_win_unstable.zip .\* .\plugins -r -aoa")
        local ("7z a ..\outwiker_win_unstable.7z .\* .\plugins -r -aoa")

    # Compile installer
    if not skipinstaller:
        local ("iscc outwiker_setup.iss")

    # Copy plugins to build folder
    for plugin in plugins_list:
        shutil.copytree (
            os.path.join (src_pluginsdir, plugin, plugin),
            os.path.join (build_pluginsdir, plugin),
        )

    # Archive versions with plugins
    with lcd (win_build_dir):
        local ("7z a ..\outwiker_win_unstable_all_plugins.zip .\* .\plugins -r -aoa -xr!*.pyc -xr!.ropeproject")
        local ("7z a ..\outwiker_win_unstable_all_plugins.7z .\* .\plugins -r -aoa -xr!*.pyc -xr!.ropeproject")


def linux (create_archives=True, build_dir=LINUX_BUILD_DIR):
    """
    Assemble binary builds under Linux
    """
    builder = BuilderLinuxBinary (build_dir, create_archives)
    builder.build()


def nextversion():
    """
    Increment a version number (execute under Linux only, incremented the deb package version also)
    """
    # The file with version number
    fname = u"src/version.txt"

    with open (fname) as fp_in:
        lines = fp_in.readlines()

    lines[1] = str (int (lines[1]) + 1) + "\n"

    result = u"".join (lines)

    with open (fname, "w") as fp_out:
        fp_out.write (result)

    local ('dch -v "{}+{}~{}"'.format (lines[0].strip(),
                                       lines[1].strip(),
                                       _getCurrentUbuntuDistribName()))



def debinstall():
    """
    Assemble deb package for current Ubuntu release
    """
    debsingle()

    version = _getVersion()

    with lcd (os.path.join (BUILD_DIR, DEB_SOURCE_BUILD_DIR)):
        local ("sudo dpkg -i outwiker_{}+{}~{}_all.deb".format (
            version[0],
            version[1],
            _getCurrentUbuntuDistribName()))


def locale():
    """
    Update the localization file (outwiker.pot)
    """
    with lcd ("src"):
        local (r'find . -iname "*.py" | xargs xgettext -o locale/outwiker.pot')


def localeplugin (pluginname):
    """
    Create or update the localization file for pluginname plug-in
    """
    with lcd (os.path.join ("plugins", pluginname, pluginname)):
        local (r'find . -iname "*.py" | xargs xgettext -o locale/{}.pot'.format (pluginname))


def run ():
    """
    Run OutWiker from sources
    """
    with lcd ("src"):
        local ("python runoutwiker.py")


def test (section=u'', params=u''):
    """
    Run the unit tests
    """
    testdir = u'src'
    files = [fname[len(testdir) + 1:]
             for fname
             in glob.glob (u'{}/tests_*.py'.format (testdir))]
    files.sort()

    with lcd ("src"):
        if section:
            local ("python tests_{}.py {}".format (section, params))
        else:
            with settings (warn_only=True):
                for fname in files:
                    local ("python {}".format (fname, params))



def deb_binary ():
    builder = BuilderLinuxDebBinary (DEB_BINARY_BUILD_DIR)
    builder.build()


def _remove (path):
    """
    Remove the fname file if it exists. The function not catch exceptions.
    """
    if os.path.exists (path):
        if os.path.isfile (path):
            os.remove (path)
        elif os.path.isdir (path):
            shutil.rmtree (path)
