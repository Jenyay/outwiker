#!/usr/bin/python
# -*- coding: UTF-8 -*-

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


def _getVersion():
    """
    Return a tuple: (version number, build number)
    """
    # The file with version number
    fname = u"src/version.txt"

    with open (fname) as fp_in:
        lines = fp_in.readlines()

    return (lines[0].strip(), lines[1].strip())


def _getDebSourceDirName():
    """
    Return a folder name for sources for building the deb package
    """
    version = _getVersion()
    return "outwiker-{}+{}".format (version[0], version[1])


def _getOrigName (distname):
    version = _getVersion()
    return "outwiker_{}+{}~{}.orig.tar".format (version[0], version[1], distname)


def _debclean():
    """
    Clean build/<distversion> folder
    """
    local ('rm -rf build/{}'.format (_getDebSourceDirName()))


def _source():
    """
    Create a sources folder for building the deb package
    """
    _debclean()

    dirname = os.path.join ("build", _getDebSourceDirName())
    os.mkdir (dirname)

    local ("rsync -avz --exclude=.bzr --exclude=distrib --exclude=build --exclude=*.pyc --exclude=*.dll --exclude=*.exe * --exclude=src/.ropeproject --exclude=src/test --exclude=src/setup_win.py --exclude=src/setup_tests.py --exclude=src/profile.py --exclude=src/tests.py --exclude=src/Microsoft.VC90.CRT.manifest --exclude=src/profiles --exclude=src/tools --exclude=doc --exclude=plugins --exclude=profiles --exclude=test --exclude=_update_version_bzr.py --exclude=outwiker_setup.iss --exclude=updateversion --exclude=updateversion.py --exclude=debian_tmp {dirname}/".format (dirname=dirname))


def _orig (distname):
    """
    Create an archive for "original" sources for building the deb package
    distname - Ubuntu release name
    """
    _source()

    origname = _getOrigName(distname)

    with lcd ("build"):
        local ("tar -cvf {} {}".format (origname, _getDebSourceDirName()))

    local ("gzip -f build/{}".format (origname))


def debsource():
    """
    Create files for uploading in PPA (including sources)
    """
    _debuild ("debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit",
              distribs)


def deb():
    """
    Assemble the deb package
    """
    _debuild ("debuild --source-option=--include-binaries --source-option=--auto-commit",
              distribs)


def debsingle():
    """
    Assemble the deb package for the first Ubuntu release in the distribs list
    """
    _debuild ("debuild --source-option=--include-binaries --source-option=--auto-commit",
              [distribs[0]])


def _debuild (command, distriblist):
    """
    Run command with debuild. The function assembles the deb packages for all releases in distriblist.
    """
    for distname in distriblist:
        # Change release name in the changelog file
        _makechangelog (distribs[0], distname)

        _orig(distname)

        with lcd ("build/{}/debian".format (_getDebSourceDirName())):
            local (command)

        # Return the source release name
        _makechangelog (distname, distribs[0])


def ppaunstable ():
    """
    Upload the current OutWiker version in PPA (unstable)
    """
    version = _getVersion()

    for distname in distribs:
        with lcd ("build".format (_getDebSourceDirName())):
            local ("dput ppa:outwiker-team/unstable outwiker_{}+{}~{}_source.changes".format (version[0], version[1], distname))


def plugins():
    """
    Create an archive with plugins (7z required)
    """
    _remove (u"build/plugins/outwiker-plugins-all.zip")

    for plugin in plugins_list:
        _remove (u"build/plugins/{}.zip".format (plugin))

        with lcd ("plugins/{}".format (plugin)):
            local ("7z a -r -aoa -xr!*.pyc -xr!.ropeproject ../../build/plugins/{}.zip ./*".format (plugin))
            local ("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -w../ ../../build/plugins/outwiker-plugins-all.zip ./*".format (plugin))


def source ():
    """
    Create the sources archives.
    """
    version = _getVersion()

    sourcesdir = os.path.join ("build", "sources")

    if not os.path.exists (sourcesdir):
        os.mkdir (sourcesdir)

    fullfname = u"outwiker-src-full.zip"
    srcfname = u"outwiker-src-min.zip"

    _remove (fullfname)
    _remove (srcfname)

    local ('git archive --prefix=outwiker-{}.{}/ -o "{}/{}" HEAD'.format (version[0], version[1], sourcesdir, fullfname))

    with lcd ("src"):
        local ("7z a -r -aoa -xr!*.pyc -xr!.ropeproject -xr!tests.py -xr!profile.py -xr!setup_tests.py -xr!setup_win.py -xr!test -xr!profiles ../{}/{} ./*".format (sourcesdir, srcfname))


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
        local ("python setup_win.py build")

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


def linux ():
    """
    Assemble builds under Windows
    """
    build_dir = u'build'
    pluginsdir = os.path.join ("src", "plugins")
    linux_build_dir = os.path.join (build_dir, u"outwiker_linux")
    build_pluginsdir = os.path.join (linux_build_dir, u'plugins')

    toRemove = [
        os.path.join (linux_build_dir, u'tcl'),
        os.path.join (linux_build_dir, u'tk'),
        os.path.join (linux_build_dir, u'PyQt4.QtCore.so'),
        os.path.join (linux_build_dir, u'PyQt4.QtGui.so'),
        os.path.join (linux_build_dir, u'_tkinter.so'),
        # os.path.join (linux_build_dir, u'pango.so'),
        # os.path.join (linux_build_dir, u'pangocairo.so'),
        # os.path.join (linux_build_dir, u'cairo._cairo.so'),
    ]

    # Create the plugins folder (it is not appened to the git repository)
    _remove (pluginsdir)
    os.mkdir (pluginsdir)

    # Build by cx_Freeze
    with lcd ("src"):
        local ("python setup_linux.py build")

    map (_remove, toRemove)

    _remove (build_pluginsdir)
    os.mkdir (build_pluginsdir)

    # Remove old versions
    _remove ("build/outwiker_linux_unstable_x64.zip")
    _remove ("build/outwiker_linux_unstable_x64.7z")

    # Create archive without plugins
    with lcd (linux_build_dir):
        local ("7z a ../outwiker_linux_unstable_x64.zip ./* ./plugins -r -aoa")
        local ("7z a ../outwiker_linux_unstable_x64.7z ./* ./plugins -r -aoa")


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

    local ('dch -v "{}+{}~{}"'.format (lines[0].strip(), lines[1].strip(), distribs[0]))



def debinstall():
    """
    Assemble the first deb package in distribs and install it.
    """
    debsingle()

    version = _getVersion()

    with lcd ("build"):
        local ("sudo dpkg -i outwiker_{}+{}~{}_all.deb".format (version[0], version[1], distribs[0]))


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


def _makechangelog (distrib_src, distrib_new):
    """
    Update the changelog file for current Ubuntu release.
    """
    fname = "debian/changelog"

    with open (fname) as fp:
        lines = fp.readlines()

    lines[0] = lines[0].replace (distrib_src, distrib_new)

    with open (fname, "w") as fp:
        fp.write (u"".join (lines))


def _remove (path):
    """
    Remove the fname file if it exists. The function not catch exceptions.
    """
    if os.path.exists (path):
        if os.path.isfile (path):
            os.remove (path)
        elif os.path.isdir (path):
            shutil.rmtree (path)
