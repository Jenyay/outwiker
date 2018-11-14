# -*- coding: utf-8 -*-

import os


# Supported Ubuntu releases
UBUNTU_RELEASE_NAMES = ["xenial"]

# List of the supported plugins
PLUGINS_LIST = [
    "autorenamer",
    "counter",
    "datagraph",
    "diagrammer",
    "export2html",
    "externaltools",
    "hackpage",
    "htmlformatter",
    "htmlheads",
    "lightbox",
    "livejournal",
    "markdown",
    "pagetypecolor",
    "readingmode",
    "sessions",
    "snippets",
    "source",
    "spoiler",
    "statistics",
    "tableofcontents",
    "texequation",
    "thumbgallery",
    "updatenotifier",
    "webpage",
]

LANGUAGES = ['en', 'de', 'it_IT', 'ru_R', 'sv', 'uk_UA']

BUILD_DIR = 'build'
BUILD_LIB_DIR = 'libs'
LINUX_BUILD_DIR = "linux"
WINDOWS_BUILD_DIR = "windows"
WINDOWS_EXECUTABLE_DIR = "outwiker_exe"
WINDOWS_INSTALLER_FILENAME = "outwiker_win_unstable.exe"
DEB_BINARY_BUILD_DIR = 'linux'
DEB_SOURCE_BUILD_DIR = 'linux/deb_source'
APPIMAGE_BUILD_DIR = 'linux'
SNAP_BUILD_DIR = 'linux'

SOURCES_DIR = 'sources'
PLUGINS_DIR = 'plugins'
PLUGIN_VERSIONS_FILENAME = 'plugin.xml'
OUTWIKER_VERSIONS_FILENAME = 'versions.xml'
NEED_FOR_BUILD_DIR = 'need_for_build'
COVERAGE_PARAMS = '--rcfile="../.coveragerc"'

FILES_FOR_UPLOAD_UNSTABLE_WIN = [
    'outwiker_win_unstable.exe',
    'outwiker_win_unstable.zip',
    'outwiker_win_unstable.7z',
    'outwiker_win_unstable_all_plugins.zip',
    'outwiker_win_unstable_all_plugins.7z',
]

FILES_FOR_UPLOAD_STABLE_WIN = [
    'outwiker_{version}_win.exe',
    'outwiker_{version}_win.zip',
    'outwiker_{version}_win.7z',
    'outwiker_{version}_win_all_plugins.zip',
    'outwiker_{version}_win_all_plugins.7z',
]

FILES_FOR_UPLOAD_UNSTABLE_LINUX = [
    'outwiker_linux_amd64.zip',
    'outwiker_linux_amd64.7z',
    'outwiker-{version}+{build}_amd64.deb',
    'Outwiker-x86_64.AppImage',
]

FILES_FOR_UPLOAD_STABLE_LINUX = [
    'outwiker_linux_{version}_amd64.zip',
    'outwiker_linux_{version}_amd64.7z',
    'outwiker-{version}+{build}_amd64.deb',
    'Outwiker-x86_64.AppImage',
]

PPA_DEV_PATH = 'ppa:outwiker-team/dev'
PPA_UNSTABLE_PATH = 'ppa:outwiker-team/unstable'
PPA_STABLE_PATH = 'ppa:outwiker-team/ppa'

# Timeout in seconds
DOWNLOAD_TIMEOUT = 15

# Parameters for deb building
TIMEZONE = '+0300'
try:
    DEB_MAINTAINER = os.environ['DEBFULLNAME']
except KeyError:
    DEB_MAINTAINER = 'Eugeniy Ilin'

try:
    DEB_MAINTAINER_EMAIL = os.environ['DEBEMAIL']
except KeyError:
    DEB_MAINTAINER_EMAIL = 'jenyay.ilin@gmail.com'


VM_BUILD_PARAMS = {
    # 'zesty64': {
    #     'vagrant_path': 'need_for_build/virtual/build_machines/zesty64',
    #     'host': '192.168.101.64',
    # },
    'xenial64': {
        'vagrant_path': 'need_for_build/virtual/build_machines/xenial64',
        'host': '192.168.101.65',
    },
    # 'artful64': {
    #     'vagrant_path': 'need_for_build/virtual/build_machines/artful64',
    #     'host': '192.168.101.66',
    # },
    # 'trusty64': {
    #     'vagrant_path': 'need_for_build/virtual/build_machines/trusty64',
    #     'host': '192.168.101.67',
    # },
}
