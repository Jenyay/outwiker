# -*- coding: utf-8 -*-

import os


# Supported Ubuntu releases
UBUNTU_RELEASE_NAMES = [u"xenial", "yakkety", "zesty"]

# List of the supported plugins
PLUGINS_LIST = [
    u"autorenamer",
    u"changepageuid",
    u"counter",
    u"diagrammer",
    u"datagraph",
    u"export2html",
    u"externaltools",
    u"hackpage",
    u"htmlformatter",
    u"htmlheads",
    u"lightbox",
    u"livejournal",
    u"markdown",
    u"pagetypecolor",
    u"readingmode",
    u"sessions",
    u"snippets",
    u"source",
    u"spoiler",
    u"statistics",
    u"style",
    u"tableofcontents",
    u"texequation",
    u"thumbgallery",
    u"updatenotifier",
    u"webpage",
]

BUILD_DIR = u'build'
LINUX_BUILD_DIR = u"outwiker_linux"
WINDOWS_BUILD_DIR = u"windows"
WINDOWS_EXECUTABLE_DIR = u"outwiker_exe"
WINDOWS_INSTALLER_FILENAME = u"outwiker_win_unstable.exe"
DEB_BINARY_BUILD_DIR = u'linux/deb_binary'
DEB_SOURCE_BUILD_DIR = u'linux/deb_source'
SOURCES_DIR = u'sources'
PLUGINS_DIR = u'plugins'
PLUGIN_VERSIONS_FILENAME = u'plugin.xml'
OUTWIKER_VERSIONS_FILENAME = u'versions.xml'
NEED_FOR_BUILD_DIR = u'need_for_build'

FILES_FOR_UPLOAD_UNSTABLE_WIN = [
    u'windows/outwiker_win_unstable.exe',
    u'windows/outwiker_win_unstable.zip',
    u'windows/outwiker_win_unstable.7z',
    u'windows/outwiker_win_unstable_all_plugins.zip',
    u'windows/outwiker_win_unstable_all_plugins.7z',
]

FILES_FOR_UPLOAD_STABLE_WIN = [
    u'windows/outwiker_{version}_win.exe',
    u'windows/outwiker_{version}_win.zip',
    u'windows/outwiker_{version}_win.7z',
    u'windows/outwiker_{version}_win_all_plugins.zip',
    u'windows/outwiker_{version}_win_all_plugins.7z',
]

PPA_DEV_PATH = u'ppa:outwiker-team/dev'
PPA_UNSTABLE_PATH = u'ppa:outwiker-team/unstable'
PPA_STABLE_PATH = u'ppa:outwiker-team/ppa'

# Timeout in seconds
DOWNLOAD_TIMEOUT = 15

# Parameters for deb building
TIMEZONE = '+0300'
try:
    DEB_MAINTAINER = os.environ['DEBFULLNAME']
except KeyError:
    DEB_MAINTAINER = u'Eugeniy Ilin'

try:
    DEB_MAINTAINER_EMAIL = os.environ['DEBEMAIL']
except KeyError:
    DEB_MAINTAINER_EMAIL = u'jenyay.ilin@gmail.com'


VM_BUILD_PARAMS = {
    u'xenial_64': {
        u'vagrant_path': 'need_for_build/virtual/build_machines/xenial_64',
        u'host': u'192.168.100.64',
        u'archive_suffix': u'_x64',
    },

    u'xenial_32': {
        u'vagrant_path': 'need_for_build/virtual/build_machines/xenial_32',
        u'host': u'192.168.100.32',
        u'archive_suffix': u'_x86',
    },
}
